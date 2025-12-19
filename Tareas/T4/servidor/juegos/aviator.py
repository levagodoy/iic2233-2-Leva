from random import choice, betavariate
from collections import deque
from abc import ABC, abstractmethod
from threading import Thread, Lock, Event
from math import e
from datetime import datetime
from time import sleep
from parametros import DURACION_RONDA_AVIATOR, APUESTA_MINIMA_AVIATOR

from juegos.base import Base

class Aviator(Base):
    def __init__(self, servidor):
        super().__init__(servidor)
        self.nombre = 'Aviator'
        self.id = 'A'
        self.estado = None
        
        self.postores_minimos = 3
        self.retirados = {}
        self.tiempo_actual = 0

    def calcular_tiempo(self):
        '''
        Calcula el tiempo de crash
        '''
        return betavariate(1.4, 4.0) * DURACION_RONDA_AVIATOR
    
    def multiplicador(self, t: float) -> float:
        '''
        Calcula el multiplicador
        '''
        return e**(0.55*t)
    
    def retirarse(self, username):
        '''
        Recibe la señal de retiro del jugador
        '''
        mult = self.multiplicador(self.tiempo_actual)
        self.retirados[username] = mult
        
        mensaje = {'comando': 'retirado', 
                    'multiplicador': mult, 
                    'ganancia': int(self.apuestas[username] * mult)}
        self.enviar_mensaje(username, mensaje)

    def periodo_apuestas(self):
        '''
        Periodo de apuestas
        '''
        self.estado = 'apuestas'
        self.capacidad_requerida.wait()
        print('Iniciando Aviator!')
        self.periodo_ejecuccion()
    
    def periodo_ejecuccion(self):
        '''
        Periodo de ejecuccion
        '''
        self.estado = 'ejecuccion'
        t_crash = self.calcular_tiempo() #Calcula el tiempo de la ronda
        self.tiempo_actual = 0
        
        self.retirados = {}
        
        for nombre in self.jugadores: #Avisa a todos los jugadores que se inicia el juego
            self.enviar_mensaje(nombre, {'comando': 'aviator_inicio'})

        while self.tiempo_actual < t_crash: #Mientras no se crashee
            mult = self.multiplicador(self.tiempo_actual)
            
            mensaje = {'comando': 'aviator_update', 
                       'multiplicador': mult, 
                       'tiempo': self.tiempo_actual}
            for nombre in self.jugadores:
                self.enviar_mensaje(nombre, mensaje)
            
            sleep(0.1) #Actualiza 
            self.tiempo_actual += 0.1
            
        # Fin del juego   
        mensaje = {'comando': 'aviator_crash', 'multiplicador': mult_crash}
        for nombre in self.jugadores:
            self.enviar_mensaje(nombre, mensaje)
            
        self.periodo_resultados()

    def periodo_resultados(self):
        '''
        Periodo de resultados
        '''
        self.estado = 'resultados'
        self.enviar_ganancias()
        
        self.capacidad_requerida.clear()
        self.postores = []
        self.apuestas = {}
        self.resultados = {}
        self.retirados = {}
        
        self.periodo_apuestas()

    def enviar_ganancias(self):
        '''
        Envía las ganancias al servidor
        '''
        numero = 0
        mensaje = {}
        for nombre in self.postores: #Envia las ganancias al servidor
            hora_actual = datetime.now().timestamp()
            if nombre in self.retirados:
                mult = self.retirados[nombre]
                ganancia = int(self.apuestas[nombre] * (mult - 1))
                mensaje[numero] = {'id': self.id, 
                                   'nombre':nombre, 
                                   'hora': hora_actual, 
                                   'ganancia': ganancia}
            else:
                mensaje[numero] = {'id': self.id, 
                                   'nombre':nombre, 
                                   'hora': hora_actual, 
                                   'ganancia': -self.apuestas[nombre]}
            numero += 1
        self.servidor.guardar_balance(mensaje, self.id)