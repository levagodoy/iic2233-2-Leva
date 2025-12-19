import threading
import json

from api import app as flask_app 
from servidor import Servidor     

with open('conexion.json', 'r') as f:
    config = json.load(f)
    
HOST = config.get("host")
PUERTO_SOCKETS = int(config.get("puerto"))
PUERTO_API = config.get("puertoAPI")

def iniciar_api(host, port):
    '''
    Inicia la API
    '''
    flask_app.run(host=host, port=port, use_reloader=False)

if __name__ == "__main__":
    api_thread = threading.Thread(
        target=iniciar_api, 
        args=(HOST, PUERTO_API),
        daemon=True
    )
    api_thread.start()

    server = Servidor(PUERTO_SOCKETS, HOST, PUERTO_API) #Inicia el servidor
    server.bind_listen()
    print(f"[Servidor] Iniciando servidor en {HOST}:{PUERTO_SOCKETS}")

    try:
        server.accept_connections_thread()
    except KeyboardInterrupt:
        print("Cerrando servidor")

    server.socket_server.close()
    exit(1)