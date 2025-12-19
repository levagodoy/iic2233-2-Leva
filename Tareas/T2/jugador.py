from cargar_datos import cargar_cartas, cargar_ia, cargar_multiplicadores
from cartas import Carta_Mixta
from parametros import COSTO_COMBINACION

diccionario_multiplicadores = cargar_multiplicadores()

class Jugador():
    
    def __init__(self, nombre):
        self.nombre = nombre
        self.todas_cartas = cargar_cartas()
        self.lista_ias = []
        self.cementerio = []
        self.cartas = [] #Mazo activo
        self.coleccion = []
        self.oro = 0
        self.victorias = 0
        self.contrincantes = 0
        self.ronda = 0
        self._iarival = None #Se guarda la ia activa como un atributo
        self.iamultiplicadores = None #Se guardan los multiplicadores de dicha IA
    
    @property
    def iarival(self):
        pass
    
    @iarival.getter
    def iarival(self):
        return self._iarival
    
    @iarival.setter
    def iarival(self, nuevaia): #Si es que se cambia el atributo de IA 
                                #se cambian tambien sus multiplicadores
        self._iarival = nuevaia
        self.iamultiplicadores = diccionario_multiplicadores[nuevaia.nombre]
    
    def coleccion_a_mazo(self, carta): #Se cambian las cartas de la coleccion al mazo
        carta = self.coleccion.pop(carta)
        self.cartas.append(carta)
    
    def mazo_a_coleccion(self, carta): #Se cambian las cartas del mazo a la coleccion
        carta = self.cartas.pop(carta)
        self.coleccion.append(carta)
    
    def previo_ataque(self): #Se ejecutan todas las habilidades previas al ataque
        for carta in self.cartas:
            carta.previo_ataque()
        self.iarival.habilidad_especial()
    
    def atacar(self):
        ataque_total = 0
        for cartas in self.cartas:
            if cartas.tipo == "tropa" or cartas.tipo == "mixta":
                if cartas.atacar() != 0: #Si es que alguna carta tiene su ataque modificado,
                                        #entonces tampoco ataca
                    ataque_total += round(cartas.atacar() * self.iamultiplicadores[0][1])
                    cartas.post_ataque_aliado(cartas.ataque)
        self.iarival.recibir_dano(ataque_total)
    
    def dano_efectivo(self, dano:int):
        """
        Recibe el daño inicial, y retorna el daño efectivo en base a
        la formula de ataque_total/(n_estructuras + (n_mixtas)
        """
        contador = 0
        for carta in self.cartas:
            if carta.tipo == "estructura" or carta.tipo == "mixta":
                contador += 1
        if contador > 0:
            dano = round(dano / contador)
        return dano

    def recibir_dano(self):
        dano = self.iarival.atacar()
        dano = self.dano_efectivo(dano) #Se modifica el valor del daño a el daño efectivo
        estructuras = 0
        for carta in self.cartas: #Reciben primero daño las estructuras
            if carta.tipo == "estructura":
                dano = round(dano * self.iamultiplicadores[1][0]) #Aumenta en base al multiplicador
                carta.recibir_daño(dano)
                estructuras += 1
            elif carta.tipo == "mixta": 
                dano = round(dano * self.iamultiplicadores[2][0]) #Aumenta en base al multiplicador
                carta.recibir_daño(dano)
                estructuras += 1
        if estructuras == 0: #No hay estructuras en el mazo
            for carta in self.cartas:
                dano = round(dano * self.iamultiplicadores[0][0]) #Aumenta en base al multiplicador
                carta.recibir_daño(dano)
        return self.check_muertos() #Luego de cada ataque enemigo, se revisa si murio alguna carta
    
    def check_muertos(self):
        if len(self.cartas) == 0: #Si es que ya no quedan cartas en el mazo, se pierde el juego
            print("Todas las cartas han muerto! Hemos perdido!")
            return 
        cartas_vivas = [] 
        for carta in self.cartas:
            if carta.vida <= 0:
                print(f'La carta {carta.nombre} ha muerto! x_x')
                carta.vida = 0
                carta.postumo() #Se activan las habilidades postumas
                self.cementerio.append(carta)
            else:
                cartas_vivas.append(carta)
        self.cartas = cartas_vivas
    
    def mix(self, carta_1, carta_2):
        """
        Debido a que se pueden mezclar cartas de la coleccion con otras
        del mazo, se debe primero checkear en que lista estan, dando asi tantas
        condiciones
        """
        carta_3 = Carta_Mixta(carta_1, carta_2)
        self.cartas.append(carta_3)
        if carta_1 in self.cartas:
            self.cartas.remove(carta_1)
        elif carta_1 in self.coleccion:
            self.coleccion.remove(carta_1)
        if carta_2 in self.cartas:
            self.cartas.remove(carta_2)
        elif carta_2 in self.coleccion:
            self.coleccion.remove(carta_2)
        self.oro -= COSTO_COMBINACION
        return 
    
    def posibles_mix(self, carta):
        #Se revisa todos los posibles mixes de alguna carta, la cual siempre sera de tipo tropa
        posibles_mix = []
        if carta.tipo == "tropa":
            for carta in self.cartas:
                if carta.tipo == "estructura":
                    posibles_mix.append(carta)
            for carta in self.coleccion:
                if carta.tipo == "estructura":
                    posibles_mix.append(carta)
        return posibles_mix


    def revivir(self, carta): #Se revive la carta seleccionada y se devuelve a la coleccion
        self.cementerio.remove(carta)
        carta.vida = carta.vida_max
        self.coleccion.append(carta)
    
    def presentarse(self):
        print(self)
    
    def __str__(self):
        mensaje = f'Jugador: {self.nombre} \n'
        mensaje = mensaje + f'Peleas Ganadas: {self.victorias}/{self.contrincantes} \n'
        mensaje = mensaje + f'Cartas en coleccion: \n'
        for cartas in self.cartas:
            carta = str(cartas)
            mensaje = mensaje+carta+"\n"
        return mensaje

