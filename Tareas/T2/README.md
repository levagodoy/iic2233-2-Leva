# Tarea 2: DCCartas contra la DCCatástrofe🎴💥


## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:


1.  **✅ Programación orientada 16 pts (8%)**
    1.  ✅Incluye y aplica herencia en un contexto correcto de la tarea.:
        1.  Se aplica la multiherencia a lo largo de todas las entidades
    2.  ✅Incluye y aplica clases abstractas en un contexto correcto de la tarea.:
        1.  Las clases Cartas() e InteligenciaArtificial() usa correctamente las clases abstractas 
    3.  ✅Incluye y aplica polimorfismo en un contexto correcto de la tarea:
        1.  La clase CartaMixtra() utiliza correctamente el polimorfismo
    4. ✅Incluye y aplica decoradores que definen properties en un contexto correcto de la tarea.
       1. Todas las clases hacen uso de decoradores
2.  ✅**Preparación programa 13 pts (7%)**
    1.  ✅El programa recibe correctamente la dificultad y el nombre del jugador como argumento por consola:
        1.  Se encuentra correctamente configurado
    2.  ✅El programa muestra correctamente la interfaz de Selección Inicial, y es consistente con la dificultad ingresada por el jugador.:
        1.  La interfaz funciona correctamente
    3.  ✅El jugador comienza con el Mazo escogido en la Selección Inicial.
        1.  La interfaz guarda automatica todas las cartas seleccionadas en el mazo
    4.  ✅Se presenta en consola la IA enemiga para que el usuario pueda planificar su estrategia.
        1.  Se presenta a la IA, mostrando su nombre, vida total y su habilidad
3.  **Entidades 76 pts (39%)**
    1.  ✅**Carta**
        1.  🟠**Carta General**
            1. ✅Modela correctamente la clase Carta, utilizando los contenidos de OOP que corresponden 
            2. ✅Modela correctamente los atributos de Carta.
            3. ✅El método Recibir daño está implementado correctamente.
            4. 🟠 El método Usar Habilidad Especial está implementado correctamente:
               1. No existe un metodo usar_habilidad() como tal, si no que sus habilidades estan en base a la etapa de combate en que se activan (previo_combate, posterior_combate, etc.), mas informacion en el modulo de cartas
            5. ✅El método Presentarse está implementado correctamente.
         2. ✅**Carta Tropa**
            1. ✅Modela correctamente la entidad Carta Tropa, utilizando los contenidos de OOP que corresponden
            2. ✅Modela correctamente los atributos de Carta Tropa.
            3. ✅El método Atacar está implementado correctamente.
            4. ✅Se implementa las habilidades especiales de la Carta Tropa.
         3. 🟠**Carta Estructura**
            1. ✅Modela correctamente la Carta Estructura, utilizando los contenidos de OOP que corresponden
            2. 🟠Se implementa las habilidades especiales de la Carta Estructura:
               1. Falta la habilidad de Canon()
         4. ✅**Carta Mixta: Tropas-Estructura**	
            1. ✅Modela las cartas mixtas correctamente, utilizando los contenidos de OOP que corresponden
            2. ✅Al fusionar cartas, la nueva carta hereda las habilidades y características de las cartas utilizadas en la combinación.
      1. ✅**Jugador**
         1. ✅Modela correctamente la clase Jugador, utilizando los contenidos de OOP que corresponden	
         2. ✅Modela correctamente los atributos de Jugador.	
         3. ✅El método Atacar está implementado correctamente.
         4. ✅El método Recibir daño está implementado correctamente.
         5. ✅El método Presentarse está implementado correctamente.
      2. 🟠**Inteligencia Artificial**
         1. ✅Modela correctamente la clase Inteligencia Artificial, utilizando los contenidos de OOP que corresponden
         2. ✅Modela correctamente los atributos de Inteligencia Artificial.
         3. ✅El método Atacar está implementado correctamente.
         4. ✅El método Recibir daño está implementado correctamente.
         5. ✅El método Habilidad especial está implementado correctamente.
         6. 🟠Se implementa correctamente las habilidades especiales la Inteligencia Artificial.
            1. Falta la habilidad de DeepSheep				
4.  **Flujo del programa 43 pts (22%)**
    1.  ✅**Menú de principal**
        1.  ✅Se muestran todas las opciones pedidas en el menú principal.
        2.  ✅Cada opción lleva a su submenú correspondiente.	
        2.  ✅Al seleccionar 'Salir del juego', se imprime un mensaje para el usuario y se termina el programa
    2.  ✅**Menú Tienda**
        1.  ✅Se muestra toda la información pedida en el menú tienda.	
        2.  ✅Se muestran todas las cartas disponibles.		
        3.  ✅Al comprar una carta, se actualiza correctamente a el dinero indicado. 	
        4.  ✅Se cumplen las reglas mínimas especificadas en el enunciado.
    3. ✅**Taller**
       1. 	✅Se muestran las combinaciones disponibles a partir de las cartas que tiene el jugador.
       2.  ✅Se cumplen las reglas del Taller especificadas en el enunciado.	
    3. ✅**Mecánica de juego**	
       1. ✅El orden de los eventos al pasar ronda sigue el orden pedido en el enunciado.
       2. ✅El juego finaliza inmediatamente en caso de que el Jugador pierda todas sus cartas activas.
    4. ✅**Robustez**
       1. ✅Todos los menús son a prueba de cualquier tipo de input.
