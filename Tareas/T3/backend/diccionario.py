from backend.consultas import (cargar_astronautas, cargar_naves, cargar_planetas, cargar_tripulaciones,
                       cargar_materiales_mision, cargar_minerales, cargar_mision,
                       cargar_planeta_minerales)

#Diccionario que administra cada funcion en base a la entidad a cargar
consulta = {'Astronauta': cargar_astronautas,
            'Nave': cargar_naves,
            'Planeta': cargar_planetas,
            'Tripulación': cargar_tripulaciones,
            'Mineral': cargar_minerales,
            'PlanetaMineral': cargar_planeta_minerales,
            'Mision': cargar_mision,
            'MisionMineral': cargar_materiales_mision}