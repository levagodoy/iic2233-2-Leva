from parametros import (ARCHIVO_CARTAS, ARCHIVO_MULTIPLICADORES, Multiplicador_Carta_Est, 
                        Multiplicador_Carta_Mix, Multiplicador_Carta_Trp, Multiplicadores,
                        ARCHIVO_IAS_FACIL, ARCHIVO_IAS_NORMAL, ARCHIVO_IAS_DIFICIL,
                        )
from parametros_diccionario import nombre_tropas, nombre_estructuras, nombre_ias


def descompositor(linea:str):
    '''
    Recibe un string de tipo info1,info2,info3,...
    y lo devuelve como una lista [info1,info2,info3,...]
    '''
    linea_final = []
    seccion = ""
    en_comillas = False
    linea = linea + "," # Se añade una coma para asegurar que el último elemento sea procesado
    for caracter in linea:
        if caracter == '"':
            # Invierte el estado de en_comillas cada vez que se encuentra una comilla
            if en_comillas == False:
                en_comillas = True
            else: 
                en_comillas = False
        elif caracter == "," and en_comillas == False: 
            # Si se encuentra una coma y no está dentro de comillas, se añade la sección.
            linea_final.append(seccion)
            seccion = ""
        else:
            seccion += caracter
    #elimina el /n de la ultima seccion
    linea_final[len(linea_final)-1] = linea_final[len(linea_final)-1].strip("\n")
    return linea_final

def cargar_cartas():
    '''
    Carga todas las cartas del archivo cartas.csv, devuelve
    una lista que contanga la informacion de todas las cartas
    '''
    cuenta = 0
    lista_cartas = []
    with open(ARCHIVO_CARTAS, "r", encoding="utf-8") as datos_cartas:
        for info_carta in datos_cartas:
            cuenta += 1
            carta = []
            if cuenta > 1:  # Omitir la cabecera del archivo.
                carta = descompositor(info_carta)
                if len(carta) > 4:
                    tipo = carta[1]
                    nombre = carta[0]
                    if tipo == "tropa":
                        carta_esperada = nombre_tropas[nombre]
                        carta_n = carta_esperada(carta[0], int(carta[2]), carta[1], float(carta[3]), 
                                                int(carta[4]), float(carta[5]), int(carta[6]), 
                                                float(carta[7]), carta[8])
                        lista_cartas.append(carta_n)
                    elif tipo == "estructura":
                        carta_esperada = nombre_estructuras[nombre]
                        carta_n = carta_esperada(carta[0], int(carta[2]), carta[1], float(carta[3]), 
                                                int(carta[4]), float(carta[5]), carta[8])
                        lista_cartas.append(carta_n)
    
    return lista_cartas

def cargar_multiplicadores():
    '''
    Carga todos los multiplicadores de multiplicadores.csv
    
    Devuelve un diccionario de multiplicadores, el cual contiene
    tuplas nombradas de cada multiplicador por IA, y cada multiplicador
    por individual tambien es una tupla nombrada
    '''
    multiplicadores = {}
    multiplicadores_temp = []
    ia_actual = None
    with open(ARCHIVO_MULTIPLICADORES, "r", encoding="utf-8") as datos_multiplicadores:
        for multiplicador in datos_multiplicadores:
            multiplicador = multiplicador.split(",")
            #detecta si se te revisando una nueva IA
            if ia_actual != multiplicador[0]:
                if len(multiplicadores_temp) == 3:
                    #Crea una tupla nombrada con la info de todos los multiplicadores
                    multiplicador_nuevo = Multiplicadores(multiplicadores_temp[0],
                                                          multiplicadores_temp[1],
                                                          multiplicadores_temp[2])
                    multiplicadores[ia_actual] = multiplicador_nuevo
                    multiplicadores_temp = []
                    ia_actual = multiplicador[0]
                ia_actual = multiplicador[0]
            #Omite la cabecera
            if multiplicador[0] != "ia_nombre":
                if multiplicador[1] == "tropa":
                    multiplicador_tropa = Multiplicador_Carta_Trp(float(multiplicador[2]),
                                                                  float(multiplicador[3]))
                    multiplicadores_temp.append(multiplicador_tropa)
                elif multiplicador[1] == "estructura":
                    multiplicador_estructura = Multiplicador_Carta_Est(float(multiplicador[2]),
                                                                       float(multiplicador[3]))
                    multiplicadores_temp.append(multiplicador_estructura)
                elif multiplicador[1] == "mixta":
                    multiplicador_mixta = Multiplicador_Carta_Mix(float(multiplicador[2]), 
                                                                  float(multiplicador[3]))
                    multiplicadores_temp.append(multiplicador_mixta)
    #Se repite para la ultima IA
    multiplicador_nuevo = Multiplicadores(multiplicadores_temp[0],
                                          multiplicadores_temp[1],
                                          multiplicadores_temp[2])
    multiplicadores[ia_actual] = multiplicador_nuevo
    return multiplicadores

def cargar_ia(dificultad:str):
    '''
    Carga el archivo de la ia correspondiente a la dificultad entregada
    '''
    archivo = ""
    lista_ia = []
    cuenta = 0
    #selecciona el archivo correcto en base a la dificultad entregada
    if dificultad == "facil":
        archivo = ARCHIVO_IAS_FACIL
    elif dificultad == "normal":
        archivo = ARCHIVO_IAS_NORMAL
    elif dificultad == "dificil":
        archivo = ARCHIVO_IAS_DIFICIL
    with open(archivo, "r", encoding="utf-8") as archivo_ias:
        for ias in archivo_ias:
            cuenta += 1
            linea = []
            if cuenta > 1:
                linea = descompositor(ias)
                ia_esperada = nombre_ias[linea[0]]
                nueva_ia = ia_esperada(linea[0], int(linea[1]), int(linea[2]), linea[3], 
                                       float(linea[4]), float(linea[5]))
                lista_ia.append(nueva_ia)
    
    return lista_ia


