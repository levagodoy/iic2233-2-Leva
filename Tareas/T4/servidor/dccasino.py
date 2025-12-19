import json
from os import path
from datetime import datetime

import pandas as pd

from parametros import MONTO_INICIO


class Dccasino:
    def __init__(self) -> None:
        self.path_usuarios = path.join("database",'usuarios.csv')
        self.path_ganancias = path.join("database",'ganancias.csv')
        if not path.exists(self.path_usuarios):
            self.crear_archivos()
        self.datos_usuarios = {}
        self.datos_ganancias = {}
        self.tokens = {}
        
    def crear_archivos(self):
        '''
        Crea todos los archivos necesarios en caso que no existan
        '''
        usuarios = pd.DataFrame(columns = ['username', 'timestamp', 'balance'])
        ganancias = pd.DataFrame(columns = ['id_trans', 'username', 'timestamp', 'earnings'])
        usuarios.to_csv(self.path_usuarios, index=False)
        ganancias.to_csv(self.path_ganancias, index=False)

    def cargar_datos(self):
        '''
        Carga ambos objetos como DFs
        '''
        self.datos_usuarios = pd.read_csv(self.path_usuarios)
        self.datos_ganancias = pd.read_csv(self.path_ganancias)
        
    def guardar_datos(self) -> None:
        '''
        Guarda ambos DFs en el csv original.
        '''
        self.datos_usuarios.to_csv(self.path_usuarios, index=False)
        self.datos_ganancias.to_csv(self.path_ganancias, index=False)
        
        print('Datos guardados!')
    
    def registrar_usuario(self, username: str) -> None:
        '''
        Recibe el username del usuario, guarda la hora actual y guarda su informacion en el csv
        original
        '''
        hora_actual = datetime.now()
        hora_actual = hora_actual.timestamp()
        usuario = {
            "username": username,
            "timestamp": hora_actual,
            "balance": MONTO_INICIO
        }
        usuario = pd.DataFrame([usuario]) #Crea un DF con la info del usuario
        
        self.datos_usuarios = pd.concat([self.datos_usuarios, usuario],
                                        ignore_index= True) #Lo agrega al DF original
        
        print(f'Usuario registrado!: {username}, 0')
        
        self.guardar_datos()
    
    def actualizar_usuario(self, username: str, earnings: int) -> None:
        '''
        Actualiza usuarios.csv con el nuevo dinero del usuario. Puede ser que aun falte agregar el cambio en
        ganancias.csv
        '''
        self.datos_usuarios.loc[self.datos_usuarios['username'] == username, 'balance'] +=earnings
        self.guardar_datos()
    
    def obtener_ganacias(self, cantidad: int) -> list:
        '''
        Obtiene las ultimas n ganancias
        '''
        ganancias = self.datos_ganancias.tail(cantidad)
        ganancias = ganancias.values.tolist()
        return ganancias

    def actualizar_ganancias(self, datos : json) -> None:
        '''
        Actualiza ganancias.csv con la nueva ganancia
        '''
        for i in datos.keys():
            if datos.get('id', 0) == 'P':
                informacion = {
                'id_trans': datos['id'],
                'username': datos['nombre'],
                'timestamp': datos['hora'],
                'earnings': datos['monto']
            }
                informacion = pd.DataFrame([informacion]) 
                self.datos_ganancias = pd.concat([self.datos_ganancias, informacion], 
                                             ignore_index = True)
                break
            resultado = datos[i]
            informacion = {
                'id_trans': resultado['id'],
                'username': resultado['nombre'],
                'timestamp': resultado['hora'],
                'earnings': resultado['ganancia']
            }
            
            informacion = pd.DataFrame([informacion])
            self.datos_ganancias = pd.concat([self.datos_ganancias, informacion], 
                                             ignore_index = True)
        

        self.guardar_datos()
            
    def informacion_usuario(self, username: str) -> list:
        '''
        Obtiene la informacion del usuario y la retorna al API
        '''
        datos_usuario = self.datos_usuarios.loc[self.datos_usuarios['username'] == username]
        datos_usuario = datos_usuario.iloc[0].tolist()
        datos_usuario[1] = float(datos_usuario[1])
        datos_usuario[2] = int(datos_usuario[2])
        
        return datos_usuario