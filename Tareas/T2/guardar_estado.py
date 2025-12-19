from cargar_datos import descompositor, cargar_cartas
from parametros_diccionario import nombre_tropas, nombre_estructuras, nombre_ias
from cartas import Carta_Mixta

def guardar_estado(jugador):
    '''
    Guarda el estado el juego con el mismo formato que los archivos
    originales, asi pudiendo reutilizar descompositor()
    
    Args:
    instancia de objeto Jugador()
    '''  
    archivo = f'{jugador.nombre}.txt'
    ia_actual = jugador.iarival
    cartas = jugador.cartas
    with open(archivo, "w", encoding="utf-8") as save_file:
        print(f'### Info jugador ###', file = save_file) 
        print(f'{jugador.oro},{jugador.victorias},{jugador.contrincantes}', file = save_file)
        print(f'### COLECCION ###', file = save_file)
        for carta in jugador.coleccion:
            if carta.tipo != "mixta":
                  print(f'{carta.nombre},{carta.tipo},{carta.vida_max},{carta.mult_def},{carta.precio},'
                        f'{carta.prob_especial},{carta.ataque},{carta.mult_ataque},'
                        f'"{carta.descripcion_habilidad}",{carta.vida}',
                        file = save_file)
            else:
                  print(f'{carta.nombre},{carta.tipo},{carta.carta1.nombre},{carta.carta2.nombre},'
                        f'{carta.vida}',
                        file = save_file)
        print(f'### MAZO ###', file = save_file)
        for carta in cartas:
            if carta.tipo != "mixta":
                  print(f'{carta.nombre},{carta.tipo},{carta.vida_max},{carta.mult_def},{carta.precio},'
                        f'{carta.prob_especial},{carta.ataque},{carta.mult_ataque},'
                        f'"{carta.descripcion_habilidad}",{carta.vida}',
                        file = save_file)
            else:
                  print(f'{carta.nombre},{carta.tipo},{carta.carta1.nombre},{carta.carta2.nombre},'
                        f'{carta.vida}',
                        file = save_file)
        print(f'### CEMENTERIO ###',file = save_file)
        for carta in jugador.cementerio:
            if carta.tipo != "mixta":
                  print(f'{carta.nombre},{carta.tipo},{carta.vida_max},{carta.mult_def},{carta.precio},'
                        f'{carta.prob_especial},{carta.ataque},{carta.mult_ataque},'
                        f'"{carta.descripcion_habilidad}",{carta.vida}',
                        file = save_file)
            else:
                  print(f'{carta.nombre},{carta.tipo},{carta.carta1.nombre},{carta.carta2.nombre},'
                        f'{carta.vida}',
                        file = save_file)
        print(f'### LISTA IA ###',file = save_file)
        for ia in jugador.lista_ias:
            print(f'{ia.nombre},{ia.vida_max},{ia.ataque},"{ia.descripcion}",{ia.prob_esp/100},'
                  f'{ia.velocidad/100}'
                  ,file = save_file)
        print(f'### IA ACTUAL ###', file = save_file)
        ia = ia_actual
        print(f'{ia.nombre},{ia.vida_max},{ia.ataque},"{ia.descripcion}",{ia.prob_esp/100},'
             f'{ia.velocidad/100},{ia.vida}',
             file = save_file)
    print("\nGuardado exitosamente!\n")

