import socket
import sys
import requests
import json
import time
from datetime import datetime

from thread_cliente import ThreadCliente
from juegos.blackjack import Blackjack
from juegos.aviator import Aviator
from juegos.base import Ruleta
from parametros import MONTO_INICIO
from parametros import TOKEN_AUTENTICACION

class Servidor:
    TOKEN = TOKEN_AUTENTICACION
    """
    Clase que representa un servidor distribuidor de archivos.
    En cuanto se instancia levanta un socket para escuchar potenciales
    clientes.
    """

    def __init__(self, port: int, host: str, puerto_api: int) -> None:
        """
        Inicializar el servidor.
        """
        self.host = host
        self.port = port
        self.puerto_api = puerto_api
        
        self.base = f'http://{host}:{puerto_api}'
        
        self.clientes = {}
        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        self.cargar_juegos()
    
    def cargar_juegos(self):
        blackjack = Blackjack(self)
        blackjack.start()
        ruleta = Ruleta(self)
        aviator = Aviator(self)
        aviator.start()
        
        self.ids = {
            'Blackjack': blackjack,
            'Ruleta': ruleta,
            'Aviator': aviator,
            'Peposit': 'Deposito'
        }

    def bind_listen(self) -> None:
        """
        Método que conecta el servidor al host y port dado.
        """
        print(self.host, self.port)
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        print(f"Servidor escuchando en {self.host} : {self.port}")

    def accept_connections_thread(self) -> None:
        """
        Función encargada de aceptar clientes y asignarles un Thread para su atención.
        """
        while True:
            socket_cliente, address = self.socket_server.accept()
            print(f"Nuevo cliente conectado: {socket_cliente} {address}")

            listening_client_thread = ThreadCliente(
                 socket_cliente, address, self
            )

            # Siempre se recomienda guardar la info del cliente para fácil acceso
            # (administrar clientes, cortar conexiones, etc.)
            listening_client_thread.start()
    
    def guardar_cliente(self, usuario, username):
        '''
        Asigna el un username al cliente, y guarda su informacion en
        self.clientes
        '''
        if username in self.clientes:
            usuario.mensajes_a_enviar.put({'comando': 'correctitud',
                                            'informacion': False})
            raise Exception('Username ya esta ocupado')
        else:
            self.clientes[username] = usuario
            self.consulta_balance(username)


    def consulta_balance(self, username:str) -> int:
        '''
        Llama a la informacion del cliente
        '''
        url = self.base + f'/users/{username}'
        try:
            respuesta = requests.get(url)
            respuesta.raise_for_status()  
            
            info = respuesta.json().get('info')
            user = self.clientes[username]
            user.balance = info[2]
        
        except requests.exceptions.HTTPError:
            self.registrar_usuario(username)
    def registrar_usuario(self, username: str) -> int:
        '''
        En caso de no existir, registra al usuario
        '''
        url = self.base + f'/users'
        header = {'Authorization': self.TOKEN}
        body = {'username': username}
        
        requests.post(url, data=json.dumps(body), headers=header)
        self.clientes[username].mensajes_a_enviar.put({'comando': 'correctitud',
                                                            'informacion': True,
                                                            'balance': MONTO_INICIO})
    
    def guardar_balance(self, cambios: dict, id_juego: str) -> None:
        '''
        Guarda la informacion de la ultima ronda en ganancias.csv
        '''
        url = self.base + f'/games/{id_juego}'
        header = {'Authorization': self.TOKEN}
        body = cambios
        requests.post(url, data=json.dumps(body), headers=header)
    
    def ultimas_ganancias(self, n=None):
        url = self.base + f'/games/'
        params = {}
        if n is not None:
            params['n'] = n
        
        respuesta = requests.get(url, params=params)

    def actualizar_usuario(self, username, earning):
        url = self.base + f'/users/{username}'
        header = {'Authorization': self.TOKEN}
        body = {'earnings': earning}
        
        requests.patch(url, data = json.dumps(body), headers=header)
        
        hora_actual = datetime.now()
        hora_actual = hora_actual.timestamp()
        
        cambios = {'id': 'P',
                   'nombre': username,
                   'hora': hora_actual,
                   'monto': earning}
        
        self.guardar_balance(cambios, 'P')

    
    def unirse_al_juego(self, username: str, id_juego: str) -> None:
        '''
        Intenta conectar al cliente en el juego solicitado
        '''
        juego = self.ids[id_juego]
        user = self.clientes[username]
        if juego.conectar_usuario(user):
            user.juego = juego
            return True
        else:
            return False
        
    def abandonar_el_juego(self, username:str, id_juego: str) -> None:
        '''
        Desconecta al cliente del juego
        '''
        user = self.clientes[username]
        juego = self.ids[id_juego]
        
        juego.desconectar_usuario(user)
        user.juego = None
    
    def apostar(self, username:str, id_juego: str, monto: int) -> None:
        '''
        Accion generica de apuestas en el juego correspondiente
        '''
        juego = self.ids[id_juego]
        
        juego.recibir_apuesta(username, monto)

    def eliminar_cliente(self, username: str) -> None:
        """
        Elimina al cliente del diccionario de clientes y lo desconecta del juego si es necesario.
        """
        if username in self.clientes:
            cliente = self.clientes[username]
            if cliente.juego:
                self.abandonar_el_juego(username, cliente.juego.nombre)
            
            if username in self.clientes:
                del self.clientes[username]
            print(f"Cliente {username} eliminado correctamente.")
