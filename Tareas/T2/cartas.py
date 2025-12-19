from abc import ABC, abstractmethod
from random import randint
from parametros import (CURE_PEPPA, DEF_CAB, PROB_LARRY_GOD, 
                        PROB_LARRY_MID, PROB_BARB, POWER_UP_BARB,
                        PROB_FIRE, PROB_GLOBO, DANO_BOMBA, DIE_PROB,
                        PROB_LAPIDA, COSTO_COMBINACION)
from copy import copy

class Carta(ABC):
    
    def __init__(self, nombre = str, maxhp = int, tipo = str, defx = float, precio = int, probesp = int, descripcion = str):
        self.nombre = nombre
        self.vida_max = maxhp
        self.vida = maxhp
        self.mult_def = defx
        self.precio = precio
        self.prob_especial = probesp
        self.tipo = tipo
        self.descripcion_habilidad = descripcion
        self._dueño = None #Guarda como atributo el jugador actual, asi poder acceder
                            #atributos o metodos
        self.mult_ataque = 0
        self.ataque = 0
    
    @property
    def dueño(self):
        pass
    
    @dueño.getter
    def dueño(self):
        return self._dueño
    
    @dueño.setter
    def dueño(self, jugador): 
        self._dueño = jugador
    
    def recibir_daño(self, atk:int):
        dano = round(atk * self.mult_def) 
        self.vida -= dano
        print(f"{self.nombre} ha recibido {atk} de daño!. Su vida ahora esta en {self.vida}/{self.vida_max}HP!")
    
    def atacar(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass
    
    '''
    Se termino por hacer las habilidad especiales en base a cuando las activan
    (previo al ataque, posterior a un ataque enemigo/aliado o posterior a su
    muerte), haciendo asi más simple la manera de llamarlas y observar su comportamiento.
    Si es que es necesario ir al margen de la letra del enunciado, era posible
    crear cada habilidad en un metodo usar_habilidad() y luego hacer que se llame
    en el momento indicado, sin embargo eso parecia un desperdicio de espacio,
    por el cual termino conservando esta forma.
    '''
    
    def presentarse(self):
        print(self)
    
    def previo_ataque(self): #Todas las habilidad que se activan previo a una ronda de combate
        pass
    
    def post_ataque_aliado(self, dano): #Todas las habilidades que se activen posterior a un ataque
        pass
    
    def post_ataque_enemigo(self, obj): #Todas las habilidades que se activen posterior a un ataque
        pass
    
    def postumo(self): #Todas las habilidades que se activen posterior a la muerte de la carta
        pass
  
class Carta_Tropa(Carta):
    
    def __init__(self, nombre=str, maxhp=int, tipo=str, defx=float, precio=int, 
                 probesp=int, atk = int, atkx = int, descripcion = str):
        super().__init__(nombre, maxhp, tipo, defx, precio, probesp, descripcion)
        self.ataque = atk #tiene dos nuevos atributos, ataque y su multiplicador de ataque
        self.mult_ataque = atkx
        
    def atacar(self): #Solo esta carta realmente ataca, por el cual solo ella tendra este metodo
        dano = round(self.ataque * self.mult_ataque)
        return dano
    
    def __str__(self):
        return f'{self.nombre} ({self.tipo}): {self.vida}/{self.vida_max} HP, Ataque: {self.ataque}'

##############################
#######  CARTAS TROPAS #######
##############################

class Duende(Carta_Tropa):
    def post_ataque_aliado(self, dano):
        self.dueño.oro += round(dano * 0.5) #aumenta el oro en 0.5 del dano hecho

class PEPPA(Carta_Tropa):
    def post_ataque_aliado(self, dano): #Se cura por el 0.5 de su vida
        cura = round(CURE_PEPPA*self.vida_max)
        self.vida +=cura
        if self.vida > self.vida_max:
            self.vida = self.vida_max

class Montapatos(Carta_Tropa):
    #Cambia la velocidad de la IA a 0, y vuelve a ser su valor original luego
    #de cada ataque
    def previo_ataque(self):
        self.velocidad_previa = copy(self.dueño.iarival.velocidad)
        self.dueño.iarival.velocidad = 0
    
    def post_ataque_aliado(self, dano):
        self.dueño.iarival.velocidad = self.velocidad_previa

class Antimuros(Carta_Tropa):
    #esta carta se mata luego de atacar
    def post_ataque_aliado(self, dano):
        self.vida = 0

class Caballero(Carta_Tropa):
    #aumenta su defensa en def_cab cada ronda que este viva
    def previo_ataque(self):
        for cartas in self.dueño.cartas:
            cartas.mult_def += round(cartas.mult_def * DEF_CAB)

class Maldecidor(Carta_Tropa):
    #devuelve la mitad del daño que le hagan
    def post_ataque_enemigo(self, obj):
        dano_retorno = round(obj * 0.5)
        return dano_retorno

class Esqueletos(Carta_Tropa):
    '''
    "Tiene una probabilidad PROB_LARRY_GOD % de causar cinco veces su daño
    base y una probabilidad PROB_LARRY_MID % de morir instantáneamente al
    recibir un ataque (incluso si el daño de la IA es menor que la vida de la
    carta)."
    '''
    def post_ataque_aliado(self, dano):
        dano_retorno = 0
        if PROB_LARRY_GOD >= randint(1, 100):
            dano_retorno = dano * 4
            dano_retorno = round(dano_retorno * self.dueño.iamultiplicadores[0][1])
            self.dueño.iarival.recibir_dano(dano_retorno)
        if PROB_LARRY_MID >= randint(1, 100):
            self.vida = 0
        
class Barbaros(Carta_Tropa):
    #Por cada vez que es atacado y sobrevive, aumenta su daño en POWER_UP_BARB
    def post_ataque_enemigo(self, obj):
        if randint(0, 100) <= PROB_BARB:
            self.ataque = round(POWER_UP_BARB*self.ataque)

class Espiritu_Igneo(Carta_Tropa):
    #Tiene una posibilidad de anular el daño recibido
    def post_ataque_enemigo(self, obj):
        if randint(0, 100) <= PROB_FIRE:
            self.vida += round(obj / self.mult_def)
            
class Globo(Carta_Tropa):
    #Si es que muere, ejerce DANO_BOMBA en la ia rival
    def postumo(self):
        if randint(0, 100) <= PROB_GLOBO:
            self.dueño.iarival.recibir_dano(DANO_BOMBA)
        
##############################
#### FIN CARTAS TROPAS #######
##############################

class Carta_Estructura(Carta):
    
    def __init__(self, nombre=str, maxhp=int, tipo=str, defx=float, 
                 precio=int, probesp=int, descripcion = str):
        super().__init__(nombre, maxhp, tipo, defx, precio, probesp, descripcion)

    def __str__(self):
        return f'{self.nombre} ({self.tipo}): {self.vida}/{self.vida_max} HP'

##############################
####  CARTAS ESTRUCTURAS #####
##############################

class Canon(Carta_Estructura):
    #Faltante
    def pasivas(self):
        return super().pasivas()

class TorreDIE(Carta_Estructura):
    '''
    Si es que los aliados atacan primero, la IA no hará daño esa ronda
    '''
    def previo_ataque(self):
        self.contador = 0
    
    def post_ataque_aliado(self, dano):
        if self.contador == 0:
            if randint(0, 100) <= DIE_PROB:
                self.copiaatk = copy(self.dueño.iarival.ataque)
                self.dueño.iarival.ataque = 0
                self.contador += 1
    
    def post_ataque_enemigo(self, obj):
        if self.contador == 1:
            self.dueño.iarival.ataque = self.copiaatk
        else:
            self.contador += 1

class Recolector(Carta_Estructura):
    ## FALTANTE ##
    def postumo(self):
        return super().postumo()

class Horno(Carta_Estructura): 
    def postumo(self): #Si es que esta carta muere, se reemplaza por Espíritu Ígneo
        if len(self.dueño.cartas) >= 1:
            for carta in self.dueño.todas_cartas:
                if carta.nombre == "Espíritu Ígneo":
                    self.dueño.cartas.append(carta)
                    break

class Lapida(Carta_Estructura):
    def post_ataque_enemigo(self, obj): 
        if randint(0, 100) <= PROB_LAPIDA:
            self.vida += round(obj / self.mult_def) #Anula el daño recibido

class CuartelBarbaros(Carta_Estructura):
    def postumo(self): #Si es que esta carta muere, se reemplaza por Barbaros
        if len(self.dueño.cartas) >= 1:
            for carta in self.dueño.todas_cartas:
                if carta.nombre == "Bárbaros":
                    self.dueño.cartas.append(carta)
                    break

class TorreBomba(Carta_Estructura):
    def postumo(self): #Si es que esta carta muere, ejerce DANO_BOMBA en la ia rival
        self.dueño.iarival.recibir_dano(DANO_BOMBA)

class CuartelDuendes(Carta_Estructura):
    def postumo(self): #Si es que esta carta muere, se remplaza por Duendes
        if len(self.dueño.cartas) >= 1:
            for carta in self.dueño.todas_cartas:
                if carta.nombre == "Duendes":
                    self.dueño.cartas.append(carta)
                    break


##############################
### FIN CARTAS ESTRUCTURAS ###
##############################

class Carta_Mixta(Carta_Tropa, Carta_Estructura):
    def __init__(self, Carta1 = Carta_Tropa, Carta2 = Carta_Estructura):
        self.carta1 = copy(Carta1) #Se crean copias de las cartas, por si estas terminando siendo editadas a futuro
        self.carta2 = copy(Carta2) 
        self.nombre = Carta1.nombre + "-" + Carta2.nombre 
        self.vida_max = Carta1.vida_max + Carta2.vida_max #Su vida max es una suma de las otras vidas
        self.vida = copy(self.vida_max) 
        self.mult_def = round(Carta1.mult_def + Carta2.mult_def/ 2, 2)
        self.prob_especial = round(Carta1.prob_especial + Carta2.prob_especial/ 2, 2)
        self.tipo = "mixta"
        self.descripcion_habilidad = Carta1.descripcion_habilidad + "/" + Carta2.descripcion_habilidad
        self._dueño = Carta1.dueño
        self.ataque = Carta1.ataque
        self.mult_ataque = Carta1.mult_ataque
        
    def atacar(self):
        #Ya que tiene atributos de ataque, puede atacar
        dano = round(self.ataque * self.mult_ataque)
        return dano
    
    '''
    Activa las habilidades por etapa de ambas de sus cartas
    heredadas.
    '''
    
    def previo_ataque(self):
        self.carta1.previo_ataque()
        self.carta2.previo_ataque()
    
    def post_ataque(self, dano, obj):
        self.carta1.post_ataque(dano, obj)
        self.carta2.post_ataque(dano, obj)  

    def postumo(self):
        self.carta1.postumo()
        self.carta2.postumo()



