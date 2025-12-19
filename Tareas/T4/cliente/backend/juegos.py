import sys

from PyQt5.QtCore import QObject, pyqtSignal, QMutex
from backend.networking import Cliente


class Juegos(QObject):
    senal_username_cargado = pyqtSignal(bool)
    senal_mostar_vp = pyqtSignal(str, int)
    senal_abrir_juego = pyqtSignal(str)
    senal_error = pyqtSignal()
    senal_actualizar_cartas = pyqtSignal(dict)
    senal_desconexion = pyqtSignal()
    senal_turno_blackjack = pyqtSignal()
    senal_asientos = pyqtSignal(dict)
    senal_revelar_cartas = pyqtSignal(list) 
    senal_enviar_carta = pyqtSignal(dict)

    def __init__(self, host: str, port: int):
        super().__init__()
        
        self.mutex = QMutex()
        
        self.cliente = Cliente(host, port)
        self.cliente.start()
        
        self.username = None
        self.balance = None
        self.juego_actual = None
        
        self.cliente.senal_username.connect(self.info_username)
        self.cliente.senal_juego.connect(self.abrir_juego)
        self.cliente.senal_desconexion.connect(self.senal_desconexion.emit)
        self.cliente.senal_turno_blackjack.connect(self.senal_turno_blackjack.emit)
        self.cliente.senal_asientos.connect(self.senal_asientos.emit)
        self.cliente.senal_actualizar_cartas.connect(self.senal_actualizar_cartas.emit)
        self.cliente.senal_revelar_cartas.connect(self.senal_revelar_cartas.emit)
        self.cliente.senal_enviar_carta.connect(self.senal_enviar_carta.emit)

    #Funciones globales
    
    def info_username(self, info: bool, balance: int):
        '''
        Revisa si es que el username esta disponible, si es que pudo carga sus datos
        '''
        if info == True:
            self.username = self.potencial_username
            self.balance = balance
            
            self.senal_username_cargado.emit(True)
            self.senal_mostar_vp.emit(self.username, self.balance)
        elif info == False:
            self.senal_username_cargado.emit(False)
    
    
    def enviar_username(self, username: str):
        '''
        Envia su username al servidor
        '''
        self.potencial_username = username
        
        self.cliente.enviar_mensaje({
            'comando': 'Informacion',
            'username': username
        })
    
    def unirse_juegos(self, juego: str):
        '''
        Se une a un juego
        '''
        self.cliente.enviar_mensaje({
            'comando': 'Conectarse',
            'id_juego': juego}
        )
        
    def actualizar_balance(self, earning: int):
        '''
        Actualiza el balance del usuario
        '''
        self.balance += earning
        
        self.cliente.enviar_mensaje({
            'comando': 'cargar',
            'earnings': earning
        })
        
    def abrir_juego(self, bul: bool,juego:str):
        '''
        Ve si se puede abrir el juego
        '''
        if bul:
            self.juego_actual = juego
            self.senal_abrir_juego.emit(juego)
        else:
            self.senal_error.emit()
        
    def apostar(self, monto):
        '''
        Envia la apuesta al servidor
        '''
        self.balance -= monto
        self.cliente.enviar_mensaje({
            'comando': 'apostar',
            'monto': monto
        })
    
    def recibir_resultados(self):
        pass
    
    def ultimas_ganancias(self):
        '''
        Solicita las ultimas 5 ganancias de los juegos
        '''
        self.cliente.enviar_mensaje({
            'comando': 'solicitar'
        })

    #Funciones BJ
    def pedir_carta(self):
        self.cliente.enviar_mensaje({
            'comando': 'pedir_carta'
        })
    
    def plantarse(self):
        self.cliente.enviar_mensaje({
            'comando': 'plantarse'
        })
