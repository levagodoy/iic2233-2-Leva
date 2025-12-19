import sys
from PyQt5.QtWidgets import QApplication

from frontend.ventana_entrada import VentanaEntrada
from frontend.ventana_principal import VentanaPrincipal
from frontend.ventana_mapa import VentanaMapa
from backend.logica import ControladorLogico



if __name__ == '__main__':
    def hook(type, value, traceback) -> None:
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])

    # Instanciamos las clases
    ventana_entrada = VentanaEntrada()
    ventana_principal = VentanaPrincipal()
    ventana_mapa = VentanaMapa()
    operador_logico = ControladorLogico()
    
    #Inicia mostrando unicamente la ventana inicial
    ventana_entrada.show()
    ventana_entrada.senal_ingreso.connect(ventana_principal.show) #Inicia la ventana principal
    
    #Conecta el boton de consultas con el operador logico
    ventana_principal.senal_consulta.connect(operador_logico.enviar_generador) 
    
    #Envia el nuevo path a la ventana mapa
    ventana_principal.senal_path.connect(ventana_mapa.recibir_path)
    
    #Abre la ventana mapa
    ventana_principal.senal_mapa.connect(ventana_mapa.show)
    
    #Envia los datos para encontrar los planetas cercanos
    ventana_mapa.senal_planetas.connect(operador_logico.encontrar_planetas)
    
    #Vuelve a abrir la ventana principal
    ventana_mapa.senal_regreso.connect(ventana_principal.show)
    
    #Reenvia el generador filtrado a la ventana principal
    operador_logico.senal_vuelta_consulta.connect(ventana_principal.actualizar_lista)
    
    #Devuelve el generador con los planetas cercanos.
    operador_logico.senal_mapa.connect(ventana_mapa.recibir_planetas)
    
    sys.exit(app.exec())