5.  **Combate 32 pts (16%)**
    1. ✅ **Turnos**
        1.  ✅Se respeta el turno según la velocidad de la IA Enemiga y del jugador.
    2. ✅**Ataque Jugador**
       1. ✅Solo las cartas de tipo Ataque e Híbridas pueden infligir daño.
       2. ✅Cada carta puede atacar la cantidad correcta de veces por ronda.
     3. ✅**Ataque IA**
        1. ✅Se aplican correctamente los multiplicadores de ataque de la IA Enemiga según el tipo de carta.
     4. ✅**Cálculo del daño Carta**
        1. ✅El daño es calculado correctamente y toma en cuenta el tipo de carta.
        2. ✅El daño se resta correctamente a la vida de la carta.
        3. ✅El reparto de daño debe realizarse automáticamente según las reglas del enunciado.
     5.  ✅**Cálculo del daño IA**
         1.  ✅El daño base infligido por el jugador debe ponderarse mediante el multiplicador correspondiente y restarse de la vida actual de la IA Enemiga.
     6. ✅**Resolución de la Ronda**
        1. ✅Al finalizar una ronda, se cumplen las condiciones especificadas en el enunciado. 
6.  **Archivos 15 pts (8%)**
    1.  ✅**Archivos .txt**
        1.  ✅Se trabaja correctamente con el archivo de cartas.csv
        2.  ✅Se trabaja correctamente con el archivo de multiplicadores.csv 
        3.  ✅Se trabaja correctamente con los archivos: ias_facil.csv, ias_normal.csv y ias_dificil.csv
    2. ✅parametros.py
       1. ✅Utiliza e importa correctamente los parámetros del archivo parametros.py.
       2. ✅El archivo parametros.py contiene todos los parámetros y constantes que se utilizan a lo largo del programa, además de los especificados en el enunciado.	
7.  🟠**Bonus 5 décimas**
    1.  ✅Al iniciar el programa, el jugador puede dar como argumento el nombre del archivo que tiene la partida guardada.:
        1.  No necesariamente como dice el enunciando, pero si se inicia el programa con algun username de un archivo guardado, dará la opcion de cargarlo
    2. ✅El Menu Principal tiene la opcion Guardar Partida, y puede accionarse.
    3. ✅La opción Guardar Partida da la posibilidad al jugador de detener el programa, entendiendo que el jugador abandonaría el juego.
    4. ✅La opción Guardar Partida crea un archivo con todos los detalles requeridos en el enunciado, guardando en este toda la información de la partida actual.
    5. ✅Es posible guardar la partida las veces que se deseen, siempre considerando la información actualizada al instante de seleccionar la opción. 
    6. ✅Si se carga una partida guardada al iniciar el programa, el juego se reanuda con la información contenida en el archivo indicado por el jugador.
    7. ❌Se implementa un cheatcode en el menú principal: al ingresar la palabra clave veotodo en lugar de seleccionar una opción del menú, se debe mostrar toda la información actual de la partida.




## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. 


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```: ```randint```
2. ```copy```: ```copy```, ```deepcopy```
3. ```Pathlib```: ```path```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```cargar_datos```: Contiene a ```descompositor```, ```cargar_cartas```, ```cargar_multiplicadores```, ```cargar_ia```. Hecha para manejar toda las lecturas de los archivos iniciales
2. ```cartas```:Contiene a las clases```Carta_Tropa``` ```Carta_Estructura``` ```Carta_Mixta```. (En realidad, cada carta tiene su propia clase, sin embargo, por el fin de simplificar, solo se mencionan sus clases de las cuales heredan) 
3. ```jugador```: Contiene a la clase ```Jugador```. Jugador tiene la propiedad de ser el mediador entre las clases de cartas e IAs.
4. ```ia```: Contiene a la clase ```InteligenciaArtificial```(nuevamente lo mismo, en realidad contiene una clase para cada tipo de IA, pero por el fin de simplficiar, solo se menciona la clase Principal).
5. ```parametros```: Contiene las constantes utilizadas a lo largo de todo el codigo
6. ```parametros_diccionario```: Contiene diccionarios los cuales sus llaves son los nombre de las cartas o IAs, y sus valores son sus clases.
7. ```guardar_estado```: Maneja el guardado de las partidas

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. En el menu de selección, solo se puede seleccionar una vez cada tipo carta, por lo cual se van despareciendo a lo largo de que son seleccionadas
2. Al curar cada carta, solo se devuelve su vida al valor de vida máxima, no se restauran otros valores como los que pueden ser afectados por las habilidades de las IAs.
3. Las cartas Mixtas heredan sus valores de manera diferente. Suman la vida maxima de cada carta que heredan y  sacan el promedio de sus multiplicadores

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. [Link del codigo](https://www.reddit.com/r/learnpython/comments/wf0xva/comment/iisfihk/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button): Este ayudó a la creacion de los atributos de las clases como jugador, cartas e IAs. Simplificó muchisimo su creacion de habilidades de cada uno

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).