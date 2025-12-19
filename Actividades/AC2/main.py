from collections import namedtuple
from pathlib import Path
from os.path import join
from utilidades import Anime  # IMPORTANT: Debes utilizar esta nametupled


#####################################
#       Parte I - Cargar datos      #
#####################################
def cargar_animes(ruta_archivo: str) -> list:
    path = Path(ruta_archivo)
    with path.open(mode = 'r', encoding = 'UTF-8') as archivo:
        archivo_animes = archivo.readlines()
    cantidad_animes = len(archivo_animes)
    animes = []
    for x in range(cantidad_animes):
        archivo_animes[x] = archivo_animes[x].strip("\n")
        archivo_animes[x] = archivo_animes[x].split(",")
        archivo_animes[x][5] = archivo_animes[x][5].split(";")
        archivo_animes[x][5] = set(archivo_animes[x][5])
        anime1 = Anime(archivo_animes[x][0], int(archivo_animes[x][1]), int(archivo_animes[x][2]), int(archivo_animes[x][3]), archivo_animes[x][4], archivo_animes[x][5])
        animes.append(anime1)
    return animes


#####################################
#        Parte II - Consultas       #
#####################################
def animes_por_estreno(animes: list) -> dict:
    estrenos = {}
    for x in range(len(animes)):
        anios_estrenos = animes[x][3]
        estrenos[anios_estrenos] = [animes[x][0]]
    return estrenos


def descartar_animes(generos_descartados: set, animes: list) -> list:
    animes_finales = []
    for x in range(len(animes)):
        if animes[x][5] not in generos_descartados:
            animes_finales.append(animes[x][0])
    return animes_finales


def resumen_animes_por_ver(*animes: Anime) -> dict:
    puntajes = []
    capitulos_totales = 0
    puntajes_suma = 0
    generos = set()
    puntaje_promedio = 0
    for x in range(len(animes)):
        puntaje = animes[x][2]
        capitulos_totales += animes[x][1]
        for genero in animes[x][5]:
            generos.add(genero)
        puntajes.append(puntaje)
    for x in range(len(puntajes)):
        puntajes_suma += puntajes[x]
    if len(puntajes) != 0:
        puntaje_promedio = round(puntajes_suma / len(puntajes), 1)
    animes_por_ver = {
        "puntaje promedio": puntaje_promedio,
        "capitulos total": capitulos_totales,
        "generos": set(generos)
    }
    return animes_por_ver


def estudios_con_genero(genero: str, **estudios: dict) -> list:
    estudios_con_el_genero = []
    for x in estudios.keys():
        for y in estudios[x]:
            if genero in y[5]:
                if x not in estudios_con_el_genero:
                    estudios_con_el_genero.append(x)
    return estudios_con_el_genero


if __name__ == "__main__":
    #####################################
    #       Parte I - Cargar datos      #
    #####################################
    animes = cargar_animes(join("data", "ejemplo.chan"))
    indice = 0
    for anime in animes:
       print(f"{indice} - {anime}")
       indice += 1

    #####################################
    #        Parte II - Consultas       #
    #####################################
    # Solo se usará los 2 animes del enunciado.
    datos = [
        Anime(
            nombre="Hunter x Hunter",
            capitulos=62,
            puntaje=9,
            estreno=1999,
            estudio="Nippon Animation",
            generos={"Aventura", "Comedia", "Shonen", "Acción"},
        ),
        Anime(
            nombre="Sakura Card Captor",
            capitulos=70,
            puntaje=10,
            estreno=1998,
            estudio="Madhouse",
            generos={"Shoujo", "Comedia", "Romance", "Acción"},
        ),
    ]

    # animes_por_estreno
    estrenos = animes_por_estreno(datos)
    print(estrenos)

    # descartar_animes
    animes = descartar_animes({"Comedia", "Horror"}, datos)
    print(animes)

    # resumen_animes_por_ver
    resumen = resumen_animes_por_ver(datos[0], datos[1])
    print(resumen)

    # estudios_con_genero
    estudios = estudios_con_genero(
        "Shonen",
        Nippon_Animation=[datos[0]],
        Madhouse=[datos[1]],
    )
    print(estudios)
