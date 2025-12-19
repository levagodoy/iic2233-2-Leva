import sys
import os
from typing import Generator
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton)


from frontend.parametros import(x1, x2, y1, y2, 
                       max_planetas, factor_radio)

from utilidades import radio_planeta

class VentanaMapa(QWidget):
    senal_regreso = pyqtSignal() #Envia la señal para cerrar esta ventana y abrir la principal.
    coordenadas = [x1,x2,y1,y2] #Guarda las coordenadas dadas en parametros
    max_planetas = max_planetas 
    senal_planetas = pyqtSignal(list) #Envia la señal con los datos necesarios para la consulta
    def __init__(self) -> None:
        super().__init__()
        self.inicializa_gui()
    
    def inicializa_gui(self) -> None:
        '''
        Crea la estructura base de la ventana.
        '''
        self.posicion = (400, 400)
        self.porte = (1500, 900)
        self.setGeometry(*self.posicion, *self.porte)
        self.setWindowTitle('Mapa')
        
        self.generar_layout()
    
    def recibir_path(self, path: str) -> None:
        '''
        Cualquier path seleccionado en la Ventana Principal se guarda automaticamente en esta 
        ventana. Ejecuta la función enviar_coordenadas para iniciar
        tempranamente la consulta.
        '''
        self.path = path
        self.enviar_coordenadas()
    
    def enviar_coordenadas(self) -> None:
        '''
        Envia los datos necesarios para su consulta, se ejecuta en su iniciación
        '''
        info = [self.coordenadas, self.max_planetas, self.path]
        self.senal_planetas.emit(info)
        
    def recibir_planetas(self, generador: Generator) -> None:
        '''
        Recibe el generador dado por la consulta e inicia la creación del layout
        '''
        self.planetas = generador
        
        self.generar_layout()
    def generar_layout(self) -> None:
        '''
        El layout consiste de un único vbox, que contiene el mapa con los planetas y 
        el boton para regresar a la ventana principal
        '''
        vbox = QVBoxLayout()
        
        self.main_label = QLabel()
        self.main_label.resize(1200, 800) #Label con el mapa
        self.main_label.setStyleSheet("border: 2px solid blue; background-color: lightblue;")
        self.boton_regreso = QPushButton('Boton de regreso')
        #Se conecta el boton con la función para regresar a la ventana principal
        self.boton_regreso.clicked.connect(self.regresar) 
        
        vbox.addWidget(self.boton_regreso)
        vbox.addWidget(self.main_label)
        
        self.setLayout(vbox)
        
    
    def regresar(self) -> None:
        '''
        Abre la ventana principal y se cierra a si mismo.
        '''
        self.senal_regreso.emit()
        self.close()
            
            
        
        

if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaMapa()
    ventana.show()


    sys.exit(app.exec())