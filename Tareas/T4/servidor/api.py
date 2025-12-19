from flask import Flask, request, json, Response
from dccasino import Dccasino
from parametros import TOKEN_AUTENTICACION

app = Flask(__name__)

TOKEN = TOKEN_AUTENTICACION

casino = Dccasino()
casino.cargar_datos()

def responder_json(codigo_estado, **body) -> Response:
    body = json.dumps(body)
    return Response(status=codigo_estado, response=body, content_type='application/json')


def verificar_token(headers):
    token_recibido = headers.get('Authorization')
    if token_recibido != TOKEN:
        return False
    return True


@app.route('/users/<username>', methods=['GET'])
def entregar_usuario(username):
    '''
    Recibe un username y entrega la informacion del usuario
    '''
    try:
        info = casino.informacion_usuario(username)
        return responder_json(200, msg = 'Informacion usario', info = info)
    except IndexError:
        return responder_json(404, msg = 'Usuario no encontrado!')


@app.route('/users', methods = ['POST'])
def regisitar_usuario():
    '''
    Recibe un username y un token y lo registra en ususarios.csv
    '''
    if not verificar_token(request.headers):
        return responder_json(401, msg = 'Token invalido')
    
    nombre = request.get_json(force=True).get('username')
    casino.registrar_usuario(nombre)
    
    return responder_json(201, msg = 'Usuario Registrado')


@app.route('/users/<username>', methods=['PATCH'])
def actualizar_usuario(username):
    '''
    Recibe un username y un token y actualiza su informacion en usuarios.csv
    '''
    body = request.get_json(force=True)
    earnings = body.get('earnings')
    
    if not verificar_token(request.headers):
        return responder_json(401, msg = 'Token invalido')
    
    casino.actualizar_usuario(username, earnings)
    return responder_json(200, msg = 'Usuario Actualizado')


@app.route('/games/', methods = ['GET'])
def informacion_juegos():
    '''
    Recibe un numero n y entrega la informacion de los ultimos n juegos de ganancias.csv
    '''
    total = int(request.args.get('n', 3))
    informacion = casino.obtener_ganacias(total)
    
    return responder_json(200, info = informacion)


@app.route('/games/<id_juego>', methods = ['POST'])
def actualizar_ganancias(id_juego):
    '''
    Recibe un id_juego y un token y actualiza la informacion de ganancias.csv
    '''
    if not verificar_token(request.headers):
        return responder_json(401, msg = 'Token invalido')
    
    body = request.get_json(force= True)
    print(body)
    
    casino.actualizar_ganancias(body)
    return responder_json(200, msg = 'Ganancias Actualizadas')