from entities import Item
from entities import Usuario
from utils import pretty_print

lista = []

def cargar_items():
    archivo_items = open('utils/items.dcc', 'r')
    items = archivo_items.readlines()
    archivo_items.close
    total = len(items)
    for x in range(total):
        items[x] = items[x].strip("\n")
        items[x] = items[x].split(",")
        nombre = items[x][0]
        precio = items[x][1]
        puntos = items[x][2]
        lista.append(Item(nombre, precio, puntos))
    return lista

def crear_usuario(tiene_subscripcion: bool):
    hola = Usuario(tiene_subscripcion)
    pretty_print.print_usuario(hola)
    return hola

if __name__ == "__main__":
    nuevo_usuario = crear_usuario(True)
    nuevos_items = cargar_items()
    pretty_print.print_items(nuevos_items)
    for x in nuevos_items:
        nuevo_usuario.agregar_item(nuevos_items)
    pretty_print.print_canasta(nuevo_usuario)
    nuevo_usuario.comprar
    pretty_print.print_usuario(nuevo_usuario)
