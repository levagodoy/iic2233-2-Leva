from typing import Generator, List, Tuple
from math import pi
from itertools import tee, islice, product
from datetime import datetime
from collections import defaultdict

from utilidades import (
    Astronauta,
    Nave,
    Tripulacion,
    Planeta,
    Mineral,
    PlanetaMineral,
    Mision,
    MisionMineral,
    radio_planeta
)


# Cargas 

#Todas las cargas tienen la misma estructura
def cargar_astronautas(path: str) -> Generator[Astronauta, None, None]:
    with open(path, 'r', encoding = "UTF-8") as astronautas:
        next(astronautas) # salta la cabecera
        for linea in astronautas:
            id_astronauta , nombre, estado = linea.strip('\n').split(",")
            yield Astronauta(int(id_astronauta), nombre, estado)

def cargar_naves(path: str) -> Generator[Nave, None, None]:
    with open(path, 'r', encoding = "UTF-8") as naves:
        next(naves) # salta la cabecera
        for linea in naves:
            info = linea.strip('\n').split(",")
            yield Nave(info[0], info[1], info[2], int(info[3]), float(info[4]),
                       float(info[5]))

def cargar_tripulaciones(path: str) -> Generator[Tripulacion, None, None]:
    with open(path, 'r', encoding = "UTF-8") as tripulaciones:
        next(tripulaciones) # salta la cabecera
        for linea in tripulaciones:
            info = linea.strip('\n').split(",")
            yield Tripulacion(int(info[0]), info[1], int(info[2]), int(info[3]))

def cargar_planetas(path: str) -> Generator[Planeta, None, None]:
    with open(path, 'r', encoding = "UTF-8") as planetas:
        next(planetas) # salta la cabecera
        for linea in planetas:
            info = linea.strip('\n').split(",")
            yield Planeta(int(info[0]), info[1], float(info[2]), float(info[3]), info[4], info[5])

def cargar_minerales(path: str) -> Generator[Mineral, None, None]:
    with open(path, 'r', encoding = "UTF-8") as minerales:
        next(minerales) # salta la cabecera
        for linea in minerales:
            info = linea.strip('\n').split(",")
            yield Mineral(int(info[0]), info[1], info[2], int(info[3]), float(info[4]))

def cargar_planeta_minerales(path: str) -> Generator[PlanetaMineral, None, None]:
    with open(path, 'r', encoding = "UTF-8") as planeta_mineral:
        next(planeta_mineral) # salta la cabecera
        for linea in planeta_mineral:
            info = linea.strip('\n').split(",")
            yield PlanetaMineral(int(info[0]), int(info[1]), float(info[2]), float(info[3]))

def cargar_mision(path: str) -> Generator[Mision, None, None]:
    with open(path, 'r', encoding = "UTF-8") as misiones:
        next(misiones) # salta la cabecera
        for linea in misiones:
            info = linea.strip('\n').split(",")
            if info[5] == "True":
                info[5] = True
            elif info[5] == "False":
                info[5] = False
            else:
                info[5] = None
            yield Mision(int(info[0]), info[1], info[2], int(info[3]), int(info[4]), info[5])

def cargar_materiales_mision(path: str) -> Generator[MisionMineral, None, None]:
    with open(path, 'r', encoding = "UTF-8") as mision_mineral:
        next(mision_mineral) # salta la cabecera
        for linea in mision_mineral:
            info = linea.strip('\n').split(",")
            yield MisionMineral(int(info[0]), int(info[1]), float(info[2]))


# Consultas 1 generador

def naves_de_material(generador_naves: Generator[Nave, None, None], 
                      material: str) -> Generator[Nave, None, None]:
    #Solo filtra por tipo de material
    return filter(lambda nave: nave.material == material, generador_naves)


