import sys
import os
import json
from PyQt5.QtWidgets import QApplication

from frontend.ventana_inicio import VentanaEntrada
from frontend.ventana_principal import VentanaPrincipal
from frontend.ventana_blackjack import VentanaBlackjack
from frontend.ventana_aviator import VentanaAviator

from backend.juegos import Juegos

class Dccasino:
    def __init__(self):
        self.path = os.path.join('backend', 'conexion.json')
        with open(self.path, 'r') as f:
            self.datos = json.load(f)
        
        self.ventana_entrada = VentanaEntrada()
        self.ventana_principal = VentanaPrincipal()
        self.ventana_blackjack = VentanaBlackjack()
        self.ventana_aviator = VentanaAviator()
        self.cliente = Juegos(self.datos['host'], self.datos['puerto'])

    def conectar(self):
        #Todas las funciones de inicio de programa
        self.ventana_entrada.senal_username.connect(self.cliente.enviar_username)
        self.cliente.senal_username_cargado.connect(self.ventana_entrada.correctitud_ingreso)
        self.cliente.senal_mostar_vp.connect(self.ventana_principal.mostrarse)
        self.cliente.senal_desconexion.connect(self.cerrar)
        
        #Funciones menu principal
        self.ventana_principal.senal_unirse_juego.connect(self.cliente.unirse_juegos)
        self.ventana_principal.senal_carga_balance.connect(self.cliente.actualizar_balance)
        self.cliente.senal_abrir_juego.connect(self.abrir)
        self.cliente.senal_error.connect(self.ventana_principal.error_union)
        

        #Funciones Blackjack
        self.cliente.senal_actualizar_cartas.connect(self.ventana_blackjack.actualizar_cartas)
        self.cliente.senal_turno_blackjack.connect(self.ventana_blackjack.turno)
        self.cliente.senal_asientos.connect(self.ventana_blackjack.actualizar_asientos)
        self.cliente.senal_revelar_cartas.connect(self.ventana_blackjack.revelar_cartas)
        self.cliente.senal_enviar_carta.connect(self.ventana_blackjack.recibir_carta)

        self.ventana_blackjack.senal_apuesta.connect(self.cliente.apostar)
        self.ventana_blackjack.senal_pedir_carta.connect(self.cliente.pedir_carta)
        self.ventana_blackjack.senal_plantarse.connect(self.cliente.plantarse)

    def iniciar(self):
        self.ventana_entrada.show()
        
    def abrir(self, juego: str):
        if juego == 'Blackjack':
            self.ventana_principal.hide()
            self.ventana_blackjack.username = self.cliente.username
            self.ventana_blackjack.show()
            
        elif juego == 'Aviator':
            self.ventana_principal.hide()
            self.ventana_aviator.show()
    
    def cerrar(self):
        sys.exit()



def hook(type, value, traceback):
    print(type)
    print(traceback)
sys.__excepthook__ = hook

app = QApplication([])
dccasino = Dccasino()
dccasino.conectar()
dccasino.iniciar()
sys.exit(app.exec())