# Tarea 1: DCCasillas 4️⃣➕5️⃣🟰9️⃣


Un buen `README.md` puede marcar una gran diferencia en la facilidad con la que corregimos una tarea y, consecuentemente, en cómo funciona su programa. Por lo general, entre más ordenado y limpio sea este, mejor será.

Para nuestra suerte, GitHub soporta el formato [Markdown](https://es.wikipedia.org/wiki/Markdown), el cual permite utilizar una amplia variedad de estilos de texto, tanto para resaltar cosas importantes como para separar ideas o poner código de manera ordenada ([pueden ver casi todas las funcionalidades que incluye aquí](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)).

Un buen `README.md` no tiene por qué ser muy extenso tampoco; hay que ser **concisos** (a menos que lo consideren necesario), pero **tampoco pueden** faltar cosas. Lo importante es que sea claro y limpio.

**Dejar claro lo que NO pudieron implementar y lo que no funciona a la perfección. Esto puede sonar innecesario, pero permite que el ayudante se enfoque en lo que sí podría subir su puntaje.**

## Consideraciones generales :octocat:

<Descripción de lo que hace y lo que **_no_** hace la tarea que entregaron, junto con detalles de último minuto y consideraciones como, por ejemplo, cambiar algo en cierta línea del código o comentar una función.>

### Cosas implementadas y no implementadas :white_check_mark: :x:




#### Dccasillas.py y Tablero.py: 23 pts (41.8%)
##### ✅ Tablero Inicializador: Se agregan dos nuevos atributos, **filas** y **columnas**, para luego optimizar otras variables.
##### ✅ Tablero cargar_tablero: Hace lo solicitado.
##### ✅ Tablero mostrar_tablero: Hace lo solicitado.
##### ✅ Tablero modificar_casillas: Hace lo solicitado.
##### ✅ Tablero validar: Hace lo solicitado; sin embargo, requiere haber cargado un estado previo en el cual se le entreguen sus filas y columnas. Entonces, al hacer casos de prueba sin haber nombrado sus filas o columnas, puede entregar errores de vuelta.
##### ✅ Tablero encontrar_solucion: Para su uso, se crean dos funciones adicionales: *resolver_tablero*, la cual es una función recursiva que, a modo de backtracking, resuelve el tablero, y *validar_movimiento*, que es una función que revisa si el último movimiento es válido.
##### ✅ DCCasillas Inicializador: Se agrega el atributo **juegos_totales** para luego optimizar el uso de otras funciones.
##### ✅ DCCasillas abrir_tablero: Hace lo solicitado.
##### ✅ DCCasillas guardar_estado: Hace lo solicitado.
##### 🟠 PEP8: Debido a dudas e incertidumbres sobre la manera correcta de utilizar este formato, no está claro si realmente está bien utilizado.

#### Menú: 25 pts (45,5%)
##### ✅ Consola: Se inicia la consola de manera automática, mostrando el menú de inicio y el input a ingresar.
##### ✅ Menú de Inicio: El texto del menú de inicio es mostrado con la función `menu_inicio()`, la cual no recibe ni devuelve ningún valor, solo se ejecuta como método para mostrar texto.
##### ✅ Menú de Acciones: Es una función recursiva; cualquier valor que sea distinto de 5 hará que se vuelva a ejecutar. Sin embargo, no se actualiza correctamente el valor de `tableros_resueltos`.
##### ✅ Modularización: Se utilizan los módulos indicados en las instrucciones.
##### 🟠 PEP8: Debido a dudas e incertidumbres sobre la manera correcta de utilizar este formato, no está claro si realmente está bien utilizado.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es `main.py`.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. `copy`: `deepcopy()`
2. `pathlib`: `Path` 

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. `dccasillas`: Contiene a `Dccasillas`.
2. `tablero`: Contiene a `Tablero`.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Al momento de seleccionar el usuario en el menú de Inicio, se asume que también se debe ingresar el nombre del archivo `__config__`.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<https://www.geeksforgeeks.org/dsa/sudoku-backtracking-7/>: En el, se extrajó el algoritmo principal para poder resolver el tablero a base de *backtracking*. A pesar de que la mayoria del codigo no aplica debido a las diferencias en tanto los validadores de movimientos como la estructura de los tableros y sus objetivos, ciertas lineas siguen siendo similares al algoritmo entregado. Esta implementado en el archivo <tablero.py> en las líneas <88-106>.
2. \<https://stackoverflow.com/a/2612815>: Fue utilizado para saber como copiar listas dentro de los objetos sin que sea una copia del objeto mismo. Su uso en unicamente visible en <tablero.py> en las lineas <114, 115, 116 y 125>.

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).