def misiones_desde_fecha(generador_misiones: Generator[Mision, None, None], 
                         fecha: str, inverso: bool) -> Generator[Mision, None, None]:
    ano, mes, dia = fecha.split("-") #Se guardan todos los valores por individual
    ano = int(ano) ; mes = int(mes) ; dia = int(dia)
    fecha = datetime(ano, mes, dia) #Se crea un objeto de datetime con la fecha
    for mision in generador_misiones:
        #Misma estructura que arriba, se descompone la fecha por cada mision, y se transforma
        #a datetime. Luego, dependiendo si es que es inverso o no, se devuelve la mision
        ano_mision, mes_mision, dia_mision = mision.fecha.split("-")
        ano_mision = int(ano_mision) ; mes_mision = int(mes_mision) ; dia_mision = int(dia_mision)
        fecha_mision = datetime(ano_mision, mes_mision, dia_mision) 
        if inverso:
            if fecha_mision <= fecha:
                yield mision
        else:
            if fecha_mision >= fecha:
                yield mision
            

def naves_por_intervalo_carga(generador_naves: Generator[Nave, None, None], 
                              cargas: tuple[float, float]) -> Generator[Nave, None, None]:
    #solo filtra por tipo de carga
    return filter(lambda nave: cargas[0] <= nave.capacidad_minerales <= cargas[1] <= cargas[1],
                  generador_naves)

def planetas_con_cantidad_de_minerales(generador_planeta_mineral: Generator[PlanetaMineral, None, 
                                                                            None], 
                                       id_mineral: int, cantidad_minima: int) -> List[int]:
    '''
    Filtra por minerales y luego por la cantidad minima, guarda todos los planetas filtrados en una
    lista que devuelve
    '''
    planetas_con_minerales = filter(lambda planeta: planeta.id_mineral == id_mineral, 
                                    generador_planeta_mineral)
    planetas_filtrados = filter(lambda planeta: planeta.cantidad_disponible * planeta.pureza >= cantidad_minima,
                                planetas_con_minerales)
    lista = []
    for planeta in planetas_filtrados:
        lista.append(planeta.id_planeta)
    return lista

## PENDIENTE ##
def naves_astronautas_rango(generador_tripulacion: Generator[Tripulacion, None, None], 
                            rango: int, 
                            minimo_astronautas: int) -> Generator[Tuple[str, Generator], None, None]:
    gen1, gen2 = tee(generador_tripulacion)
    filtro = filter(lambda trip: trip.rango >= rango, gen1)
    filtro, filtro2 = tee(filtro)
    
    for tripulacion in filtro2:
        hola = filter(lambda trip: trip.id_equipo == tripulacion.id_equipo, filtro)
        hola = map(lambda trip: trip.id_astronauta, hola)
        yield (tripulacion.patente_nave, hola)
## PENDIENTE ##

def cambiar_rango_astronauta(generador_tripulacion: Generator[Tripulacion, None, None], 
                             id_astronauta: int, 
                             rango_astronauta: int) -> Generator[Tripulacion, None, None]:
    id = id_astronauta #Se reenombran las variables para que quedan en el minimo de lineas
    rank = rango_astronauta
    #Se entregan los astronautas con su nuevo rango
    return map(lambda ast: ast._replace(rango = rank) if ast.id_astronauta == id else ast,
               generador_tripulacion)

def encontrar_planetas_cercanos(generador_planetas: Generator[Planeta, None, None], x1: int, 
                                y1: int, x2: int, y2: int, 
                                cantidad: int | None = None) -> Generator[Planeta, None, None]:
    #Filtra por coordenadas de planetas, y luego por la cantidad maxima a devolver
    planetas = filter(lambda planeta: x1 <= planeta.coordenada_x <= x2,
                      generador_planetas)
    planetas = filter(lambda planeta: y1 <= planeta.coordenada_y <= y2,
                      planetas)
    if cantidad != None:
        #Solo devuelve la cantidad dada
        return islice(planetas, cantidad)
    else:
        #Retorna todos los filtrados
        return planetas
 
# Consultas 2 generadores

