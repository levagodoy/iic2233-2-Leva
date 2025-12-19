from sys import argv, exit
from jugador import Jugador
from cargar_datos import cargar_ia, cargar_cartas
from guardar_estado import guardar_estado, cargar_estado
from random import randint
from parametros import dinero, COSTO_REROLL, opciones, COSTO_CURAR, COSTO_REVIVIR, ORO_POR_VICTORIA, ORO_POR_RONDA
from copy import deepcopy
from pathlib import Path


# ---INICIACION DEL JUEGO ----
# Se valida que todos los argumentos de entrada sean correctos.

args = argv
if len(args) != 3:
    exit("Error! Debes Ingresar tu Nombre y la dificultad!")

dificultad = args[2]
username = args[1]
rondas = 1

if dificultad not in ["normal", "facil", "dificil"]:
    exit("Dificultad no valida!")

todas_las_cartas = cargar_cartas()
jugador = Jugador(username)

# ---Funciones auxiliares---
def setup_cartas():
    for cartas in todas_las_cartas:
        cartas.dueño = jugador

def ia_randomizer(lista_ias):
    setup_cartas()
    indice = randint(0, len(lista_ias)-1)
    ia_actual = lista_ias[indice]
    lista_ias.pop(indice)
    jugador.lista_ias = lista_ias
    return ia_actual

def cartas_randomizer():
    pool_cartas = []
    numeros_invalidos = []
    while len(pool_cartas) != 5:
        numero = randint(0, 17)
        if numero not in numeros_invalidos:
            carta = deepcopy(todas_las_cartas[numero])
            carta.dueño = jugador
            pool_cartas.append(carta)
            numeros_invalidos.append(numero)
    return pool_cartas

# ---MENUS DE JUEGO---

def menu_inventario():
    """Muestra el inventario y gestiona el movimiento de cartas."""
    print("----------------------------------------")
    print("               Inventario                \n----------------------------------------\n")
    print("Cartas en coleccion:\n")
    for carta in jugador.coleccion:
        print(carta)
    print("\nMazo actual:\n")
    for carta in jugador.cartas:
        print(carta)
    print("\nQue deseas hacer?\n[1] Pasar cartas de mi coleccion al mazo")
    print("[2] Pasar cartas de mi mazo a la coleccion\n[X] Salir del Inventario")
    decision = input()
    if decision == "1":
        if len(jugador.cartas) == 5:
            print("Solo puedes tener un maximo de 5 cartas en tu mazo!")
        else:
            print("Que carta deseas mover de la coleccion?")
            for x in range(len(jugador.coleccion)):
                print(f'[{x}] {jugador.coleccion[x]}')
            cambio = input("Elige tu opcion:")
            if cambio.isdigit():
                if int(cambio) in range(0, len(jugador.coleccion)):
                    cambio = int(cambio)
                    jugador.coleccion_a_mazo(cambio)
                else:
                    print("opcion invalida!")
            else:
                print("Opcion Invalida!")
    elif decision == "2":
        print("Que carta deseas mover de el mazo?")
        for x in range(len(jugador.cartas)):
            print(f'[{x}] {jugador.cartas[x]}')
        cambio = input("Elige tu opcion:")
        if cambio.isdigit():
            if int(cambio) in range(0, len(jugador.cartas)):
                cambio = int(cambio)
                jugador.mazo_a_coleccion(cambio)
            else:
                print("opcion invalida!")
        else:
            print("opcion invalida!")
    elif decision in ["X","x"]:
        return
    else:
        print("Opcion Invalida!")
    return menu_inventario()

