# Tarea 4: DCCasino
## Consideraciones generales :octocat:

<Descripción de lo que hace y que **_no_** hace la tarea que entregaron junto
con detalles de último minuto y consideraciones como por ejemplo cambiar algo
en cierta línea del código o comentar una función>

### Cosas implementadas y no implementadas :white_check_mark: :x:

1.  **Cliente: 84 pts (47%)**
    1. **✅Ventana de Inicio**
        1. ✅Se visualiza correctamente la ventana. Se muestran todos los elementos mínimos solicitados en el enunciado, sin superponerse entre sí.
        2. ✅Se implementa algún tipo de notificación para el usuario cuando algún otro cliente con el mismo nombre de usuario ingresado ya esta conectado.
        3. ✅Se pasa a la ventana siguiente si se inicia sesión correctamente.
        4. ✅Se implementa correctamente el envío del nombre de usuario al servidor.
    2. **✅Ventana Principal**
        1. ✅Se visualiza correctamente la ventana. Se muestran todos los elementos mínimos solicitados en el enunciado, sin superponerse entre sí.
        2. Se muestran las últimas 5 ganancias o pérdidas de los jugadores.
        3. ✅Se muestra el nombre y saldo actual del jugador conectado.
        4. ✅Al presionar el botón de cargar dinero, se abre la ventana de recargar.
        5. ✅Al presionar el botón de alguno de los juegos y este estar en etapa de apuestas, se abre la ventana del juego respectivo.
        6. ✅No es posible entrar a alguno de los juegos si este está en progreso.
    3. **Ventana de Recarga**	
        1. ✅Se visualiza correctamente la ventana. Se muestran todos los elementos mínimos solicitados en el enunciado, sin superponerse entre sí.
        2. ✅Es posible recargar el monto de dinero ingresado por el usuario. Este cambio se refleja en la interfaz. 
    4. **✅Inicio de juego**
        1. ✅Para cada juego implementado, se visualiza correctamente la ventana. Se muestran todos los elementos mínimos solicitados en el enunciado, sin superponerse entre sí.
        2. ✅Para cada juego implementado, es posible introducir un monto a apostar, y este debe ser mayor al monto mínimo de apuesta. Este es recolectado inmediatamente.
        3. ✅Para cada juego implementado, una vez se cumple la cantidad límite de apuestas de ese juego, este comienza automáticamente.
    5. **🟠Aviator**
        1. 🟠El tiempo de crash y el multiplicador de Aviator se calculan con la fórmula pedida. Los parámetros de la fórmula son los adecuados:
            1. Solo se implementan las formulas, no existe una GUI para el juego.
        2. ❌La posición del avión se actualiza segundo a segundo correctamente. El camino que siguió el avión queda demarcado correctamente.
        3. ❌El multiplicador y ganancias de cada jugador se actualizan correctamente segundo a segundo.
        4. ❌Es posible retirarse mientras el avión vuela. Una vez retirado, se dehabilita la opción. No es posible retirarse luego del crash.
        5. ❌Una vez ocurrido el crash, se aplican correctamente los pagos respectivos según el resultado. La visualización de resultados dura el tiempo requerido por el enunciado.
    6. **🟠Blackjack**
        1. ✅Se reparten dos cartas por cada jugador y al dealer. Una de ellas es visible para todos y otra está oculta para los jugadores adversarios. 
        2. 🟠La tercera repartición ocurre un usuario a la vez, en orden. Durante el turno del jugador es posible pedir múltiples cartas adicionales o pasar. En caso de pasar de 21, el jugador pierde:
           1.  No se visualiza correctamente las cartas en el juego, pero si es posible jugar.
        3. 🟠El dealer revela su carta oculta y se reparte sus últimas cartas siguiendo las reglas del enunciado. 
        4. 🟠Una repartido todo, se aplican correctamente los pagos respectivos según el resultado. La visualización de resultados dura el tiempo requerido por el enunciado.:
            1. Se calcula correctamente el monto a pagar y los resultados, sin embargo no se actualizan en la GUI.
    7. **Fin del juego**
        1. ✅Al finalizar el flujo completo de cualquier juego, este vuelve a comenzar desde la etapa de apuestas y es posible volver a jugar.
2. **✅Networking: 27 pts (15%)**
    1. **✅Networking General**
        1. ✅Correcto uso de TCP/IP.
        2. ✅Instancia y conecta los sockets de manera correcta, sin bloquearse al escuchar un socket.
        3. ✅Si algún Cliente se desconecta, el servidor sigue funcionando. Si el servidor se desconecta, se finaliza el programa para todos los clientes.
    2. **✅Codificación y decodificación**
        1. ✅Se envía primero el largo del contenido y luego el contenido por chunks.
        2. ✅Se envía el valor correcto del largo del contenido
        3. ✅Cada paquete enviado posee el número de paquete y el contenido del objeto usando la cantidad de bytes correcta
        4. ✅Se rellena con ceros (b'\x00') correctamente
        5. ✅Se usa el XOR correctamente sobre el Paquete antes de enviarlo
        6. ✅Se obtiene correctamente el objeto a partir de los bytes recibidos siguiendo el protocolo