def disponibilidad_por_planeta(generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                               generador_planetas: Generator[Planeta, None, None], 
                               id_mineral: int) -> Generator[Tuple[str, int, float], None, None]:
    '''
    Se crea un defaultdict con un diccionario de argumento, asi, se puede guardar por multiples
    llaves, lo que resulta util para almacenar la cantidad_disponible de cada planeta mineral
    '''
    disponibilidad = defaultdict(dict)
    for pm in generador_planeta_mineral:
        disponibilidad[pm.id_planeta][pm.id_mineral] = pm.cantidad_disponible

    for planeta in generador_planetas:
        #Se usa .get para evitar problemas con KeyErrors
        cantidad = disponibilidad.get(planeta.id_planeta, {}) 
        cantidad = cantidad.get(id_mineral, 0.0)
        yield planeta.nombre, planeta.id_planeta, cantidad


def misiones_por_tipo_planeta(generador_misiones: Generator[Mision, None, None],
                              generador_planetas: Generator[Planeta, None, None], 
                              tipo: str) -> Generator[Mision, None, None]:
    filtro_planetas = filter(lambda planeta: planeta.tipo == tipo,
                             generador_planetas) #Se filtra por tipo
    filtro_misiones = filter(lambda mision: mision.lograda != None,
                             generador_misiones) #Se filtra a solo misiones que se hayan realizado
    gen2 = product(filtro_planetas, filtro_misiones) #Se crea una tupla de generadores
    pares_filtrados = filter(lambda par: par[0].id_planeta == par[1].id_planeta,
                  gen2) #Se mantienen solo los generadores que comparte su id_planeta
    return map(lambda par: par[1], pares_filtrados) #Solo se devuelven las misiones

def naves_pueden_llevar(generador_naves: Generator[Nave, None, None], 
                        generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                        id_planeta: int) -> Generator[tuple[str, int, float], None, None]:
    minerales_del_planeta = {} #Diccionario para guardar la cantidad disponible por mineral
    for pm in generador_planeta_mineral:
        if pm.id_planeta == id_planeta:
            minerales_del_planeta[pm.id_mineral] = pm.cantidad_disponible

    for nave in generador_naves:
        for mineral_id, cantidad_disponible in minerales_del_planeta.items():
            #Si es que excede el maximo, se lleva el 100%
            if nave.capacidad_minerales >= cantidad_disponible: 
                yield nave.patente, mineral_id, 100.0
            else:
                porcentaje = nave.capacidad_minerales * 100 / cantidad_disponible
                yield nave.patente, mineral_id, porcentaje
        
# Consultas 3 generadores

def planetas_por_estadisticas(generador_mineral: Generator[Mineral, None, None], 
                              generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                              generador_planeta: Generator[Planeta, None, None], 
                              moles_elemento_min: int,
                              concentracion_molar_min: int, 
                              densidad_min: int) -> Generator[Planeta, None, None]:
    info_minerales = {} #Diccionario para guardar cada masa_atomica por mineral
    for mineral in generador_mineral:
        info_minerales[mineral.id_mineral] = mineral.masa_atomica
        #Default dict para guardar los minerales, su cantidad por planeta
    planeta_mineral = defaultdict(dict) 
    for pm in generador_planeta_mineral:
        planeta_mineral[pm.id_planeta][pm.id_mineral] = pm.cantidad_disponible * pm.pureza * 10 **6
    for planeta in generador_planeta:
        radio = radio_planeta(planeta.id_planeta, planeta.tamano) #Se calcula el radio del planeta
        volumen = (4/3) * pi * radio ** 3 #Su volumen en base a la formula entregada
        minerales = planeta_mineral.get(planeta.id_planeta, {}) #.get para evitar keyerror
        for mineral, cantidad in minerales.items():
            moles = cantidad / info_minerales[mineral] #Se calculan los moles en base a la info
            if moles >= moles_elemento_min: #Filtros en base a los entregados
                densidad = cantidad / volumen
                if densidad >= densidad_min:
                    concentracion = cantidad / (volumen * info_minerales[mineral])
                    if concentracion >= concentracion_molar_min:
                        yield planeta
                        break

