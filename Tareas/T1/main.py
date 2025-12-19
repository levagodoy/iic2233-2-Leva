from dccasillas import DCCasillas
from tablero import Tablero
from pathlib import Path
from visualizador import imprimir_tablero

usuario = "UUU"
puntaje = "PPP"
tableros_resueltos = 0
tableros_totales = 0
cargado = False
num_tablero = 0


def menu_inicio():
    print("¡Bienvenido a DCCasillas!")
    print(f'Usuario: {usuario}, Puntaje: {puntaje}')
    print(f'Tableros Resueltos: {tableros_resueltos} de {tableros_totales}')
    print("\n *** Menú de Juego *** \n")
    print("[1] Iniciar juego nuevo \n[2] Continuar Juego \n[3] Guardar estado del juego \n[4] Recuperar estado de juego \n[5] Salir del programa \n")

def menu_acciones(accion_elegida):
    """
    Gestiona el menú de acciones dentro de un tablero específico.

    """
    puntaje = partida.puntaje
    if accion_elegida == "1":
        # Muestra el estado actual del tablero.
        tablero_actual.mostrar_tablero()
    if accion_elegida == "2":
        # Entra al submenú para editar casillas.
        editar_tablero()
    if accion_elegida == "3":
        tablero_actual.validar()
        if tablero_actual.estado == False:
            print("Tu tablero sigue sin resolverse... :c")
        if tablero_actual.estado == True:
            print("Felicidades! haz resuelto tu tablero!")
            partida.puntaje += tablero_actual.movimientos
    if accion_elegida == "4":
        resultado = tablero_actual.encontrar_solucion()
        if resultado != None:
            if resultado == list():
                tablero_actual.mostrar_tablero()
            else:
                resultado.mostrar_tablero()
        else:
            print("\nEl tablero no tiene solucion! :o\n")
    if accion_elegida == "5":
        print("Volviendo al menu de juego.. \n")   
        return
    print("DDCasillas")
    print(f'Usuario: {usuario}, Puntaje: {partida.puntaje}')
    print(f'Número de tablero: {num_tablero} de {tableros_totales}') 
    print(f'Movimientos tablero: {tablero_actual.movimientos}') 
    print("\n *** Menú de Acciones *** \n")
    print("[1] Mostrar tablero \n[2] Habilitar/deshabilitar casillas \n[3] Verificar Solución \n[4] Encontrar Solucion \n[5] Volver al menu de juego \n") #arreglar
    accion_elegida = input("Indique su opcion:")
    if accion_elegida != "5":
        # Llamada recursiva para procesar la siguiente acción.
        return menu_acciones(accion_elegida)
        
def editar_tablero():
    """
    Gestiona la interfaz para modificar una casilla del tablero.

    Esta función es recursiva para permitir al usuario editar múltiples
    casillas sin tener que volver al menú de acciones cada vez.
    """
    print("\nBienvenido al editor de tablero! \n")
    fila = (input("Por favor, ingrese que fila desea editar: \n"))
    columna = (input("Por favor, ingrese que columna desea editar: \n"))
    if fila.isdigit() and columna.isdigit():
        fila = int(fila)
        columna = int(columna)
        # Intenta modificar la casilla usando el método del objeto Tablero.
        if tablero_actual.modificar_casilla(fila, columna) == True:
            print("\n La casilla ha sido modificada con exito!: \n")
            tablero_actual.mostrar_tablero()
            print("\nDeseas continuar editando, o deseas volver?")
            print("\n[1] Deseo continuar")
            print("\n[2] Retornar al menu")
            accion_elegida = input()
            if accion_elegida == "1":
                return editar_tablero()
            if accion_elegida == "2":
                return
            else:
                print("\nError! no selecciona una opcion correcta, volviendo al menu inicial")
                return
        else:
            print("\n Error, la fila o columna no son correctas, por favor, reintente")
            return editar_tablero()
    else:
        print("\n Error, la fila o columna no son correctas, por favor, reintente")
        return editar_tablero()
        

menu_inicio()
opcion_menu_principal = input("Indique su opcion: \n")

while opcion_menu_principal != "5":
    if opcion_menu_principal == "1":
        print("Iniciando nuevo juego...\n")
        usuario_parcial = input("Ingrese su username!:") 
        configuracion = input("Elija que configuracion desea usar (debe terminar en .txt): ")
        path_configuracion = Path("config/"+configuracion)
        # Validación del nombre del archivo.
        if path_configuracion.exists():
            # Crea la instancia principal del juego.
            partida = DCCasillas(usuario_parcial, configuracion)
            # Actualiza las variables globales con los datos de la partida.
            usuario = partida.usuario
            puntaje = partida.puntaje
            tableros_totales = len(partida.tableros)
            tableros_totales -= 1
            cargado = True
            print("\nCargado con exito!\n")
        else:
            print("\nError!, dicho archivo no existe! \n")
            cargado = False
    elif opcion_menu_principal == "2":
        # --- Continuar Juego ---
        if cargado == True:
            if partida.tablero_actual == None:
                # Si no hay un tablero activo, pide al usuario que elija uno.
                num_tablero = int(input(f'Elija el numero de tablero a jugar (puede ser de 0 a {tableros_totales})'))
                if num_tablero in range(tableros_totales):
                    partida.abrir_tablero(num_tablero)
                    accion_elegida = None
                    tablero_actual = partida.tableros[num_tablero]
                    if tablero_actual.estado == True:
                        print("Este tablero ya lo tienes resuelto!, retornando al menú")
                    else:
                        # Inicia el menu de acciones si es que cumple todas las condiciones
                        menu_acciones(accion_elegida)
            else:
                # Si ya hay un tablero activo, pregunta si quiere continuar o cambiar.
                print("Ya tienes un tablero seleccionado")
                print("[1] Continuar con el mismo")
                print("[2] Cambiar de tablero")
                decision = input("Seleccione su opcion")
                if decision == "1":
                    if tablero_actual.estado == True:
                        print("Este tablero ya lo tienes resuelto!, retornando al menú")
                    else:
                        accion_elegida = None
                        menu_acciones(accion_elegida)
                elif decision == "2":
                    # Lógica para cambiar a un nuevo tablero.
                    num_tablero = int(input(f'Elija el numero de tablero a jugar (puede ser de 0 a {tableros_totales-1})'))
                    if num_tablero in range(tableros_totales):
                        partida.abrir_tablero(num_tablero)
                        accion_elegida = None
                        tablero_actual = partida.tableros[num_tablero]
                        if tablero_actual.estado == True:
                            print("Este tablero ya lo tienes resuelto!, retornando al menú")
                        else:
                            print("\nCargado con exito! \n")
                            menu_acciones(accion_elegida)
                else:
                    print("\n Error, tenia que ser 1 o 2... \n ")
        if cargado ==  False:
            print("Error! no se ha seleccionado un usuario")
    elif opcion_menu_principal == "3":
        # --- Guardar Estado del Juego ---
        guardado = partida.guardar_estado()
        if guardado == True:
            print("Juego ha sido guardado con exito!")
        else:
            print("oh oh, algo malo ha pasado :c")
    elif opcion_menu_principal == "4":
        # --- Recuperar Estado del Juego ---
        cargar_partida = partida.recuperar_estado()
        if cargar_partida == True:
            print("Tu juega ha sido recuperado!")
        else:
            print("no existe un archivo con tu username :c")
    else:
        print("opcion invalida :c\n")
    # Al final del bucle, muestra el menú principal de nuevo.
    menu_inicio()
    opcion_menu_principal = input("Indique su opcion: \n")

print("hasta luego o/")    
    

