from abc import ABC, abstractmethod
from random import randint
from copy import copy


class InteligenciaArtificial():
    
    def __init__(self, nombre:str, vida_max:int, atk:int, descripcion:str, prob_esp:float,
                 velocidad:float):
        self.nombre = nombre
        self.vida = vida_max
        self.vida_max = vida_max
        self.ataque = atk
        self.descripcion = descripcion
        self.velocidad = velocidad * 100 #Se multiplica por 100 para luego compararla con randint
        self.prob_esp = prob_esp * 100
        self._jugador = None #Guarda como atributo el jugador actual, asi poder acceder
                            #atributos o metodos
        
        
    @property    
    def jugador(self):
        pass
    
    @jugador.getter
    def jugador(self):
        return self._jugador
    
    @jugador.setter
    def jugador(self, jugador):
        self._jugador = jugador
    
    def atacar(self):
        dano = self.ataque 
        return dano
    
    def recibir_dano(self, dano):
        print(f"{self.nombre} ha recibido {dano} de daño!")
        self.vida -= round(dano)
        pass
    
    def habilidad_especial(self):
        '''
        Debido a que siempre sus habilidades son usadas previas al ataque,
        no es necesario dividirlas por etapas
        '''
        pass
    
    def __str__(self):
        return f'{self.nombre}: HP {self.vida}/{self.vida_max} |\nHabilidad: {self.descripcion}' 

    
class CatGPT(InteligenciaArtificial):
    '''
    Cambia todos los multiplicadores de todas las cartas
    a 0.65
    '''
    def habilidad_especial(self):
        if randint(0, 100) <= self.prob_esp:
            for carta in self.jugador.cartas:
                carta.mult_ataque = 0.65
                carta.mult_def = 0.65

class CowPilot(InteligenciaArtificial):
    def habilidad_especial(self):
        if len(self.jugador.cartas) >1: #solo inicia si el mazo tiene mas de una carta
            if randint(0, 100) <= self.prob_esp:
                indice_copia = randint(0, len(self.jugador.cartas) -1) #Se copia alguna carta
                copia = self.jugador.cartas[indice_copia]
                for i in range(2):
                    indice = randint(0, len(self.jugador.cartas) -1)
                    while indice == indice_copia:
                        indice = randint(0, len(self.jugador.cartas) -1)
                    self.jugador.cartas.pop(indice) #Se remueven dos cartas aleatorias
                for i in range(2):
                    self.jugador.cartas.append(copia) #se suman copias de la instancia copiada
            
class Crok(InteligenciaArtificial):
    
    def __init__(self, nombre, vida_max, atk, descripcion, prob_esp, velocidad):
        super().__init__(nombre, vida_max, atk, descripcion, prob_esp, velocidad)
        self.contador = 0 #Se crea un nuevo atributo de contador para ser usado en su habilidad
    
    def habilidad_especial(self):
        self.contador -= 1
        if self.contador <= 0:
            if randint(0, 100) <= self.prob_esp:
                self.contador = 4
                indice_viejo = 0
                for i in range(2):
                    if i == 1:
                        indice = randint(0, len(self.jugador.cartas) -1)
                        self.carta1 = self.jugador.cartas[indice]
                        self.multatk_c1 = copy(self.carta1.mult_ataque) #se guardan sus valores
                        self.multdef_c1 = copy(self.carta1.mult_def) 
                        self.carta1.mult_def = 0 #se editan sus multiplicadores
                        self.carta1.mult_ataque = 0
                        indice_viejo = indice #Se guarda el valor del indice de la carta previa
                    else:
                        if len(self.jugador.cartas) == 1: 
                            break #Si es que el mazo no tiene mas de una carta, entonces se termina
                        indice = randint(0, len(self.jugador.cartas) -1)
                        while indice == indice_viejo: #Repite hasta tener un indice distinto
                            indice = randint(0, len(self.jugador.cartas) -1) 
                        self.carta2 = self.jugador.cartas[indice]
                        self.multatk_c2 = copy(self.carta2.mult_ataque)
                        self.multdef_c2 = copy(self.carta2.mult_def)
                        self.carta2.mult_def = 0
                        self.carta2.mult_ataque = 0
        elif self.contador == 1: #Si es que ya se cumplieron los 3 turnos, se devuelven sus valores
            self.carta1.mult_def = self.multdef_c1
            self.carta1.mult_ataque = self.multatk_c1
            self.carta2.mult_def = self.multdef_c2
            self.carta2.mult_ataque = self.multatk_c2
            
            
                

class DeepSheep(InteligenciaArtificial):
    '''
    faltante
    '''
    pass

class Gemibee(InteligenciaArtificial):
    '''
    accede a sus multiplicadores y los aumenta en un 10%
    '''
    def habilidad_especial(self):
        if randint(0, 100) <= self.prob_esp:
            for tipo in range(3):
                for multiplicador in range(2):
                    self.jugador.iamultiplicadores[tipo][multiplicador] * 0.1