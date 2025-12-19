import os
import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QInputDialog, QScrollArea, QLineEdit, QHBoxLayout,
                             QListWidget, QComboBox, QMessageBox, QLabel)


class VentanaPrincipal(QWidget):
    
    senal_unirse_juego = pyqtSignal(str)
    senal_carga_balance = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.inicializa_gui()
        
    def inicializa_gui(self) -> None: #Propiedades básicas de la ventana
        self.posicion = (400, 400)
        self.porte = (500, 300)
        self.setGeometry(*self.posicion, *self.porte)
        self.setWindowTitle('Principal')

        self.generar_layout()

    def generar_layout(self) -> None:
        '''
        Genera el layout de la ventana
        '''
        self.hbox = QHBoxLayout()
        
        self.lista_ganancias = QListWidget()
        self.lista_ganancias.setFixedWidth(200)
        
        self.hbox.addWidget(self.lista_ganancias)
        self.hbox.addLayout(self.botones_principales())
        
        self.setLayout(self.hbox)
    
    def botones_principales(self) -> None:
        '''
        Crea todos los botones principales y sus layouts
        '''
        vbox_principal = QVBoxLayout()
        
        botones_juegos = QHBoxLayout()
        
        self.boton_blackjack = QPushButton('B')
        self.boton_blackjack.clicked.connect(self.unirse_blackjack)
        self.boton_blackjack.setMinimumHeight(180)
        botones_juegos.addWidget(self.boton_blackjack)
        
        self.boton_crash = QPushButton('C')
        self.boton_crash.setMinimumHeight(180)
        self.boton_crash.clicked.connect(self.unirse_aviator)
        botones_juegos.addWidget(self.boton_crash)
        
        self.boton_ruleta = QPushButton('R')
        self.boton_ruleta.setMinimumHeight(180)
        self.boton_ruleta.clicked.connect(self.unirse_ruleta)
        botones_juegos.addWidget(self.boton_ruleta)
        
        vbox_principal.addLayout(botones_juegos)
        vbox_principal.addLayout(self.layout_inferior())
        
        return vbox_principal
    
    
    def layout_inferior(self) -> None:
        '''
        Crea el layout inferior (Ventana de recarga y datos del usuario)
        '''
        hbox = QHBoxLayout()
        self.boton_recarga = QPushButton('V.R.')
        self.boton_recarga.clicked.connect(self.cargar_balance)
        hbox.addWidget(self.boton_recarga)
        hbox.addWidget(self.datos_usuario())
        return hbox
    
    def datos_usuario(self) -> None:
        '''
        Crea el label de datos del usuario
        '''
        self.nombre = 'default'
        self.balance = 500
        self.label_datos = QLabel(f'{self.nombre} \nBalance: {self.balance}')
        return self.label_datos
    
    
    def mostrarse(self, username: str, balance: int) -> None:
        '''
        Muestra la ventana
        '''
        print(username)
        self.nombre = username
        self.balance = balance
        
        self.label_datos.setText(f'{self.nombre} \nBalance: {self.balance}')
        
        self.show()
    
    def cargar_balance(self) -> None:
        '''
        Carga el balance del usuario
        '''
        carga, ok = QInputDialog.getInt(None, "Menu Recarga", "Por favor inserte el monto a cargar:")
        if ok:
            self.senal_carga_balance.emit(carga)
            self.balance += carga
            self.label_datos.setText(f'{self.nombre} \nBalance: {self.balance}')
    
    def unirse_blackjack(self) -> None:
        '''
        Envía la señal de unirse al juego de Blackjack
        '''
        self.senal_unirse_juego.emit('Blackjack')
        
    def unirse_aviator(self) -> None:
        '''
        Envía la señal de unirse al juego de Aviator
        '''
        self.senal_unirse_juego.emit('Aviator')
    
    def unirse_ruleta(self) -> None:
        '''
        Envía la señal de unirse al juego de Ruleta
        '''
        self.senal_unirse_juego.emit('Ruleta')
    
    def error_union(self) -> None:
        '''
        Muestra un mensaje de error
        '''
        mensaje = QMessageBox()
        mensaje.setText("Error, la partida está en juego!")
        mensaje.setWindowTitle("Error")
        mensaje.setDefaultButton(QMessageBox.Ok)
        mensaje.exec_()






if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()


    sys.exit(app.exec())