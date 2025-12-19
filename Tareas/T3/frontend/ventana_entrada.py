import os
import sys
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton)


class VentanaEntrada(QWidget):
    '''
    Ventana de ingreso al programa.
    '''
    senal_ingreso = pyqtSignal() #Señal para abrir la ventana principal
    
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
        
        self.mensaje = QLabel("Bienvenido!", self) #Lo que queremos que diga el mensaje
        self.mensaje.setAlignment(Qt.AlignCenter) #Lo centramos
        self.mensaje.setMinimumHeight(100) #Su altura minima
        
        
        self.boton_ingreso = QPushButton("Botón de Ingreso") #Agregamos el boton de ingreso
        self.boton_ingreso.clicked.connect(self.ingreso) #Conectamos el boton a la funcion de ingreso

        main_layout.addStretch() #Agregamos un espacio previo al mensaje
        main_layout.addWidget(self.mensaje)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.boton_ingreso, 0, Qt.AlignHCenter) #Agregamos y centramos el boton
        main_layout.addStretch()
        self.setLayout(main_layout)   #Setteamos el layout
        
    def ingreso(self) -> None:
        '''
        Cuando el boton de ingreso, se ejecuta esta funcion, la cual emite una señal para abrir
        la ventana principal y cierra la ventana de entrada.
        '''
        self.senal_ingreso.emit()
        self.close()
    
    

if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaEntrada()
    ventana.show()


    sys.exit(app.exec())