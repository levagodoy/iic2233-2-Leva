from random import choice, betavariate
from collections import deque
from abc import ABC, abstractmethod
from threading import Thread, Lock, Event
from math import e
from datetime import datetime
from time import sleep
from parametros import DURACION_RONDA_AVIATOR, APUESTA_MINIMA_AVIATOR

from juegos.base import Base


class Blackjack(Base):
    
    def __init__(self, servidor):
        super().__init__(servidor)
        self.nombre = 'Blackjack'
        self.id = 'B'
        self.estado = None
        
        self.asientos_ocupados = {1: None,
                                  2: None,
                                  3: None,
                                  4: None}
        self.postores_minimos = 4
        self.mano_dealer = 0
        
        self.espera_acciones = Event()

        self.resultados = {}
        self.manos_juego = {}
        self.valores_cartas = {'A': 11,
                          '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, 
                          '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}
        self.valores_manos = {}
        
        categorias = ['c', 'd', 'h', 's']
        cartas = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.mazo = [f'{carta}{categoria}' for categoria in categorias for carta in cartas]
        #https://www.geeksforgeeks.org/python/blackjack-console-game-using-python/
    
    def recibir_apuesta(self, username, monto):
        '''
        Recibe la apuesta del jugador. Usa los mismos metodos que la superclase,
        pero ademas, asigna el asiento al jugador
        '''
        super().recibir_apuesta(username, monto)
        for asiento in self.asientos_ocupados:
            if self.asientos_ocupados[asiento] == None:
                self.asientos_ocupados[asiento] = username
                break
    
    def enviar_mensaje(self, nombre, mensaje):
        '''
        Envia cualquier mensaje al jugador, excepto al dealer
        '''
        if nombre == 'dealer':
            return
        
        super().enviar_mensaje(nombre, mensaje)
    
    def enviar_asientos(self):
        '''
        Envía el mensaje de asientos a todos los jugadores
        '''
        mensaje = {'asientos': self.asientos_ocupados}
        print(mensaje)
        for nombre in self.jugadores.keys():
            if nombre == 'dealer':
                continue
            self.enviar_mensaje(nombre, {'comando': 'asientos',
                                         'asientos': self.asientos_ocupados})

    def periodo_apuestas(self):
        '''
        Periodo de apuestas
        '''
        self.estado = 'apuestas' #Cambia su estado global

        self.capacidad_requerida.wait() #Espera a que se cumplan las condiciones
        self.jugadores['dealer'] = None #Asigna el dealer
        
        self.enviar_asientos()
        print('Preparacion exitosa!')
        
        sleep(2)



        self.periodo_ejecuccion()
    
    def periodo_ejecuccion(self):
        '''
        Primero entrega la primera carta, luego un diccionario en que solo envia la carta
        correspondiente, y tercero, calcular el valor de todas las manos
        '''
        print('Primera ronda de cartas:')
        self.estado = 'ejecuccion' #Cambia su estado global 

        #Entrega primera carta
        for nombre in self.jugadores.keys():
            carta = choice(self.mazo)
            self.manos_juego[nombre] = [carta]
        for nombre in self.jugadores.keys(): #Envia las cartas publicas a todos los jugadores
            self.enviar_mensaje(nombre, {'comando': 'actualizar_cartas',
                                         'manos': self.manos_juego})
        
        sleep(5)
        
        print('Segunda Ronda de Cartas')
        
        #Entrega segunda carta
        for nombre in self.jugadores.keys():
            carta = choice(self.mazo)
            self.manos_juego[nombre].append(carta)
            mensaje = {nombre: 'Bb' for nombre in self.jugadores.keys()}
            mensaje[nombre] = carta
            #Envia solo la carta del jugador, todo el resto son privadas
            self.enviar_mensaje(nombre, {'comando': 'actualizar_cartas',
                                         'manos': mensaje})
        
        sleep(5)
        
        print('Cartas entregadas!')
        
        #Valoracion Manos
        for nombre in self.jugadores.keys():
            valor_mano = self.valorar_mano(self.manos_juego[nombre])
            
            mensaje = {'Valor mano': valor_mano}
            #Envia el valor de la mano a todos los jugadores
            self.enviar_mensaje(nombre, {'comando': 'valor_mano',
                                         'valor': valor_mano})
            self.valores_manos[nombre] = valor_mano
            if nombre == 'dealer':
                self.mano_dealer = valor_mano

        #Periodo de acciones
        for nombre in self.jugadores.keys():
            if nombre == 'dealer':
                continue
            #Envia el turno de blackjack a todos los jugadores
            self.enviar_mensaje(nombre, {'comando': 'turno_blackjack'})
            self.espera_acciones.clear()
            self.espera_acciones.wait()
        
        #Turno dealer
        self.revelar_cartas()
        self.turno_dealer()
            
        
        self.periodo_resultados()

        
    def periodo_resultados(self):
        '''
        Periodo de resultados
        '''
        self.estado = 'resultados'
        
        for nombre in self.jugadores.keys():
            if nombre == 'dealer':
                continue
            #Evalua si el jugador gano
            jugador_valor = self.valores_manos[nombre]
            if jugador_valor > 21:
                self.resultados[nombre] = False
            elif self.mano_dealer > 21:
                self.resultados[nombre] = True
            elif jugador_valor > self.mano_dealer:
                self.resultados[nombre] = True
            else:
                self.resultados[nombre] = False
        for nombre in self.jugadores.keys():
            if nombre == 'dealer':
                continue
            self.enviar_mensaje(nombre, {'comando': 'resultados',
                                         'resultados': self.resultados})
        
        self.enviar_ganancias() #Se envian las ganancias a todos los jugadores y al servidor
        
        sleep(10)
        #Periodo de apuestas
        self.capacidad_requerida.clear() #Se reinicia el evento
        
        self.asientos_ocupados = {1: None,
                                  2: None,
                                  3: None,
                                  4: None}
        self.postores = []
        self.apuestas = {}
        self.valores_manos = {}
        self.resultados = {}
        self.mano_dealer = 0
        
        self.periodo_apuestas() #Se reinicia el periodo de apuestas

    def valorar_mano(self, mano : list):
        '''
        Valora la mano de un jugador
        '''
        valor_mazo = 0
        ases = 0
        for carta in mano:
            numero = carta[:-1]
            valor = self.valores_cartas.get(numero, 0)
            valor_mazo += valor
            if numero == 'A':
                ases += 1
        
        while valor_mazo > 21 and ases > 0:
            valor_mazo -= 10
            ases -= 1
            
        return valor_mazo
    
    def pedir_carta(self, nombre):
        '''
        Recibe el pedido de carta de un jugador
        '''
        carta = choice(self.mazo)
        self.manos_juego[nombre].append(carta)
        valor_mano = self.valorar_mano(self.manos_juego[nombre])
        for username in self.jugadores.keys():
            if username == 'dealer':
                continue
            print(nombre)
            self.enviar_mensaje(username, {'comando': 'pedir_carta', 
                                         'username': nombre,
                                         'carta': carta})
        if valor_mano > 21:
            self.espera_acciones.set()
        else:
            self.enviar_mensaje(nombre, {'comando': 'turno_blackjack'})
    
    def turno_dealer(self):
        self.mano_dealer = self.valorar_mano(self.manos_juego['dealer'])
        while self.mano_dealer < 17:
            self.pedir_carta('dealer')
            sleep(1)
            self.mano_dealer = self.valorar_mano(self.manos_juego['dealer'])
        self.espera_acciones.set()
    
    def revelar_cartas(self):
        for nombre in self.jugadores.keys():
            if nombre == 'dealer':
                continue
            self.enviar_mensaje(nombre, {'comando': 'revelar_cartas',
                                         'manos': self.manos_juego['dealer']})
    
    def plantarse(self, nombre):
        self.espera_acciones.set()