from visualizador import imprimir_tablero
from pathlib import Path
from copy import deepcopy #Se requiere para poder copiar la informacion de los tableros

class Tablero:

    def __init__(self) -> None:
        """Inicializa un nuevo objeto Tablero con valores por defecto."""
        self.tablero = []
        self.copia_tablero = []
        self.movimientos = 0 
        self.estado = False # ¿Se encuentra resuelto?
        self.filas = 0
        self.columnas = 0


    def cargar_tablero(self, archivo:str) -> None:
        path_archivo = Path("config/"+archivo)
        with path_archivo.open(mode='r', encoding= "utf-8") as archivo_tablero:
            tablero = archivo_tablero.readlines()
        # Limpia y divide cada linea para formar el tablero
        for x in range(len(tablero)):
            tablero[x] = tablero[x].strip("\n")
            tablero[x] = tablero[x].split(" ")
        
        # Extrae las dimensiones de la primera línea y la elimina
        self.filas = int(tablero[0][0])
        self.columnas = int(tablero[0][1])
        tablero.pop(0)
        
        # Guarda dos copias de tablero, una para ser utilizada en encontrar_solucion()
        self.tablero = tablero
        self.copia_tablero = deepcopy(self.tablero)
        
    def mostrar_tablero(self) -> None:
        """Imprime el estado actual del tablero en la consola."""
        tablero = self.tablero
        imprimir_tablero(tablero)

    def modificar_casilla(self, fila:int, columna:int) -> bool:
        """
        Modifica el estado de una casilla numérica entre 'marcada' y 'no marcada'.

        Una casilla 'marcada' se prefija con una 'X'. Esto se usa para
        excluir su valor de las sumas de validación. No se pueden
        modificar casillas vacías ('.').
        """
        if type(fila) == int and type(columna) is int:
            if self.filas > fila and self.columnas > columna:
                casilla = self.tablero[fila][columna]
                if casilla != ".": #Solo modifica casillas con numeros
                    if "X" in casilla:
                        casilla = casilla.strip("X")
                    else:
                        casilla = "X"+casilla
                    self.tablero[fila][columna] = casilla
                    self.movimientos += 1
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def validar(self) -> bool:
        """
        Verifica si el estado actual del tablero es una solución válida.

        Comprueba que la suma de los números no marcados ('X') en cada fila
        y columna coincida con el valor de la casilla objetivo.
        """
        #Valida si es que se cumple la condicion en esa columna
        for x in range(self.filas): 
            valor_esperado = self.tablero[x][self.columnas]
            suma_total = 0
            if valor_esperado != ".":
                valor_esperado = int(valor_esperado)
                for y in range(self.columnas):
                    casilla = self.tablero[x][y]
                    if casilla != "." and casilla[0] != "X": #Se suman todas las casillas de esa fila
                        casilla = int(casilla)
                        suma_total += casilla
                if valor_esperado != suma_total:
                    return False
        #Valida si es que se cumple la condicion en esa fila
        for x in range(self.columnas): 
            valor_esperado = self.tablero[self.filas][x]
            if valor_esperado != ".":
                valor_esperado = int(valor_esperado)
                suma_total = 0
                for y in range(self.filas):
                    casilla = self.tablero[y][x]
                    if casilla != "." and casilla[0] != "X":
                        casilla = int(casilla)
                        suma_total += casilla
                if valor_esperado != suma_total:
                    return False
        self.estado = True
        return True

    def encontrar_solucion(self):
        """
        Busca una solución para el tablero actual usando backtracking.

        Este método gestiona el estado del tablero antes y después de llamar
        al método recursivo 'resolver_tablero'.Si es que ya estaba previamente resuelto,
        devuelve su mismo tablero. Si es que resolver_tablero() encuentra una solucion, devuelve
        una instancia de otro Tablero() con el tablero resuelto. Si es que no se encuentra ninguna
        solucion, devuelve False.
        """
        if self.validar():
            return self.tablero
        copia_tablero = deepcopy(self.tablero)
        self.tablero = deepcopy(self.copia_tablero)
        movimientos_previos = deepcopy(self.movimientos) #se guardan los movimientos previos
        if self.resolver_tablero(0, 0):
            self.movimientos = movimientos_previos #se recuperan los movimientos previos
            self.copia_tablero = deepcopy(self.tablero) #se guarda el tablero resuelto
            self.tablero = copia_tablero #se recupera el tablero original
            self.estado = False
            tablero_resuelto = Tablero()
            tablero_resuelto.tablero = self.copia_tablero
            return tablero_resuelto
        self.copia_tablero = deepcopy(self.tablero)
        self.tablero = copia_tablero
        self.movimientos = movimientos_previos
        return None
  
    def resolver_tablero(self, fila:int, columna:int) -> bool:
        #Si es que el tablero ya está resuelto, 
        if self.validar():
            return True
        #Si es que ya acabo el tablero, debe devolverse ya que no está resuelto
        if fila == self.filas and columna == self.columnas:
            if self.validar():
                return True
            return False
        #Si es que llego a la columna final, reinicia su contador y suma uno a la fila
        if columna == self.columnas:
            fila += 1
            columna = 0
        #Si es que la casilla no es numero, avanza de columna
        if self.tablero[fila][columna] == ".":
            return self.resolver_tablero(fila, columna +1)
        else:
        # Inicia modificando la casilla seleccionada, si es que validar_movimiento == False,
        # La vuelve a su estado original. En ambos casos luego de ejecutar dicha movida, se inicia
        # nuevamente la funcion ahora una columna por delante
            self.modificar_casilla(fila, columna)
            if self.validar_movimiento(fila, columna):
                if self.resolver_tablero(fila, columna +1):
                    return True
            self.modificar_casilla(fila, columna)
            if self.resolver_tablero(fila, columna +1):
                return True
        return False
        

    def validar_movimiento(self, fila:int, columna:int) -> bool:
        """Verifica si es que las casillas objetivos de la columna y fila
        correspondiente son menores a la suma total de sus respectivas columnas o filas.
        Si es que es menor, significa que el tablero ya no tiene resolucion, devolviendo False.

        Args:
            fila (int): Indice de fila actual.
            columna (int): Indice de columna actual.

        Returns:
            bool: Aun puede ser resuelto o no.
        """
        valor_esperado_row = self.tablero[fila][self.columnas]
        valor_esperado_col = self.tablero[self.filas][columna]
        #validar su columna
        if valor_esperado_col != ".":
            valor_esperado_col = int(valor_esperado_col)
            suma_total = 0
            for x in range(self.filas):
                casilla = self.tablero[x][columna]
                if casilla != "." and casilla[0] != "X":
                    casilla = int(casilla)
                    suma_total += casilla
            if suma_total < valor_esperado_col:
                return False
        #validar su fila    
        if valor_esperado_row != ".":
            valor_esperado_row = int(valor_esperado_row)
            suma_total = 0
            for x in range(self.columnas):
                casilla = self.tablero[fila][x]
                if casilla != "." and casilla[0] != "X":
                    casilla = int(casilla)
                    suma_total += casilla
            if suma_total < valor_esperado_row:
                return False
        return True
        
    