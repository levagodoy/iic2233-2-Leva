import socket
import json
import time
import sys
import math
from PyQt5.QtCore import QThread, pyqtSignal
from backend.parametros import CLAVE_CASINO

class Cliente(QThread):
    
    senal_username = pyqtSignal(bool, int)
    senal_juego = pyqtSignal(bool, str)
    senal_desconexion = pyqtSignal()
    senal_actualizar_cartas = pyqtSignal(dict)
    senal_turno_blackjack = pyqtSignal()
    senal_asientos = pyqtSignal(dict)
    senal_revelar_cartas = pyqtSignal(list)
    senal_enviar_carta = pyqtSignal(dict)

    def __init__(self, HOST, PORT): 
        super().__init__()
        
        self.host = HOST
        self.port = PORT
        self.chunk_size = 2**16
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            self.socket.connect((self.host, self.port))
            print("[BACK] Conectado correctamente al servidor.")

        except ConnectionError as e:
            print(f"[BACK] No se logró conectar: {e}")
            self.socket.close()
            exit()
        
    def enviar_mensaje(self, mensaje: dict):
        """
        Envía un mensaje (dict) al servidor, encriptado con el protocolo.
        """
        try:
            # 1. Serializa el mensaje
            bytes_mensaje = json.dumps(mensaje).encode("UTF-8")
            largo_original = len(bytes_mensaje)
            
            # 2. Agrega el padding necesario hasta que sea un multiplo de 124
            resto = largo_original % 124
            if resto != 0:
                padding = 124 - resto
                bytes_mensaje += b'\x00' * padding
            
            # 3. Crea el mensaje encriptado
            mensaje_encriptado = bytearray()
            
            # 4. Agrega el largo original al inicio 
            mensaje_encriptado.extend(largo_original.to_bytes(4, "little"))
            
            num_chunks = len(bytes_mensaje) // 124
            
            for i in range(num_chunks):
                chunk = bytes_mensaje[i*124 : (i+1)*124]
                
                # 5. Agrega el numero de chunk (4 bytes big endian)
                numero_bloque = i.to_bytes(4, "big")
                paquete = numero_bloque + chunk 
                
                # 6. Encripta el paquete con XOR
                paquete_encriptado = bytearray()
                for j in range(128):
                    paquete_encriptado.append(paquete[j] ^ CLAVE_CASINO[j])
                
                mensaje_encriptado.extend(paquete_encriptado)
            
            self.socket.sendall(mensaje_encriptado)
            
        except ConnectionError:
            print("[BACK] Error: No se pudo enviar el mensaje. Conexión perdida.")
            self.senal_desconexion.emit()
            
    
    def recibir_bytes(self, cantidad: int):
        """
        Recibe una cantidad específica de bytes desde el socket.
        """
        bytes_leidos = bytearray()
        while len(bytes_leidos) < cantidad:
            cantidad_restante = cantidad - len(bytes_leidos)
            bytes_leer = min(self.chunk_size, cantidad_restante)

            respuesta = self.socket.recv(bytes_leer)

            if not respuesta:
                # Si no hay respuesta, asumimos desconexión
                return None
            bytes_leidos.extend(respuesta)
        return bytes_leidos
    
    def run(self) -> None:
        """
        Loop principal para escuchar mensajes del servidor.
        """
        while True:
            try:
                #   1. Recibe el largo original
                bytes_largo = self.recibir_bytes(4)
                if bytes_largo is None:
                    print("[BACK] El servidor ha cerrado la conexión.")
                    self.senal_desconexion.emit()
                    break
                
                largo_original = int.from_bytes(bytes_largo, "little")
                
                if largo_original == 0:
                    continue 

                # Calcula cuantos chunks hay
                num_chunks = math.ceil(largo_original / 124)
                bytes_totales_encriptados = num_chunks * 128
                
                data_encriptada = self.recibir_bytes(bytes_totales_encriptados)
                if data_encriptada is None:
                    print("[BACK] El servidor ha cerrado la conexión durante la recepción.")
                    break
                
                chunks = {}
                
                for i in range(num_chunks): #Reconstruye el paquete por cada chunk
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
                        print(f"[BACK] Error: Falta el chunk {i}")
                
                # Truncar al largo original (Remueve los bytes de padding)
                mensaje_bytes = mensaje_bytes[:largo_original]
                
                mensaje = json.loads(mensaje_bytes.decode("UTF-8"))
                print(f"[BACK] Mensaje servidor: {mensaje}")
                
                self.procesar_mensaje(mensaje)
                

            except ConnectionError:
                print("[BACK] Conexión perdida con el servidor.")
                self.senal_desconexion.emit()
                self.socket.close()
                break
                
            except Exception as e:
                print(f"[BACK] Error inesperado en el loop de recepción: {e}")
                self.senal_desconexion.emit()
                self.socket.close()
                break
    
    def procesar_mensaje(self, mensaje: dict) -> None:
        """
        Procesa un mensaje recibido del servidor.
        """
        if mensaje.get('comando', 0 ) != 0:
            if mensaje['comando'] == 'correctitud': #Informacion sobre el usuario
                self.senal_username.emit(mensaje['informacion'], mensaje.get('balance', 0))
            
            elif mensaje["comando"] == 'conectarse': #Conexion al juego
                self.senal_juego.emit(True, mensaje["juego"])
           
            elif mensaje["comando"] == 'actualizar_cartas': #Actualiza las cartas
                if mensaje.get('username', 0) != 0:
                    print(mensaje['username'])
                self.senal_actualizar_cartas.emit(mensaje['manos'])
            
            elif mensaje["comando"] == 'turno_blackjack': #Turno del blackjack
                self.senal_turno_blackjack.emit()
            
            elif mensaje["comando"] == 'asientos': #Asientos disponibles de BJ
                self.senal_asientos.emit(mensaje['asientos'])
            
            elif mensaje["comando"] == 'revelar_cartas': #Revelar cartas del dealer
                self.senal_revelar_cartas.emit(mensaje['manos'])
            
            elif mensaje['comando'] == 'pedir_carta': #Pedir carta
                self.senal_enviar_carta.emit(mensaje)
        
        
        