def menu_tienda(cartas_ventas, seleccion):
    """Muestra la tienda y procesa las compras o acciones del jugador."""
    print("----------------------------------------")
    print("                 TIENDA                 \n----------------------------------------")
    print(f'Dinero disponible:  {jugador.oro}G\n\nCartas Disponibles:')
    for x in range(len(cartas_ventas)):
        carta = cartas_ventas[x]
        print(f'[{x}] {carta.nombre}............. {carta.precio}G')
    print(f'[6] Curar Carta ({COSTO_CURAR}G)\n[7] Revivir Carta del Cementerio ({COSTO_REVIVIR}G)')
    print(f'[8] Reroll Catalogo (costo {COSTO_REROLL}G)\n[9] Taller (Combinar Cartas)')
    print(f'[X] Volver al menu principal\n')
    seleccion = input(f'Indique su opcion:')
    if seleccion in opciones:
        seleccion = int(seleccion)
        if seleccion < len(cartas_ventas):
            if jugador.oro >= cartas_ventas[seleccion].precio:
                jugador.coleccion.append(cartas_ventas[seleccion])
                jugador.oro -= cartas_ventas[seleccion].precio
                cartas_ventas.pop(seleccion)
                print("Compra exitosa!")
            else:
                print("Error! te falta dinero!")
        else:
            print("Opcion Invalida!")
    if seleccion == "6":
        if jugador.cartas == 0:
            print("Error! solo se pueden curar cartas que esten en tu mazo!")
        else:
            print(f"Que carta deseas curar?: (Recuerda que tiene un costo de {COSTO_CURAR}G)")
            for x in range(len(jugador.cartas)  ):
                print(f'[{x}] {jugador.cartas[x]}')
            print("[0] Ninguna, volver al menu anterior")
            curar_a = int(input())
            if int(curar_a) in range(0,len(jugador.cartas)):
                jugador.cartas[curar_a].vida = jugador.cartas[curar_a].vida_max
                jugador.oro -= 3
            elif curar_a == "0":
                return menu_tienda(cartas_ventas, seleccion)
    elif seleccion == "7":
        if len(jugador.cementerio) > 0:
            for i in range(len(jugador.cementerio)):
                carta = jugador.cementerio[i]
                print([i],carta.nombre)
            revivir = input("Que carta quieres revivir?")
            if jugador.oro > 3:
                carta = jugador.cementerio[int(revivir)]
                jugador.revivir(carta)
            else:
                print("Te falta dinero!")
        else:
            print("No tienes cartas muertas...")
    elif seleccion == "8":
        if jugador.oro >= 3:
            cartas_ventas = cartas_randomizer()
            jugador.oro -= 3
        else:
            print("\nTe falta oro para rerollear! \n")
    elif seleccion == "9":
        menu_taller()
    elif seleccion in ["x","X"]:
        return
    return menu_tienda(cartas_ventas, seleccion)

def combate(ronda):
    """Gestiona el menú pre-combate y la simulación de una ronda."""
    print("----------------------------------------")
    print("        PREPARACION DE RONDA            ")
    print("----------------------------------------")
    print(f"        RONDA ACTUAL: {jugador.ronda}\n")
    print(f'        HP {jugador.iarival.nombre}: {jugador.iarival.vida}/{jugador.iarival.vida_max} \n')
    print(f'[0] Ingresar a la tienda \n[1] Reordenar el inventario')
    print(f'[2] Ingresar a la batalla!\n[9] Abandonar la batalla! :o')
    seleccion = input("Seleccione su opcion:")
    if seleccion == "0":
        cartas_venta = cartas_randomizer()
        menu_tienda(cartas_venta , None)
        return combate(jugador.ronda)
    elif seleccion == "1":
        menu_inventario()
        return combate(jugador.ronda)
    elif seleccion == "9":
        return menu_prinicipal(None)
    elif seleccion == "2":
        print("----------------------------------------")
        print("        SIMULACION DE COMBATE           ")
        print("----------------------------------------")
        jugador.previo_ataque()
        if randint(0,100) <= jugador.iarival.velocidad:
            jugador.recibir_dano()
            jugador.atacar()
        else:
            jugador.atacar()
            jugador.recibir_dano()
        if len(jugador.cartas) == 0:
            print("\n Se han muerto todas las cartas de tu mazo! Perdiste!\n")
            exit()
        if jugador.iarival.vida <= 0:
            print(f"\nFelicidades! le haz ganado a {jugador.iarival.nombre}!")
            print(f'Haz ganado {ORO_POR_VICTORIA}G!')
            jugador.victorias += 1
            if jugador.victorias == jugador.contrincantes:
                print("\n FELICIDADES! o/ \n")
                print("\n HAZ GANADO! \n")
                exit("Hasta luego o/")
            jugador.oro += ORO_POR_VICTORIA
            proxima_ia = ia_randomizer(jugador.lista_ias)
            jugador.iarival = proxima_ia
            proxima_ia.jugador = jugador
            return menu_prinicipal(None)
        else:
            print("El combate continuara!")
            print(f"Haz ganado {ORO_POR_RONDA}G!")
            jugador.oro += ORO_POR_RONDA
            jugador.ronda += 1
            return combate(jugador.ronda)
    else:
        print("Porfavor, selecciona una opcion valida!")
        return combate(jugador.ronda)
    
def menu_taller():
    """Muestra el taller para combinar una carta de tropa con otra."""
    print("----------------------------------------")
    print("                 TALLER                 \n----------------------------------------")
    print("Seleccione con que carta Tropa quiere mezclar:")
    contador = 0
    tropas = []
    for carta in jugador.cartas:
        #Se listan primero las cartas de tipo tropa
        if carta.tipo == "tropa":
            print(f'[{contador}] {carta.nombre}')
            contador += 1
            tropas.append(carta)
    for carta in jugador.coleccion:
        if carta.tipo == "tropa":
            print(f'[{contador}] {carta.nombre}')
            contador += 1
            tropas.append(carta)
    print(f'[X] Retornar al menu')
    indice = input("\nIndique su opcion:")
    if indice in ["X", "x"]:
        return
    elif int(indice) in range(contador):
        indice = int(indice)
        contador2 = 0
        tropa_a_mezclar = tropas[indice]
        posibles_mix = jugador.posibles_mix(tropa_a_mezclar)
        print("\nSus posibles combinaciones son:")
        for match in posibles_mix:
            print(f'[{contador2}] {tropa_a_mezclar.nombre}-{match.nombre}')
            contador2 += 1
        print("[x] Me arrepenti!")
        indice2 = input("\nIndique su opcion:")
        if indice2 in ["X", "x"]:
            return
        elif int(indice2) in range(contador2):
            indice2 = int(indice2)
            jugador.mix(tropas[indice], posibles_mix[indice2])
        else:
            print("Indice erroneo!, volviendo al menu....")



