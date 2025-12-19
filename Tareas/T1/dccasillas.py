from tablero import Tablero
from pathlib import Path


class DCCasillas:
    def __init__(self, usuario:str, config:str) -> None:
        self.usuario = usuario
        self.puntaje = 0
        self.tablero_actual = None
        path_configuracion = Path("config/"+config) # Se crea un path absoluto #
        with path_configuracion.open(mode="r", encoding= "utf-8") as archivo_tableros:
            #se guardan toda su contenido en la variable tableros
            tableros = archivo_tableros.readlines() 
        for x in range(len(tableros)): 
            tableros[x] = tableros[x].strip("\n") 
            if x != 0:
                nuevo_tablero = Tablero() #Se crea una nueva instancia de tablero
                nuevo_tablero.cargar_tablero(tableros[x]) #Se guarda su informacion
                tableros[x] =  nuevo_tablero #Se guarda en la lista de tableros
        self.juegos_totales = int(tableros.pop(0)) #Se sustrae el primer valor(Numero de juegos totales)
        self.tableros = tableros 

    def abrir_tablero(self, num_tablero:int) -> None:
        """Establece el indice de tablero a jugar"""
        self.tablero_actual = num_tablero

    def guardar_estado(self) -> bool:
        """
        Guarda el estado actual del juego en un archivo.

        El estado incluye el número total de juegos y los detalles
        de cada tablero (movimientos, dimensiones y disposición).

        Retorna un bool dependiendo del exito del guardado
        """
        path_save = Path("data/"+self.usuario+".txt")
        with path_save.open(mode="w", encoding= "utf-8") as save_file:
            print(self.juegos_totales, file=save_file)
            for tablero in self.tableros:
                #Se guardan las 3 variables por separados#
                columnas = tablero.columnas
                filas = tablero.filas
                movimientos = tablero.movimientos
                print(movimientos, file = save_file) #Se escribe primero el numero de movimientos
                print(filas, columnas, file = save_file) #Luego el total de filas y columnas
                for indice_fila in range(filas+1):
                    fila_actual = "" #Reiniciamos el contenido de la fila
                    for indice_columna in range(columnas+1): #Guardamos cada contenido de la fila
                        if indice_columna == 0:
                            fila_actual = tablero.tablero[indice_fila][indice_columna] 
                        else:
                            fila_actual = f'{fila_actual} {tablero.tablero[indice_fila][indice_columna]}'
                    print(fila_actual, file=save_file)
        return True

    def recuperar_estado(self) -> bool:
        """
        Recupera un estado de juego guardado desde un archivo.

        Retorna un bool dependiendo si fue exitosa o no la operación
        """
        path_save = Path("data/"+self.usuario+".txt") #Creamos un path con el nombre del usuario.
        if path_save.exists(): #Si es que dicho path existe, entonces:
            with path_save.open(mode='r', encoding='utf-8') as archivo: 
                self.juegos_totales = int(archivo.readline()) 
                self.tableros = [] #Reiniciamos la variable tableros
                self.puntaje = 0 #Se reinicia el puntaje
                for x in range(self.juegos_totales):
                    nuevo_tablero = Tablero() #Se crea una nueva instancia de tablero
                    nuevo_tablero.movimientos = archivo.readline() #La segunda linea siempre seran los movimiento
                    self.puntaje += int(nuevo_tablero.movimientos)
                    indices = archivo.readline()
                    indices = indices.strip("\n")
                    indices = indices.split(" ")
                    nuevo_tablero.filas = int(indices[0]) +1
                    nuevo_tablero.columnas  = int(indices[1]) +1
                    nuevo_tablero.tablero = []
                    for y in range(nuevo_tablero.filas):
                        fila_actual = archivo.readline()
                        fila_actual = fila_actual.strip("\n")
                        fila_actual = fila_actual.split(" ")
                        nuevo_tablero.tablero.append(fila_actual)
                    self.tableros.append(nuevo_tablero)
            return True
        else:
            return False
        

    