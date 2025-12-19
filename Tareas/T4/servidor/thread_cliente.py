from socket import socket
from queue import Queue
from random import randint
import threading
import json
import time
import math
from parametros import CLAVE_CASINO

class ThreadCliente(threading.Thread):
    """
    Clase que representa un cliente aceptado por el servidor.
    """

    def __init__(self, socket_cliente: socket, address: tuple, servidor) -> None:
        super().__init__()

        self.chunk_size = 2**16
        
        self.username = None
        self.balance = None
        
        self.socket = socket_cliente
        self.address = address
        
        self.juego = None
        self.servidor = servidor
        
        self.mensajes_a_enviar = Queue()
        self.daemon = True
        
        self.enviar_mensajes_thread = threading.Thread(
            target=self.procesar_mensajes_a_enviar, daemon=True
        )
        
        
    def procesar_mensajes_a_enviar(self) -> None:
        """
        Método encargado de ir enviando 1 mensaje a la vez si es que la cola
        para enviar mensajes tiene algo pendiente.
        """
        while True:
            mensaje = self.mensajes_a_enviar.get()

            try:
                # 1. Serializar el mensaje
                bytes_mensaje = json.dumps(mensaje).encode("UTF-8")
                largo_original = len(bytes_mensaje)
                
                # Agrega bits de padding para que el mensaje tenga un largo múltiplo de 124
                resto = largo_original % 124
                if resto != 0:
                    padding = 124 - resto
                    bytes_mensaje += b'\x00' * padding
                
                mensaje_encriptado = bytearray()
                
                # Agrega largo original al inicio
                mensaje_encriptado.extend(largo_original.to_bytes(4, "little"))
                
                #Calcula el numero total de chunks
                num_chunks = len(bytes_mensaje) // 124 
                
                #Recorre cada chunk
                for i in range(num_chunks):
                    chunk = bytes_mensaje[i*124 : (i+1)*124]
                    
                    # Concatenar número de chunk (4 bytes big endian)
                    numero_bloque = i.to_bytes(4, "big")
                    paquete = numero_bloque + chunk 
                    
                    # Encriptar con XOR
                    paquete_encriptado = bytearray()
                    for j in range(128):
                        paquete_encriptado.append(paquete[j] ^ CLAVE_CASINO[j])
                    
                    mensaje_encriptado.extend(paquete_encriptado)

                self.socket.sendall(mensaje_encriptado) #Envia el mensaje encriptado
                self.mensajes_a_enviar.task_done()

            except BrokenPipeError:
                self.mensajes_a_enviar.task_done()
                break
            except Exception as e:
                print(f"Error enviando mensaje al cliente {self.username}: {e}")
                self.mensajes_a_enviar.task_done()
    
    def recibir_bytes(self, cantidad: int) -> bytearray:
        """
        Este método de recibir bytes desde el cliente hasta completar una cantidad
        específica.
        """
        bytes_leidos = bytearray()
        while len(bytes_leidos) < cantidad:
            cantidad_restante = cantidad - len(bytes_leidos)
            bytes_leer = min(self.chunk_size, cantidad_restante)
            
            try:
                respuesta = self.socket.recv(bytes_leer)
            except ConnectionError:
                return None

            if not respuesta:
                return None
            
            bytes_leidos.extend(respuesta)
        return bytes_leidos
        
    def run(self) -> None:
        """
        Este método se encarga de escuchar los mensajes
         y utilizar el protocolo para decodificar el mensaje recibido.
        """

        self.enviar_mensajes_thread.start()
        while True:
            bytes_mensaje_parte_1 = self.recibir_bytes(4)
            
            if bytes_mensaje_parte_1 is None:
                print(f"Cliente [{self.username}] Cliente desconectado")
                break
                
            largo_mensaje = int.from_bytes(bytes_mensaje_parte_1, "little")

            if largo_mensaje == 0:
                # Mensaje de largo 0, se cerro el cliente
                continue

            # Calcula cuantos bytes leer (paquetes de 128 bytes)
            num_chunks = math.ceil(largo_mensaje / 124)
            bytes_totales_encriptados = num_chunks * 128

            # Ahora sabiendo el largo, recibamos el mensaje en sí:
            data_encriptada = self.recibir_bytes(bytes_totales_encriptados)
            
            if data_encriptada is None:
                print(f"Cliente [{self.username}] Cliente desconectado durante recepción")
                break

            try:
                chunks = {}
                for i in range(num_chunks):
                    paquete_encriptado = data_encriptada[i*128 : (i+1)*128]
                    # Desencriptar XOR
                    paquete_desencriptado = bytearray()
                    for j in range(128):
                        paquete_desencriptado.append(paquete_encriptado[j] ^ CLAVE_CASINO[j])
                    numero_bloque = int.from_bytes(paquete_desencriptado[:4], "big")
                    contenido_chunk = paquete_desencriptado[4:]
                    chunks[numero_bloque] = contenido_chunk
                
                # Ordenar y concatenar
                mensaje_bytes = bytearray()
                for i in range(num_chunks):
                    if i in chunks:
                        mensaje_bytes.extend(chunks[i])
                    else:
                        # Si falta un chunk, el mensaje está corrupto
                        raise ValueError(f"Falta el chunk {i}")
                
                # Truncar al largo original (eliminar los bytes de padding)
                mensaje_bytes = mensaje_bytes[:largo_mensaje]
                mensaje = json.loads(mensaje_bytes.decode("UTF-8"))
                
                # Procesar el mensaje
                self.procesar_mensaje(mensaje)
                
            except Exception as e:
                print(f"Error procesando mensaje: {e}")
                break
        
        if self.username:
            self.servidor.eliminar_cliente(self.username)
        self.socket.close()

    def procesar_mensaje(self, mensaje: dict) -> None:
        '''
        Procesa el mensaje recibido
        '''
        if mensaje['comando'] == 'Informacion':
            try:
                username = mensaje['username']
                self.servidor.guardar_cliente(self, username)
                
                self.username = username
            except:
                pass
        
        elif mensaje['comando'] == 'solicitar': #Solicita las ultimas 5 ganancias
            datos = self.servidor.ultimas_ganancias(5)
            self.mensajes_a_enviar.put({'datos' : 'ganancias',
                                        'info': datos})
            
        elif mensaje['comando'] == 'Conectarse':
            conexion = self.servidor.unirse_al_juego(self.username, mensaje['id_juego'])
            if conexion == True:
                self.mensajes_a_enviar.put({'comando': 'conectarse',
                                            'juego': mensaje['id_juego']})
            else:
                pass
        
        elif mensaje['comando'] == 'Desconectarse': #Desconecta al cliente del juego actual
            self.servidor.abandonar_el_juego(self.username, self.juego.nombre)
            
        elif mensaje['comando'] == 'apostar': #Hace una apuesta
            id_juego = self.juego.nombre
            monto = mensaje['monto']
            
            self.balance -= monto
            self.servidor.apostar(self.username, id_juego, monto)
        
        elif mensaje['comando'] == 'cargar': #Carga dinero al usuario   
            monto = mensaje['earnings']
            self.balance += monto
        
            self.servidor.actualizar_usuario(self.username, monto)
        
        #funciones BJ
        elif mensaje['comando'] == 'pedir_carta': #Pedir una carta
            self.juego.pedir_carta(self.username)
        
        elif mensaje['comando'] == 'plantarse': #Plantarse
            self.juego.plantarse(self.username)