def menu_prinicipal(accion_elegida):
    """Muestra el menú principal y dirige al jugador a otras secciones."""
    print("----------------------------------------")
    print("            MENÚ PRINCIPAL              ")
    print("----------------------------------------")
    print(f'Dinero disponible: {jugador.oro}G')
    print(f'Ronda Actual: {jugador.victorias + 1} de {jugador.contrincantes}')
    print(f'IA Enemiga: {jugador.iarival.nombre}\n')
    print(f'[1] Entrar en combate \n[2] Inventario\n[3] Tienda\n[4] Espiar a la IA')
    print(f'[5] Guardar partida\n[6] Revisar Mazo\n[X] Salir del juego\n')
    print(f'Indique su opcion:')
    accion_elegida = input()
    if accion_elegida == "1":
        if len(jugador.cartas) >= 3:
            return combate(jugador.ronda)
        else:
            print("\nDebes tener un minimo de 3 cartas en tu mazo para entrar en combate!\n")
    elif accion_elegida == "2":
        menu_inventario()
    elif accion_elegida == "3":
        cartas_venta = cartas_randomizer()
        menu_tienda(cartas_venta, None)
    elif accion_elegida == "4":
        ia = jugador.iarival
        print("\n### INFORMARCION IA ACTUAL ###")
        print(f'{ia.nombre}: {ia.vida}/{ia.vida_max}HP | Ataque:{ia.ataque} |\n'
              f'Habilidad:{ia.descripcion}')
    elif accion_elegida == "5":
        guardar_estado(jugador)
        print("\nDeseas continuar jugando?\n[1] Si\n [Cualquier otra tecla] No")
        opcion_salir = input()
        if opcion_salir == "1":
            exit("Hasta luego!")
    elif accion_elegida == "6":
        if len(jugador.cartas) >= 1:
            print("\n---- DESCRIPCION CARTAS ----\n")
            for carta in jugador.cartas:
                carta.presentarse()
                print(f'Habilidad: {carta.descripcion_habilidad}\n')
        else:
            print("\nTu mazo esta vacio!\n")
    elif accion_elegida in ["x","X"]:
        exit("Hasta luego o/")
    else:
        print("\nPor favor seleccione una opcion correcta! \n" )
    return menu_prinicipal(accion_elegida)
        
def iniciar_juego():
    """Configura una nueva partida, incluyendo selección de IA y cartas."""
    lista_ias = cargar_ia(dificultad)
    jugador.contrincantes = len(lista_ias)
    ia_actual = ia_randomizer(lista_ias)
    jugador.iarival = ia_actual
    ia_actual.jugador = jugador
    jugador.oro = dinero[dificultad]
    cartas_por_jugar = cartas_randomizer()
    seleccion = 0
    ("\n### INFORMARCION IA ACTUAL ###")
    print(ia_actual)
    # Bucle para la selección de cartas iniciales.
    while len(jugador.cartas) < 3 or seleccion != 6: 
        print("----------------------------------------")
        print("         SELECCIÓN INICIAL              ")
        print("----------------------------------------")
        for x in range(len(cartas_por_jugar)):
            print(f'[{x+1}] {cartas_por_jugar[x].nombre}')
        print(f'[6] Continuar al Menu Principal')
        print(f'\nTienes actualmente {len(jugador.cartas)} cartas elegida(s), debes seleccionar'
              f'entre 3-5 cartas!')
        seleccion = input(f"Por favor, selecciona tu carta! \n" )
        if seleccion.isdigit():
            seleccion = int(seleccion)
            if seleccion != 6:
                if seleccion <= len(cartas_por_jugar):
                    jugador.cartas.append(cartas_por_jugar[seleccion-1])
                    cartas_por_jugar.pop(seleccion-1)
                else:
                    print("opcion invalida!")
            if seleccion == 6:
                if len(jugador.cartas) >= 3:
                    return menu_prinicipal(None)
                else:
                    print("Error!, Debes elegir al menos 3 cartas")


# ---FLUJO INICIAL ---
#   Revisa si es que ya existe un save file con el nombre del usuario
save_file = Path(username+".txt")
if save_file.exists():
    print("Ya existe una partida guardada a tu nombre. Deseas cargarla?")
    print("[1] Si\n[Cualquier otra tecla] No")
    opcion = input()
    if opcion == "1":
        cargar_estado(jugador)
        menu_prinicipal(None)
    else:
        iniciar_juego() 
else:
    iniciar_juego()


