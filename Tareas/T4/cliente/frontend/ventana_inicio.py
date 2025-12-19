import os
import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton,
                             QHBoxLayout, QLineEdit, QMessageBox)


class VentanaEntrada(QWidget):
    '''
    Ventana de ingreso al programa.
    '''
    senal_username = pyqtSignal(str) #Señal para enviar el username actual
    
    def __init__(self) -> None:
        super().__init__()
        self.inicializa_gui()
        
    def inicializa_gui(self) -> None:
        self.posicion = (300, 300) #Se eligen las propiedades de la ventana
        self.porte = (400, 300)
        self.setGeometry(*self.posicion, *self.porte)
        self.setWindowTitle('Entrada')
        
        self.generar_widgets()
    
    def generar_widgets(self) -> None:
        '''
        Se crea el layout para la ventana
        '''
        main_layout = QVBoxLayout() #Se usa un layout vertical
        hbox = QHBoxLayout()
        
        self.mensaje = QLabel("Bienvenido a DCCasino!", self) #Lo que queremos que diga el mensaje
        self.mensaje.setAlignment(Qt.AlignCenter) #Lo centramos
        self.mensaje.setMinimumHeight(100) #Su altura minima
        font = QFont("Arial", 24)  # Font family "Arial", size 24 points
        self.mensaje.setFont(font)
        
        
        self.boton_ingreso = QPushButton("Botón de Ingreso") #Agregamos el boton de ingreso
        self.username = QLineEdit('Username')
        hbox.addWidget(self.username)
        hbox.addWidget(self.boton_ingreso)
        self.boton_ingreso.clicked.connect(self.ingreso) #Conectamos el boton a la funcion de ingreso

        main_layout.addStretch() #Agregamos un espacio previo al mensaje
        main_layout.addWidget(self.mensaje)
        main_layout.addSpacing(20)
        main_layout.addLayout(hbox)
        main_layout.addStretch()
        self.setLayout(main_layout)   #Setteamos el layout
        
    def ingreso(self) -> None:
        '''
        Cuando el boton de ingreso, se ejecuta esta funcion, la cual emite una señal para abrir
        la ventana principal y cierra la ventana de entrada.
        '''
        self.senal_username.emit(self.username.text())
    
    def correctitud_ingreso(self, info) -> None:
        if info == True:
            self.close()
        else:
            mensaje = QMessageBox()
            mensaje.setText("Error, ese username está actualmente conectado!")
            mensaje.setWindowTitle("Error")
            mensaje.setDefaultButton(QMessageBox.Ok)
            mensaje.exec_()
        
        
    
    

if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaEntrada()
    ventana.show()


    sys.exit(app.exec())