3. **✅Funcionalidades Servidor: 35 pts (20%)**
    1. **Inicio sesión**
        1. ✅El servidor revisa que el nombre de usuario no esté siendo usado por otro cliente en línea y responde adecuadamente. Ingresa el nombre en la base de datos con el monto por defecto si no existía.
    2. **✅Administración de partidas**
        1. ✅El servidor posee una única sala de juego por cada juego. Estas pueden funcionar en paralelo.
        2. ✅El servidor permite diferenciar si una partida de un juego está en etapa de apuestas, está ejecutandose, o está mostrando resultados del juego.
        3. ✅El servidor puede diferenciar a los jugadores de una sala que han apostado y los que no han apostado. Una vez se llega a la cantidad máxima de apuestas, elimina a los jugadores que no apostaron de la sala.
        4. ✅Cuando un juego comienza a ejecutarse, el servidor determina los parámetros necesarios para la realización de dicho juego y los entrega a cada cliente.
        5. ✅De ser necesario para un juego, el servidor puede recibir información adicional de los clientes para progresar la partida y responder adecuadamente (entregando cartas, pasando de turno, recibiendo un retiro del aviator, etc.)
    3. **✅Durante la partida**
        1. ✅Al finalizar la partida, el servidor calcula las ganancias o perdidas necesarias y las indica a los clientes.
        2. ✅Al registrar los resultados de una partida o la modificación en el dinero de un cliente, se modifican adecuadamente las bases de datos respectivas.
    4. **✅WebServices**
        1. ✅El servidor utiliza correctamente los endpoints (GET, POST y PATCH) de /users.
        2. ✅El servidor utiliza correctamente los endpoints de /games (GET y POST).
        3. ✅El servidor no modifica directamente los archivos que dependen de WebServices.
4. **✅Webservices: 21 pts (12%)**
    1. **✅GET /users/:id**
    2. **✅POST /users**
    3. **✅PATCH /users/:id**
    4. **✅GET /games?n=N**
    5. **✅POST /games/juego**
    6. **✅Concurrencia**
5. **✅Archivos: 12 pts (7%)**
    1. **✅Estructura**
    2. **✅conexion.json**
    3. **Parámetros**




## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py``` en la carpeta ```Cliente``` para el cliente y ```Servidor``` para el servidor. Además se debe crear los siguientes archivos y directorios adicionales:
1. ```database``` en ```servidor```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. `PyQt5`: Utilizada para la interfaz gráfica del cliente. 
2. `Flask`: Utilizada para crear la API en el servidor. 
3. `requests`: Utilizada para realizar peticiones HTTP a la API. 
4. `socket`: Utilizada para la comunicación por red (TCP/IP). 
5. `threading`: Utilizada para manejar la concurrencia con threads. 
6. `json`: Utilizada para serializar y deserializar datos. 
7. `time`: Utilizada para manejar tiempos y pausas. 
8. `datetime`: Utilizada para crear los timestampss. 
9. `random`: Utilizada para seleccionar aleatoriamente cartas y para generar números aleatorios. 
10. `math`: Utilizada para operaciones matemáticas como math.ceil y la constante de euler. 
13. `queue`: Utilizada para colas de mensajes thread-safe.
14. `abc`: Utilizada para definir clases abstractas. 
15. `collections`: Utilizada para estructuras de datos especializadas como deque en el servidor y 
deque en el cliente.

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

#### Cliente
1. `backend.networking`: Contiene la lógica de networking del cliente, incluyendo la clase `Cliente` que maneja la conexión con el servidor, y funciones para codificar/decodificar mensajes.
2. `backend.juegos`: Maneja la lógica de los juegos en el lado del cliente.
3. `frontend.ventana_inicio`: Contiene la clase `VentanaInicio` que maneja la interfaz gráfica del inicio de sesión.
4. `frontend.ventana_principal`: Contiene la clase `VentanaPrincipal` que maneja la interfaz del lobby principal.
5. `frontend.ventana_aviator`: Contiene la clase `VentanaAviator` para la interfaz del juego Aviator.
6. `frontend.ventana_blackjack`: Contiene la clase `VentanaBlackjack` para la interfaz del juego Blackjack.
7. `frontend.cartas`: Módulo auxiliar para el manejo y visualización de cartas.

#### Servidor
1. `servidor`: Contiene la clase `Servidor` que inicializa el socket del servidor y acepta conexiones de clientes.
2. `thread_cliente`: Contiene la clase `ThreadCliente` que maneja la comunicación individual con cada cliente conectado.
3. `dccasino`: Contiene la clase `DCCasino` que administra la lógica central del casino, usuarios y salas de juego.
4. `api`: Maneja las consultas a la API REST para obtener/actualizar información de usuarios y juegos.
5. `juegos.base`: Define la clase base `Juego` con la lógica común para todos los juegos.
6. `juegos.aviator`: Implementa la lógica específica del juego Aviator.
7. `juegos.blackjack`: Implementa la lógica específica del juego Blackjack.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. <Al momento de perder la conexion con el servidor, el cliente se desconecta> 


-------

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. \<#https://www.geeksforgeeks.org/python/blackjack-console-game-using-python/>: este muestra un codigo simple para implementar el blackjack y está implementado en el archivo <servidor.juegos.blackjack.py> en las líneas <39> y hace un mazo de cartas estandar.
