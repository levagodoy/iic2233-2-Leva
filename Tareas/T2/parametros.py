from collections import namedtuple

# Archivo de parámetros para DCCardMaster

DINERO_INICIAL_FACIL = 30
DINERO_INICIAL_NORMAL = 20
DINERO_INICIAL_DIFICIL = 15
ORO_POR_VICTORIA = 20
ORO_POR_RONDA = 5
COSTO_CURAR = 3
COSTO_REVIVIR = 1.5
COSTO_REROLL = 3
COSTO_COMBINACION = 5
MAX_CARTAS_MAZO = 5
CURE_PEPPA = 0.05
DEF_CAB = 0.10
CANNON_ABILITY = 20
DIE_PROB = 10
PROB_LARRY_GOD = 15
PROB_LARRY_MID = 20
PROB_BARB = 30
POWER_UP_BARB = 0.15
PROB_FIRE = 25
PROB_GLOBO = 40
DANO_BOMBA = 100
PROB_LAPIDA = 35

# Paths a los archivos de datos
import os

# Directorio base de datos
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Archivo de cartas
ARCHIVO_CARTAS = os.path.join(DATA_DIR, 'cartas.csv')

# Archivos de IAs por dificultad
ARCHIVO_IAS_FACIL = os.path.join(DATA_DIR, 'ias_facil.csv')
ARCHIVO_IAS_NORMAL = os.path.join(DATA_DIR, 'ias_normal.csv')
ARCHIVO_IAS_DIFICIL = os.path.join(DATA_DIR, 'ias_dificil.csv')

# Archivo de multiplicadores
ARCHIVO_MULTIPLICADORES = os.path.join(DATA_DIR, 'multiplicadores.csv')

#Tupla de multiplicadores

Multiplicador_Carta_Trp = namedtuple("Tropas", ["ataque", "defensa"])
Multiplicador_Carta_Est = namedtuple("Estructuras", ["ataque", "defensa"])
Multiplicador_Carta_Mix = namedtuple("Mixto", ["ataque", "defensa"])

Multiplicadores = namedtuple("multiplicadores",["Tropas", "Estructuras", "Mixto"])

#Diccionario de valores

dinero = {"facil": DINERO_INICIAL_FACIL,
          "normal": DINERO_INICIAL_NORMAL,
          "dificil": DINERO_INICIAL_DIFICIL}

#Listado pool
opciones = ["0","1", "2", "3", "4"]