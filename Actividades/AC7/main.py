from collections import defaultdict, deque
from typing import Optional

import pandas as pd
import numpy as np
import re


def cargar_sismos(path_archivo: str) -> pd.DataFrame:
    '''
    Lee el contenido del archivo entregado y lo transforma en un
    DataFrame compuesto de 7 campos (Fecha y hora local, Magnitud Ms,
    Magnitud Mw, Profundidad, Efecto, Coordenadas, Ubicación), donde 
    - 'Fecha y hora local' es un objeto de tipo datetime
    - 'Ubicación' es una lista de strings
    '''
    # TODO: Parte I
    
    info_archivo = []
    
    with open(path_archivo, 'r', encoding='utf-8') as csv:
        next(csv)
        for linea in csv:
            linea = linea.strip().split(',')
            fecha = pd.to_datetime(linea[0])
            ubicacion = linea[6].split(";")
            info = {
                "Fecha y hora local" : fecha,
                "Magnitud Ms" : linea[1],
                "Magnitud Mw" : linea[2],
                "Profundidad" : linea[3],
                "Efecto" : linea[4],
                "Coordenadas" : linea[5],
                "Ubicación" : ubicacion
            }
            info_archivo.append(info)
            
    df = pd.DataFrame.from_dict(info_archivo)
            
    return df


def filtrar_sismos_magnitud(df: pd.DataFrame, magnitud: float,
                            operacion: Optional[str] = '>') -> pd.DataFrame:
    '''
    Recibe un DataFrame y filtra todos los sismos que su ``Magnitud Ms'' cumpla
    la magnitud y operación recibidas como input.
    '''
    df['Magnitud Ms'] = df['Magnitud Ms'].astype(float)
    if operacion == ">":
        top = df[df['Magnitud Ms'] > magnitud]
    elif operacion == "<":
        top = df[df['Magnitud Ms'] < magnitud]
    elif operacion == "=":
        top = df[df['Magnitud Ms'] == magnitud]
    return top


def estadisticas_efectos(df: pd.DataFrame) -> pd.Series:
    '''
    Recibe un DataFrame y obtiene el porcentaje correspondiente a
    los distintos tipos de Efecto que puede tener un Sismo.
    '''
    
    total_sismos = len(df)
    
    
    proporciones = df.groupby('Efecto')['Fecha y hora local'].count() / total_sismos
    return proporciones*100
    
    


def crear_grafo_ubicaciones(df: pd.DataFrame) -> dict[set]:
    '''
    Recibe un DataFrame y retorna un grafo formado a partir de
    la información contenida en la columna 'Ubicación'.
    '''
    grafo = defaultdict(set)
    
    for ubicaciones in df['Ubicacion']:
        for i in range(len(ubicaciones) - 1):
            nodo_origen = ubicaciones[i]
            nodo_destino = ubicaciones[i+1]
            
            grafo[nodo_origen].add(nodo_destino)
            
            if nodo_destino not in grafo:
                grafo[nodo_destino] = set()

    return grafo
def ubicacion_tuvo_sismo_mar(grafo: dict[set], ubicacion: str) -> bool:
    '''
    Recibe un grafo representado mediante un diccionario de adyacencia, y
    una ubicación correspondiente a uno de los nodos de dicho grafo.
    Retorna un booleano que indica si desde dicha ubicación ha presentado
    sismos en el mar.
    '''
    # Vamos a mantener una lista con los nodos visitados.
    visitados = []
    # La cola de siempre, comienza desde el nodo inicio.
    queue = deque([grafo['Chile']])

    while len(queue) > 0:
        # Elegimos el siguiente nodo a visitar de la cola
        vertice = queue.popleft()
        # Detalle clave: si ya visitamos el nodo, no hacemos nada!
        if vertice in visitados:
            continue
        
        # Lo visitamos
        visitados.append(vertice)
        # Agregamos los vecinos a la cola si es que no han sido visitados.
        for vecino in grafo[vertice]:
            if vecino not in visitados:
                queue.append(vecino)
    if ubicacion not in visitados:
        return False
    else:
        return


def limpiar_header_corrompido(header: str) -> str:
    '''
    Recibe un texto corrompido y elimina todos los elementos correspondiente a
    la corrupción. 
    '''
    patron_combinado = r'\d+|[!#$%&?*+]|[A-Z]{2,}'
    
    header = re.sub(patron_combinado, "", header)
    
    return header


if __name__ == '__main__':
    path_sismos = 'sismos.csv'

    print('\nParte I: Cargar la información')
    df_sismos = cargar_sismos(path_sismos)
    print(df_sismos.head(5))

    print('\nParte II: Consultas Sismos')
    input('Aprieta ENTER para continuar')

    print('\nFiltrar Sismos por magnitud')
    print(filtrar_sismos_magnitud(df_sismos, 8.0, '>'))

    print('\nEstadísticas de los Efectos de los Sismos')
    print(estadisticas_efectos(df_sismos))

    print('\nParte III: Grafo de ubicaciones')
    input('Aprieta ENTER para continuar')

    print('\nGrafo')
    grafo_ubicaciones = crear_grafo_ubicaciones(df_sismos)
    print(grafo_ubicaciones)

    print('\nRevisar si ubicaciones han tenido Sismos en el Mar')
    input('Aprieta ENTER para continuar')
    print('Magallanes:', ubicacion_tuvo_sismo_mar(grafo_ubicaciones, 'Magallanes'))
    print('Tamarugal:', ubicacion_tuvo_sismo_mar(grafo_ubicaciones, 'Tamarugal'))
    print('Chile:', ubicacion_tuvo_sismo_mar(grafo_ubicaciones, 'Chile'))
    print('Metropolitana:', ubicacion_tuvo_sismo_mar(grafo_ubicaciones, 'Metropolitana'))


    print('\nParte IV: Repara el Header corrompido usando Regex')
    input('Aprieta ENTER para continuar')
    header_corrompido = '*+1Fe321chaKSNM234 y ho32%%&#$ra loc?#a432lOIJSN'
    header_reparado = limpiar_header_corrompido(header_corrompido)
    print('- Original:', header_corrompido)
    print('- Reparado:', header_reparado)
