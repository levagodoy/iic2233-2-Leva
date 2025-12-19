import os
import sys

from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, 
                             QFileDialog, QScrollArea, QLineEdit, QHBoxLayout,
                             QListWidget, QComboBox, QMessageBox, QLabel)

import time

class VentanaAviator(QWidget):
    
    senal_apostar = pyqtSignal(int)
    senal_retirarse = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.path_carpeta = os.path.join('Assets', 'Aviator')
        self.setWindowTitle('Aviator')
        self.setGeometry(100, 100, 600, 400)
        
        self.init_gui()
        
    def init_gui(self):
        pass