def ganancias_potenciales_por_planeta(generador_minerales: Generator[Mineral, None, None], 
                                      generador_planeta_mineral: Generator[PlanetaMineral, 
                                                                           None, None],
                                      generador_planetas: Generator[Planeta, None, None],
                                      precios: dict) -> dict:
    #Se filtran los minerales en base a los dados en los diccionarios
    minerales_filtrados = filter(lambda min: min.nombre in precios,
                                 generador_minerales) 
    id_a_nombre = {} #Diccionario para almacenar su precio en base a su id
    for mineral in minerales_filtrados:
        id_a_nombre[mineral.id_mineral] = precios[mineral.nombre]
    planeta_mineral = defaultdict(dict) #ddict para guardar la cantidad de mineral por planeta
    for pm in generador_planeta_mineral:
        planeta_mineral[pm.id_planeta][pm.id_mineral] = pm.cantidad_disponible * pm.pureza
    valores = {} #Diccionario que almacena el valor por planeta
    for planeta in generador_planetas:
        valor_potencial = 0
        #Accede a todos los minerales del planeta
        minerales = planeta_mineral.get(planeta.id_planeta, {}) 
        for mineral, cantidad in minerales.items():
            precio = id_a_nombre.get(mineral, 0) #Accede a su precio
            valor_potencial += precio * cantidad
        valores[planeta.id_planeta] = valor_potencial
    return valores
        
def planetas_visitados_por_nave(generador_planetas: Generator[Planeta, None, None], 
                                generador_misiones: Generator[Mision, None, None], 
                                generador_tripulaciones: Generator[Tripulacion, None, None]):
    planetas = {} #Diccionario que guarda todos los nombres de los planetas
    for planeta in generador_planetas:
        planetas[planeta.id_planeta] = planeta.nombre
    misiones = defaultdict(set) #ddict que contiene a todas los planetas visitados por equipo
    for mision in generador_misiones:
        if mision.lograda != None:
            misiones[mision.id_equipo].add(mision.id_planeta)
    tripulaciones = {} #Guarda el id del equipo por patente de las naves
    for tripulacion in generador_tripulaciones:
        tripulaciones[tripulacion.patente_nave] = tripulacion.id_equipo
    for patente, id in tripulaciones.items():
        planetas_tripulacion = misiones.get(id, set())
        if planetas_tripulacion == set(): #Si es que el equipo no ha visitado nada:
            yield (patente, None, None)
        else:
            for id_planeta in planetas_tripulacion:
                yield (patente, planetas[id_planeta], id_planeta)

def mineral_por_nave(generador_tripulaciones: Generator[Tripulacion, None, None], 
                     generador_misiones: Generator[Mision, None, None], 
                     generador_misiones_mineral: Generator[MisionMineral, None, None]):
    generador_misiones = filter(lambda mision: mision.lograda ==True,
                                        generador_misiones) #Filtro a solo misiones logradas
    misiones = defaultdict(dict) #ddict que guarda la cantidad total recolectada por tripulacion
    minerales = {} #dict de cantidad obtenida por mision
    for mm in generador_misiones_mineral:
        cantidad1= minerales.get(mm.id_mision, 0)
        minerales[mm.id_mision] = mm.cantidad + cantidad1
    for mision in generador_misiones:
        cantidad1 = minerales.get(mision.id_mision, 0)
        cantidad2 = misiones.get(mision.id_equipo, {}).get(mision.id_mision, 0)
        misiones[mision.id_equipo][mision.id_mision] = cantidad1 + cantidad2
    patentes = {} #dict que guarda los id de equipos por patentes
    for tripulacion in generador_tripulaciones:
        patentes[tripulacion.patente_nave] = tripulacion.id_equipo
    for patente in patentes:
        cantidades = misiones.get(patentes[patente], {})
        total = 0
        if cantidades != {}:
            for cantidad in cantidades.values(): #Calcula el total obtenido
                total += cantidad
        yield patente, total

