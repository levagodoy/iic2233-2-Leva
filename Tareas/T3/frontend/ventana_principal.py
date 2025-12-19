import os
import sys
from typing import Generator
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QFileDialog, QScrollArea, QLineEdit, QHBoxLayout,
                             QListWidget, QComboBox, QMessageBox)

class VentanaPrincipal(QWidget):
    
    senal_consulta = pyqtSignal(list) #Envia todos los datos necesarios para hacer consultas
    senal_mapa = pyqtSignal() #Señal para abrir la ventana de mapa
    senal_path = pyqtSignal(str) #Señal que envia el path a la ventana de mapa
    
    def __init__(self) -> None:
        super().__init__()
        self.inicializa_gui()
    
    def inicializa_gui(self) -> None: #Propiedades básicas de la ventana
        self.posicion = (400, 400)
        self.porte = (1500, 900)
        self.setGeometry(*self.posicion, *self.porte)
        self.setWindowTitle('Principal')

        self.generar_layout()
    
    
    def generar_layout(self) -> None:
        '''
        Nuestro hbox se divide entre el layout de la izquierda y los botones
        de la derecha
        '''
        hbox = QHBoxLayout()
        
        hbox.addLayout(self.layout_izquierda()) #Se ejecuta la funcion del layout de la izquierda
        hbox.addStretch(10)
        hbox.addLayout(self.botones_laterales())
        self.setLayout(hbox)
    
    def layout_izquierda(self) -> None:
        '''
        Nuestro Layout de la izquierda contiene, el boton de consultas,
        la lista de resultados y un QFileDialog para insertar el path
        '''
        vbox = QVBoxLayout() #Se divide manera vertical; botones arriba y la lista debajo
        
        self.lista_consulta = QListWidget() #QListWidget para poder exponer multiples resultados
        
        area_scroll = QScrollArea() #Area scrolleable para mostrar nuestra lista de consultas
        area_scroll.setWidgetResizable(True)
        area_scroll.setFixedWidth(1200)
        area_scroll.setWidget(self.lista_consulta)
        
        hbox = QHBoxLayout() #Creamos el hbox para nuestra parte superior
        self.boton_archivo() #Ejecutamos la función que crea nuestro boton para seleccionar el path
        hbox.addWidget(self.boton_path) #Agregamos nuestro boton recien creado
        hbox.addStretch()
        hbox.addLayout(self.consultas()) #Se ejecuta la función de layout de los botones de consulta
        
        vbox.addLayout(hbox)
        vbox.addWidget(area_scroll)
        
        return vbox

    def boton_archivo(self) -> None:
        '''
        Crea el botón para seleccionar el path en el atributo self.boton_path. Si es que se
        aprieta dicho botón, iniciará la función self.abrir_archivo, la cual contiene la lógica
        para el QFileDialog
        '''
        self.path = "Seleccionar Path"
        self.boton_path = QPushButton(self.path)
        self.boton_path.clicked.connect(self.abrir_archivo) 
    
    def consultas(self) -> None:
        '''
        Creamos los dos botones de consultas, el primero es un combo box que contiene todos los
        tipo de datos posibles, y otro para typpear la consulta en especifico
        '''
        hbox = QHBoxLayout()
        self.combo_box = QComboBox()
        self.combo_box.addItems(['Astronauta', 'Nave', 'Tripulación', 'Planeta', 'Mineral',
                            'PlanetaMineral', 'Mision', 'MisionMineral']) #Contenido ComboBox
        self.texto_consulta = QLineEdit('Consulta')
        self.texto_consulta.resize(100,100)
        
        hbox.addWidget(self.combo_box)
        hbox.addWidget(self.texto_consulta)
        return hbox
    
    def botones_laterales(self) -> None:
        '''
        Crea todos los botones laterales
        '''
        vbox = QVBoxLayout()
        boton_ejecucion = QPushButton('Boton de Ejecucion')
        boton_ejecucion.clicked.connect(self.consultar) 
        boton_mapa = QPushButton('Boton de Mapa')
        boton_mapa.clicked.connect(self.abrir_mapa)
        
        vbox.addWidget(boton_ejecucion)
        vbox.addStretch()
        vbox.addWidget(boton_mapa)
        
        return vbox
        
        
    def abrir_archivo(self) -> None:
        '''
        Guarda la ruta en file_path y cambia el texto del boton para que muestre la ruta
        seleccionada
        '''
        file_path = QFileDialog.getExistingDirectory(self, "Abrir Directorio")
        self.path = file_path
        self.boton_path.setText(self.path)
        
    def consultar(self) -> None:
        '''
        Guarda todos los datos necesarios para hacer nuestra consulta. 
        Envia la entidad a consultar, el path y la consulta a hacer.
        '''
        entidad = self.combo_box.currentText()
        consulta = self.texto_consulta.text()
        
        senal = [self.path, entidad, consulta]
        
        sender = self.sender()
        identificador = sender.text()
        self.senal_consulta.emit(senal) #Se envia la lista
    
    def actualizar_lista(self, generador: Generator) -> None:
        '''
        Recibe el generador filtrado por los parametros puestos en la consulta,
        la función se encarga de actualizar self.lista_consulta con los nuevos datos entregados.
        '''
        self.lista_consulta.clear()
        for item in generador:
            info = ""
            try:
                for nombre, dato in zip(item._fields, item):
                    string = f'{nombre}: {dato}'
                    info = f'{info}/{string}'
            except AttributeError:
                self.lista_consulta.addItem(item)
            self.lista_consulta.addItem(info)
    
    def abrir_mapa(self) -> None:
        '''
        Abre la ventana del mapa, solo si es que se ha seleccionado un path previamente,
        si no, se ejecuta un MessageBox que muestra un error.
        '''
        if os.path.exists(self.path) == False:
            mensaje = QMessageBox()
            mensaje.setText("Error! Debes primero seleccionar un path")
            mensaje.setWindowTitle("Error")
            mensaje.setDefaultButton(QMessageBox.Ok)
            mensaje.exec_()
        else:
            self.senal_mapa.emit()
            self.close()
        
    
    
            
                





if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])
    ventana = VentanaPrincipal()
    ventana.show()


    sys.exit(app.exec())