def cargar_estado(jugador):
    save_file = f'{jugador.nombre}.txt'
    lista_ia = []
    mazo = []
    cementerio = []
    coleccion = []
    lista_cartas = cargar_cartas()
    contador = -1
    with open(save_file, "r", encoding = "utf-8") as archivo:
        for linea in archivo:
            info = descompositor(linea)
            if info[0][0] == "#":
                  contador += 1
            elif contador == 0:
                  jugador.oro = int(info[0])
                  jugador.victorias = int(info[1])
                  jugador.contrincantes = int(info[2])
            #CARGAR COLLECION
            elif contador == 1:
                  carta = info
                  if len(carta) > 2:
                        if carta[1] == "tropa":
                              carta_esperada = nombre_tropas[carta[0]]
                              carta_n = carta_esperada(carta[0], int(carta[2]), carta[1], float(carta[3]), 
                                                      int(carta[4]), float(carta[5]), int(carta[6]), 
                                                      float(carta[7]), carta[8])
                              carta_n.vida = int(carta[9])
                              carta_n.dueño = jugador
                              coleccion.append(carta_n)
                        elif carta[1] == "estructura":
                              carta_esperada = nombre_estructuras[carta[0]]
                              carta_n = carta_esperada(carta[0], int(carta[2]), carta[1], float(carta[3]), 
                                                      int(carta[4]), float(carta[5]), carta[8])
                              carta_n.vida = int(carta[9])
                              carta_n.dueño = jugador
                              coleccion.append(carta_n)
                        elif carta[2] == "mixta":
                              for cartas in lista_cartas:
                                    if cartas.nombre == carta[2]:
                                          carta1 = cartas
                                    elif cartas.nombre == carta[3]:
                                          carta2 = cartas
                              carta_n = Carta_Mixta(carta1, carta2)
                              carta_n.vida = int(carta[4])
                              carta_n.dueño = jugador
                              coleccion.append(carta_n)
                              
            #CARGAR MAZO
            elif contador == 2:
                  carta = info
                  if len(carta) > 2:
                        if carta[1] == "tropa":
                              carta_esperada = nombre_tropas[carta[0]]
                              carta_n = carta_esperada(carta[0], int(carta[2]), carta[1], float(carta[3]), 
                                                      int(carta[4]), float(carta[5]), int(carta[6]), 
                                                      float(carta[7]), carta[8])
                              carta_n.vida = int(carta[9])
                              carta_n.dueño = jugador
                              mazo.append(carta_n)
                        elif carta[1] == "estructura":
                              carta_esperada = nombre_estructuras[carta[0]]
                              carta_n = carta_esperada(carta[0], int(carta[2]), carta[1], float(carta[3]), 
                                                      int(carta[4]), float(carta[5]), carta[8])
                              carta_n.vida = int(carta[9])
                              carta_n.dueño = jugador
                              mazo.append(carta_n)
                        elif carta[2] == "mixta":
                              for cartas in lista_cartas:
                                    if cartas.nombre == carta[2]:
                                          carta1 = cartas
                                    elif cartas.nombre == carta[3]:
                                          carta2 = cartas
                              carta_n = Carta_Mixta(carta1, carta2)
                              carta_n.vida = int(carta[4])
                              carta_n.dueño = jugador
                              mazo.append(carta_n)
            #CARGAR CEMENTERIO
            elif contador == 3:
                  carta = info
                  if len(carta) > 2:
                        if carta[1] == "tropa":
                              carta_esperada = nombre_tropas[carta[0]]
                              carta_n = carta_esperada(carta[0], int(carta[2]), carta[1], float(carta[3]), 
                                                      int(carta[4]), float(carta[5]), int(carta[6]), 
                                                      float(carta[7]), carta[8])
                              carta_n.vida = int(carta[9])
                              carta_n.dueño = jugador
                              mazo.append(carta_n)
                        elif carta[1] == "estructura":
                              carta_esperada = nombre_estructuras[carta[0]]
                              carta_n = carta_esperada(carta[0], int(carta[2]), carta[1], float(carta[3]), 
                                                      int(carta[4]), float(carta[5]), carta[8])
                              carta_n.vida = int(carta[9])
                              carta_n.dueño = jugador
                              mazo.append(carta_n)
                        elif carta[2] == "mixta":
                              for cartas in lista_cartas:
                                    if cartas.nombre == carta[2]:
                                          carta1 = cartas
                                    elif cartas.nombre == carta[3]:
                                          carta2 = cartas
                              carta_n = Carta_Mixta(carta1, carta2)
                              carta_n.dueño = jugador
                              carta_n.vida = int(carta[4])
            #CARGAR LISTAS IA
            elif contador == 4:
                ia_esperada = nombre_ias[info[0]]  
                nueva_ia = ia_esperada(info[0], int(info[1]), int(info[2]), info[3], 
                                       float(info[4]), float(info[5]))
                lista_ia.append(nueva_ia)
            #cargar ia actual
            elif contador == 5:
                ia_esperada = nombre_ias[info[0]]  
                nueva_ia = ia_esperada(info[0], int(info[1]), int(info[2]), info[3], 
                                       float(info[4]), float(info[5]))
                ia_esperada.vida = int(info[6])
                nueva_ia.jugador = jugador
                jugador.iarival = nueva_ia
    jugador.coleccion = coleccion
    jugador.cartas = mazo
    jugador.cementerio = cementerio
    jugador.lista_ias = lista_ia
    print("Cargado exitosamente!")
    return 