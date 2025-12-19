import os
import sys

from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QFileDialog, QScrollArea, QLineEdit, QHBoxLayout,
                             QListWidget, QInputDialog, QMessageBox, QLabel)

from frontend.cartas import cartas
from frontend.parametros import estilo, apuesta_min_blackjack


class VentanaBlackjack(QWidget):
    senal_pedir_carta = pyqtSignal()
    senal_plantarse = pyqtSignal()
    senal_apuesta = pyqtSignal(int)
    
    def __init__(self) -> None:
        super().__init__()
        
        base_dir = os.path.dirname(__file__)
        self.path_carpeta = os.path.join(base_dir, 'Assets', 'Blackjack')
        self.cartas_cargadas = {}
        
        self.username = None
        self.jugadores = {1: 'jugador 1',
                          2: 'jugador 2',
                          3: 'jugador 3',
                          4: 'jugador principal'}
        
        self.cartas_j1 = {}
        self.cartas_j2 = {}
        self.cartas_j3 = {}
        self.cartas_player = {}
        self.cartas_dealer = {}
        
        self.cartas_jugadores = {1: self.cartas_j1,
                                 2: self.cartas_j2,
                                 3: self.cartas_j3,
                                 4: self.cartas_player,
                                 5: self.cartas_dealer}
        
        self.inicializa_gui()
    
    def inicializa_gui(self) -> None: #Propiedades básicas de la ventana
        self.posicion = (400, 400)
        self.porte = (850, 500)
        self.setGeometry(*self.posicion, *self.porte)
        self.setWindowTitle('Blackjack')
        
        self.generar_layout()
    
    def generar_layout(self):
        '''
        Genera el layout principal de la ventana
        '''
        self.cargar_cartas()
        hbox_main = QHBoxLayout()
        
        hbox_main.addLayout(self.jugador_izquierda())
        hbox_main.addSpacing(10)
        hbox_main.addLayout(self.layout_central())
        hbox_main.addSpacing(10)
        hbox_main.addLayout(self.jugador_derecha())
        
        self.setLayout(hbox_main)
    
    def jugador_izquierda(self): 
        #Genera el layout del jugador de la izquierdo
        hbox = QHBoxLayout()
        vbox_cartas = QVBoxLayout()
        
        for x in range(4):
            self.cartas_j1[f'{x+1}'] = QLabel()
            self.cartas_j1[f'{x+1}'].setFixedSize(64, 64)
            self.cartas_j1[f'{x+1}'].setStyleSheet(estilo)
            vbox_cartas.addWidget(self.cartas_j1[f'{x+1}'])
        
        self.username_j1 = self.jugadores[1]
        
        username = QLabel(self.username_j1)
        
        hbox.addLayout(vbox_cartas)
        hbox.addWidget(username)
        
        return hbox

    def layout_central(self):
        '''
        Genera el layout central de la ventana. Esta contiene los botones y cartas del jugador
        superior, el dealer y el jugador principal.
        '''
        vbox_main = QVBoxLayout()
        
        vbox_main.addLayout(self.jugador_superior())
        vbox_main.addSpacing(10)
        vbox_main.addLayout(self.layout_dealer())
        vbox_main.addSpacing(10)
        vbox_main.addLayout(self.layout_player())
        
        return vbox_main
    
    def jugador_superior(self):
        vbox = QVBoxLayout()
        hbox_cartas = QHBoxLayout()
        
        for x in range(4):
            self.cartas_j2[f'{x+1}'] = QLabel()
            self.cartas_j2[f'{x+1}'].setFixedSize(64, 64)
            self.cartas_j2[f'{x+1}'].setStyleSheet(estilo)
            hbox_cartas.addWidget(self.cartas_j2[f'{x+1}'])
        
        username = QLabel(self.jugadores[2])
        username.setAlignment(Qt.AlignCenter)
        
        vbox.addLayout(hbox_cartas)
        vbox.addWidget(username)
        
        return vbox
    
    def layout_dealer(self):
        vbox = QVBoxLayout()
        hbox_cartas = QHBoxLayout()
        
        hbox_cartas.setContentsMargins(0, 0, 0, 0)
        
        for x in range(4):
            self.cartas_dealer[f'{x+1}'] = QLabel()
            self.cartas_dealer[f'{x+1}'].setFixedSize(64, 64)
            self.cartas_dealer[f'{x+1}'].setStyleSheet(estilo)
            
            hbox_cartas.addWidget(self.cartas_dealer[f'{x+1}'])
            
        username = QLabel('Dealer')
        username.setAlignment(Qt.AlignCenter)
        
        vbox.addLayout(hbox_cartas)
        vbox.addWidget(username)
        
        return vbox
    
    def layout_player(self):
        vbox = QVBoxLayout()
        hbox_cartas = QHBoxLayout()
        
        for x in range(4):
            self.cartas_player[f'{x+1}'] = QLabel()
            self.cartas_player[f'{x+1}'].setFixedSize(64, 64)
            self.cartas_player[f'{x+1}'].setStyleSheet(estilo)
            hbox_cartas.addWidget(self.cartas_player[f'{x+1}'])
        
        vbox.addLayout(hbox_cartas)
        vbox.addLayout(self.dashboard_player())
        
        return vbox
        
    def dashboard_player(self):
        hbox = QHBoxLayout()
        vbox_acciones = QVBoxLayout()
        
        self.boton_plantarse = QPushButton('Plantarse')
        self.boton_plantarse.clicked.connect(self.plantarse)
        self.boton_plantarse.setDisabled(True)
        vbox_acciones.addWidget(self.boton_plantarse)
        
        self.boton_pedir = QPushButton('Pedir')
        self.boton_pedir.clicked.connect(self.senal_pedir_carta.emit)
        self.boton_pedir.setDisabled(True)
        vbox_acciones.addWidget(self.boton_pedir)
        hbox.addLayout(vbox_acciones)
        
        self.boton_apostar = QPushButton('Apostar')
        self.boton_apostar.clicked.connect(self.apostar)
        hbox.addWidget(self.boton_apostar)
        hbox.addSpacing(10)
        self.username = self.jugadores[4]
        
        usuario = QLabel(self.username)
        hbox.addWidget(usuario)
        
        self.boton_volver = QPushButton('Menu')
        hbox.addWidget(self.boton_volver)
        self.boton_exit = QPushButton('Exit')
        self.boton_exit.clicked.connect(sys.exit)
        hbox.addWidget(self.boton_exit)
        
        return hbox
        
    
    def cargar_cartas(self) -> None:
        for carta in cartas.keys():
            path_completo = os.path.join(self.path_carpeta, f'{cartas[carta]}.png')
            pixmap = QPixmap(path_completo)
            self.cartas_cargadas[carta] = pixmap
    
    def jugador_derecha(self):
        hbox = QHBoxLayout()
        vbox_cartas = QVBoxLayout()
        
        for x in range(4):
            self.cartas_j3[f'{x+1}'] = QLabel()
            self.cartas_j3[f'{x+1}'].setFixedSize(64, 64)
            self.cartas_j3[f'{x+1}'].setStyleSheet(estilo)
            vbox_cartas.addWidget(self.cartas_j3[f'{x+1}'])
        
        self.username_j3 = self.jugadores[3]
        
        username = QLabel(self.username_j3)
        
        hbox.addWidget(username)
        hbox.addLayout(vbox_cartas)
        
        return hbox
    
    def apostar(self):
        apuesta, ok = QInputDialog.getInt(None, "Menu Apuestas", "Por favor inserte su apuesta:",
                                          apuesta_min_blackjack, apuesta_min_blackjack)
        if ok:
            self.boton_apostar.setDisabled(True)
            self.senal_apuesta.emit(apuesta)
    
    def resultados(self, resultados: dict):
        pass

    def actualizar_cartas(self, manos: dict):
        mapa_asientos = {
            1: self.cartas_j1,
            2: self.cartas_j2,
            3: self.cartas_j3
        }
        for username, cartas_data in manos.items():
            labels_jugador = None
            if username == 'dealer':
                labels_jugador = self.cartas_dealer
            elif username == self.username:
                labels_jugador = self.cartas_player
            else:
                for seat_num, player_name in self.jugadores.items():
                    if player_name == username:
                        seat_key = int(seat_num)
                        if seat_key in mapa_asientos:
                            labels_jugador = mapa_asientos[seat_key]
                        break
            if labels_jugador:
                if isinstance(cartas_data, list):
                    for label in labels_jugador.values():
                        label.clear()
                    for i, carta_str in enumerate(cartas_data):
                        if carta_str in self.cartas_cargadas:
                            pixmap = self.cartas_cargadas[carta_str]
                            labels_jugador[str(i+1)].setPixmap(pixmap)
                            labels_jugador[str(i+1)].setScaledContents(True)
                            labels_jugador[str(i+1)].repaint()
                else:
                    carta_str = cartas_data
                    for i in range(1, 5): 
                        label = labels_jugador[str(i)]
                        if not label.pixmap() or label.pixmap().isNull():
                            if carta_str in self.cartas_cargadas:
                                pixmap = self.cartas_cargadas[carta_str]
                                label.setPixmap(pixmap)
                                label.setScaledContents(True)
                                label.repaint()
                            break
                        
    
    def turno(self):
        self.boton_apostar.setDisabled(True)
        self.boton_pedir.setDisabled(False)
        self.boton_plantarse.setDisabled(False)
    
    def plantarse(self):
        self.boton_apostar.setDisabled(True)
        self.boton_pedir.setDisabled(True)
        self.boton_plantarse.setDisabled(True)
        self.senal_plantarse.emit()
    
    def revelar_cartas(self, cartas: list):
        for i, carta_str in enumerate(cartas):
            pixmap = self.cartas_cargadas[carta_str]
            self.cartas_dealer[str(i+1)].setPixmap(pixmap)
            self.cartas_dealer[str(i+1)].setScaledContents(True)

    def reinicio_ronda(self):
        self.boton_apostar.setDisabled(False)
    
    def actualizar_asientos(self, asientos: dict):
        '''
        Actualiza los asientos de los jugadores, se asegura que siempre el jugador 
        este en el asiento 4
        '''
        print(asientos)
        self.jugadores = asientos
        print(self.jugadores)
        if self.jugadores[4] != self.username:
            for asiento in self.jugadores:
                if self.jugadores[asiento] == self.username:
                    asiento_a_cambiar = asiento
                    break
            self.jugadores[asiento_a_cambiar] = self.jugadores[4]
            self.jugadores[4] = self.username
    
    def recibir_carta(self, carta: dict):
        del carta['comando']
        self.actualizar_cartas(carta)

if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaBlackjack()
    ventana.show()


    sys.exit(app.exec())