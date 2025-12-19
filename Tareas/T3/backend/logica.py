from PyQt5.QtCore import QObject, pyqtSignal
from typing import Generator

from backend.consultas import encontrar_planetas_cercanos
from backend.diccionario import consulta

class ControladorLogico(QObject):
    senal_vuelta_consulta = pyqtSignal(object) #Devuelve el generador con los datos filtrados
    senal_mapa = pyqtSignal(object) #Devuelve el generador de los mapas
    consulta = consulta #Guarda el diccionario que contiene las funciones por nombre de entidad
    
    def __init__(self):
        super().__init__()
    
    def enviar_generador(self, lista):
        '''
        Funcion que solo recibe una lista con el path, nombre de la identidad a consultar,
        y el filtro de dicha consulta
        '''
        path = f'{lista[0]}/{lista[1]}.csv'
        try:
            generador = self.consulta[lista[1]](path)
        except FileNotFoundError:
            error = ["Error! Consulta invalida!"]
            error = iter(error)
            self.senal_vuelta_consulta.emit(error)
        
        try:
            if lista[2] == "":
                #Si es que no se puso algun filtro, se devuelve el generador como tal
                self.senal_vuelta_consulta.emit(generador)
            else:
                consultas = lista[2].split(",")
                try:
                    for consulta in consultas:
                        #Por cada filtro, se hace una nueva iteracion de filtros
                        consulta = consulta.split("=")
                        llave = consulta[0]
                        valor = consulta[1]
                        if valor.isdigit(): #Si es que el filtro es algun int, se convierte a tal
                            valor = int(consulta[1])
                        generador = filter(lambda gen, llave=llave, 
                                           valor=valor: getattr(gen, llave) == valor,
                                        generador)
                    self.senal_vuelta_consulta.emit(generador)
                except:
                    error = ["Error! Consulta invalida!"]
                    error = iter(error)
                    self.senal_vuelta_consulta.emit(error)
        except:
            error = ["Error! Consulta invalida!"]
            error = iter(error)
            self.senal_vuelta_consulta.emit(error)
        
    def encontrar_planetas(self, info):
        '''
        Recibe todos los datos para encontrar los planetas cercanos,
        transmite de vuelta todos los planetas cercanos en base a los filtros
        '''
        coordenadas = info[0]
        max_planetas = info[1]
        
        planetas = encontrar_planetas_cercanos(coordenadas, max_planetas)
        
        self.senal_mapa.emit(planetas)