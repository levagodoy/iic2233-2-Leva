from random import choice, betavariate
from collections import deque
from abc import ABC, abstractmethod
from threading import Thread, Lock, Event
from math import e
from datetime import datetime
from time import sleep
from parametros import DURACION_RONDA_AVIATOR, APUESTA_MINIMA_AVIATOR


class Base(ABC, Thread):
    '''
    Clase base para todos los juegos
    '''
    def __init__(self, servidor):
        super().__init__()
        self.nombre = None
        self.id = None
                
        self.lock = Lock()
        self.daemon = True
        self.capacidad_requerida = Event()
        
        self.servidor = servidor
        self.jugadores = {}
        self.postores = []
        self.apuestas = {}
        self.resultados = {}
        
        self.postores_minimos = 0

    def conectar_usuario(self, usuario):
        '''
        Conecta un usuario al juego, revisa que no haya llegado al maximo de jugadores
        ''' 
        if self.capacidad_requerida != False:
            self.jugadores[usuario.username] = usuario
            print(f'{usuario.username} se ha conectado exitosamente a {self.nombre}!')
            return True
        else:
            return False
    
    def desconectar_usuario(self, usuario):
        '''
        Desconecta un usuario del juego
        '''
        del self.jugadores[usuario.username]
        
        print(f'{usuario.username} se ha desconectado exitosamente de {self.nombre}!')
    
    def desconectar_extras(self):
        '''
        Desconecta a los usuarios que no hayan apostado
        '''
        ausentes = self.jugadores.keys() - self.apuestas.keys()
        if len(ausentes) >= 1:
            for nombre in ausentes:
                self.servidor.abandonar_el_juego(nombre, self.nombre)
            return True
    
    def recibir_apuesta(self, username: str, monto: int):
        '''
        Recibe la apuesta del jugador
        ''' 
        self.apuestas[username] = monto
        self.postores.append(username)
        
        print(f'Apuesta de {username} con un monto total de: {monto} recibida en {self.nombre}!')
        
        if len(self.postores) == self.postores_minimos:
            self.desconectar_extras()
            self.capacidad_requerida.set()
    
    def enviar_ganancias(self):
        '''
        Envía las ganancias a todos los jugadores
        ''' 
        numero = 0
        mensaje = {}
        for nombre in self.resultados:
            hora_actual = datetime.now()
            hora_actual = hora_actual.timestamp()
            if self.resultados[nombre]:
                mensaje[numero] = {'id': self.id, 
                                   'nombre':nombre, 
                                   'hora': hora_actual, 
                                   'ganancia': 2*self.apuestas[nombre]}
            else:
                mensaje[numero] = {'id': self.id, 
                                   'nombre':nombre, 
                                   'hora': hora_actual, 
                                   'ganancia': -self.apuestas[nombre]}
            numero += 1
        self.servidor.guardar_balance(mensaje, self.id)
    
    def enviar_mensaje(self, nombre: str, mensaje: dict):   
        '''
        Envía un mensaje a un jugador
        ''' 
        self.jugadores[nombre].mensajes_a_enviar.put(mensaje)
    

    #Cada juego define su propios periodos.
    @abstractmethod
    def periodo_apuestas(self):
        pass
    
    @abstractmethod
    def periodo_ejecuccion(self):
        pass
    
    @abstractmethod
    def periodo_resultados(self):
        pass
    
    def run(self):
        
        self.periodo_apuestas()


class Ruleta(Base):
    def __init__(self, servidor):
        super().__init__(servidor)
        self.nombre = 'Ruleta'
        self.id = 'R'
        
        self.postores_minimos = 4
        
    def periodo_apuestas(self):
        return super().periodo_apuestas()
    
    def periodo_ejecuccion(self):
        return super().periodo_ejecuccion()
    
    def periodo_resultados(self):
        return super().periodo_resultados()