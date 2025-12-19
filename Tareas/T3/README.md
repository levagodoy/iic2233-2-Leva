# Tarea 3: Departamento de las Colecciones del Cosmos 🌌

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:


1.  **✅ Carga de datos: 16pts (16%)**
    1.  Las siguientes funciones pasan todos los tests de correctitud y carga:
        1. ✅cargar_astronautas()
        2. ✅cargar_naves()
        3. ✅cargar_tripulaciones()
        4. ✅cargar_planetas()
        5. ✅cargar_planeta_minerales()
        6. ✅cargar_mision()
        7. ✅cargar_materiales_mision()

2. **🟠Consultas Simples: 15pts (15%)**
   1. Las siguientes funciones pasan todos los tests de correctitud y carga:
      1. ✅naves_de_material()
      2. ✅misiones_desde_fecha()
      3. ✅naves_por_intervalo_carga()
      4. ✅planetas_con_cantidad_de_minerales()
      5. ❌naves_astronautas_rango()
      6. ✅cambiar_rango_astronauta()
      7. ✅encontrar_planetas_cercanos()
3. **✅Consultas Complejas: 42pts (43%)**
   1. Las siguientes funciones pasan todos los tests de correctitud y carga:
      1. ✅disponibilidad_por_planeta()
      2. ✅misiones_por_tipo_planeta()
      3. ✅naves_pueden_llevar()
      4. ✅planetas_por_estadisticas()
      5. ✅ganancias_potenciales_por_planeta()
      6. ✅planetas_visitados_por_nave()
      7. ✅mineral_por_nave()
      8. ✅porcentaje_extraccion()
      9. 🟠resultado_mision():
         1.  Solo falla el test_4 de correctitud.
4. **🟠Interfaz Gráfica e Interacción: 24pts (25%)**
    1. ✅Ventana de Entrada
    2. ✅Ventana Principal:
        1. ✅Se implementa correctalemte el obtener el path del archivo usando un QFileDialog
        2. ✅Se implementa correctamente un input de texto donde se pueda ingresar la entidad a cargar y un filtro.
        3. ✅Se implementa correctamente un botón con el nombre “Ejecutar Consulta” que se encarga de cargar los datos indicados en el input de texto considerando la entidad a cargar indicada y el filtro.
        4. ✅Se implementa correctamente un elemento de texto que posea -por lo menos- un scroll de tipo vertical.
        5. ✅Se implementa correctamente un botón con el nombre “Botón Mapa”, el cual tiene como funcionalidad poder avanzar a la ventana Mapa.
    3. 🟠Ventana Mapa:
        1. ❌Se muestra correctamente el mapa estelar, haciendo uso de la función "encontrar_planetas_cercanos".
        2. ✅Se implementa un botón que retorne a la  "Ventana Principal"
    4. ✅El usuario puede moverse sin problemas a lo largo de toda la aplicación implementada.


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. No es necesario crear cualquier otro tipo de archivo.


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```collections```: ```defaultdict```
2. ```itertools```: ```tee, islice, product```
3. ```datetime```: ```datetime```
4. ```PyQt5```: ```QtCore, Qtwidgets, QtGui```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```frontend.ventana_principal```: Contiene a ```VentanaPrincipal```
1. ```frontend.ventana_mapa```: Contiene a ```VentanaMapa```
1. ```frontend.ventana_entrada```: Contiene a ```VentanaEntrada```
1. ```backend.logica```: Contiene a ```ControladorLogico```
1. ```backend.diccionario```: Contiene a ```consulta```, hecha para almacenar un diccionario con todas las funciones de carga en base al nombre de la entidad


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<link de código>: este hace \<lo que hace> y está implementado en el archivo <nombre.py> en las líneas <número de líneas> y hace <explicación breve de que hace>

## Descuentos
La guía de descuentos se encuentra [link](https://github.com/IIC2233/Syllabus/blob/main/Tareas/Bases%20Generales%20de%20Tareas%20-%20IIC2233.pdf).