def porcentaje_extraccion(generador_tripulacion: Generator[Tripulacion, None, None], 
                          generador_mision_mineral: Generator[MisionMineral, None, None], 
                          generador_planeta_mineral: Generator[PlanetaMineral, None, None], 
                          mision : Mision) -> Tuple[float, float]:
    if mision.lograda != True: #Si es que la mision nunca fue realizada, entonces su valor es 0.0
        return 0.0, 0.0
    tripulantes = 0
    for tripulacion in generador_tripulacion:
        if tripulacion.id_equipo == mision.id_equipo:
            tripulantes += 1 #numero total de tripulantes
    cantidad_mision = 0 #total de la cantidad recolectada
    minerales = [] #lista con todos los id de minerales
    for mm in generador_mision_mineral:
        if mision.id_mision == mm.id_mision:
            cantidad_mision += mm.cantidad #suma cada mision
            minerales.append(mm.id_mineral) #se agrega el id del mineral
    cantidad_planeta = 0 #cantidad total de minerales del planeta
    for pm in generador_planeta_mineral:
        if pm.id_planeta == mision.id_planeta and pm.id_mineral in minerales:
            cantidad_planeta += pm.cantidad_disponible * pm.pureza
    total = cantidad_mision * 100 / cantidad_planeta #se calcula el % de recoleccion del planeta
    total_tripulantes = total / tripulantes #% por total de tripulantes
    return total, total_tripulantes    

# Consultas 4 generadores

def resultado_mision(mision: Mision, generador_naves: Generator[Nave, None, None], 
                     generador_planeta_mineral: Generator[PlanetaMineral, None, None],
                     generador_tripulaciones: Generator[Tripulacion, None, None], 
                     generador_mision_mineral: Generator[MisionMineral, None, None]) -> Mision:
    for tripulacion in generador_tripulaciones:
        if tripulacion.id_equipo == mision.id_equipo:
            patente = tripulacion.patente_nave #Si es que accede a la patente, se guarda
            break
    minerales_requerido = 0
    gatochico_requerido = 0
    minerales = [] #lista que contiene todos los id de minerales requeridos
    for mm in generador_mision_mineral:
        if mm.id_mision == mision.id_mision:
            if mm.id_mineral == 1:
                gatochico_requerido += mm.cantidad #Se suma el gatochico requerido
            else:
                minerales_requerido += mm.cantidad #Se suma el total de cantidades
                minerales.append(mm.id_mineral)
    capacidad_mineral = 0
    for nave in generador_naves:
        if nave.patente == patente:
            capacidad_mineral = nave.capacidad_minerales
            break #Se guarda ahora la capacidad por nave, en base a la patente previamente guardada
    total_minerales = 0 #Total de minerales en el planeta
    total_gatochico = 0 #total de gatochico en el planeta
    #loop para guardar el total de cantidades por minerales del planeta
    for pm in generador_planeta_mineral:
        if pm.id_planeta == mision.id_planeta:
            if pm.id_mineral == 1: #Si es que el planeta contiene gatochico:
                total_gatochico = pm.cantidad_disponible * pm.pureza
            elif pm.id_mineral in minerales:
                total_minerales += pm.cantidad_disponible * pm.pureza
    if gatochico_requerido > 0: #si es que se requiere gatochico y puede llevarlo todo:
        if total_gatochico >= gatochico_requerido and total_gatochico <= capacidad_mineral:
            return mision._replace(lograda = True)
    #si es que puede llevar todo el resto de los minerales:
    elif total_minerales >= minerales_requerido and total_minerales <= capacidad_mineral:
        return mision._replace(lograda = True)
    return mision._replace(lograda = False)
