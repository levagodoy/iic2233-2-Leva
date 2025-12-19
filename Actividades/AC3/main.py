from __future__ import annotations
from typing import Self

import copy


class NodoCliente:
    identificador = 0

    def __init__(self, preferencial: bool) -> None:
        self.identificador = NodoCliente.identificador
        NodoCliente.identificador += 1

        self.preferencial = preferencial
        self.siguiente = None

    def agregar_nodo(self, nuevo_nodo: NodoCliente) -> None:
        if self.siguiente == None:
            self.siguiente = nuevo_nodo
            return
        proximo_nodo = self.siguiente
        while proximo_nodo.siguiente != None:
            proximo_nodo = proximo_nodo.siguiente
        proximo_nodo.siguiente = nuevo_nodo
        return
    def __str__(self) -> str:
        texto = f'C({self.identificador}) ->'
        if self.siguiente != None:
            proximo_nodo = self.siguiente
            while proximo_nodo.siguiente != None:
                conc = f' C({proximo_nodo.identificador}) ->'
                texto = texto+conc
                proximo_nodo = proximo_nodo.siguiente
            conc = f' C({proximo_nodo.identificador}) ->'
            texto = texto+conc
        a_none = f' None'
        texto = texto + a_none
        return texto

    def __len__(self) -> int:
        contador = 0
        if self.siguiente == None: 
            contador += 1
            return contador
        else:
            proximo_nodo = self.siguiente
            contador += 1
            while proximo_nodo.siguiente != None:
                contador += 1
                proximo_nodo = proximo_nodo.siguiente
            contador += 1
            return contador


class SistemaColas:
    def __init__(self) -> None:
        self.cola_preferencial = None
        self.cola_normal = None

    def __str__(self) -> str:
        return f'Preferencial: {self.cola_preferencial}\n' \
               f'Normal:       {self.cola_normal}'

    def agregar_persona(self, preferencial: bool) -> None:
        if preferencial == True:
            persona = NodoCliente(True)
            if self.cola_preferencial != None:
                self.cola_preferencial.agregar_nodo(persona)
                return
            else:
                self.cola_preferencial = persona
                return
        else:
            persona = NodoCliente(False)
            if self.cola_normal != None:
                self.cola_normal.agregar_nodo(persona)
                return
            else:
                self.cola_normal = persona
                return

    def __len__(self) -> int:
        total_normal = 0
        total_preferencial =0 
        if self.cola_preferencial != None:
            total_preferencial = len(self.cola_preferencial)
        if self.cola_normal != None:
            total_normal = len(self.cola_normal)
        return total_preferencial + total_normal

    def __iter__(self) -> IteradorSistemaColas:
        copia_cola_pref = copy.deepcopy(self.cola_preferencial)
        copia_cola_norm = copy.deepcopy(self.cola_normal)
        sistema = IteradorSistemaColas(copia_cola_pref, copia_cola_norm)
        return sistema


class IteradorSistemaColas:
    def __init__(self, cola_preferencial, cola_normal) -> None:
        self.cola_preferencial = cola_preferencial
        self.cola_normal = cola_normal
        self.contador_preferencial = 0

    def __iter__(self) -> Self:
        return self
    def __next__(self) -> NodoCliente:
        if self.cola_preferencial != None:
            while len(self.cola_preferencial) != self.contador_preferencial:
                nodo = self.cola_preferencial
                self.cola_preferencial = nodo.siguiente
                self.contador_preferencial += 1
                return nodo
        if self.cola_normal == None:
            raise StopIteration()
        else:
            nodo = self.cola_normal
            self.cola_normal = nodo.siguiente
            return nodo
        



if __name__ == '__main__':
    print('----- NODO CLIENTE -----')

    persona_1 = NodoCliente(True)
    persona_2 = NodoCliente(True)
    persona_3 = NodoCliente(True)
    persona_4 = NodoCliente(True)

    persona_1.agregar_nodo(persona_2)
    persona_1.agregar_nodo(persona_3)
    persona_1.agregar_nodo(persona_4)

    print('Cola: ', persona_1)
    print('Largo:', len(persona_1))
    print()


    print('----- SISTEMA COLAS -----')

    sistema_colas = SistemaColas()
    sistema_colas.cola_preferencial = persona_1

    sistema_colas.agregar_persona(True)
    sistema_colas.agregar_persona(False)
    sistema_colas.agregar_persona(False)

    print(sistema_colas)
    print(len(sistema_colas))


    print('----- ITERACIÓN SISTEMA -----')

    estados = {True: 'Preferencial', False: 'Normal'}

    for cliente in sistema_colas:
        print(f'> Avanza Cliente({cliente.identificador}, {estados[cliente.preferencial]})')
    print('< Se acabó la cola')
