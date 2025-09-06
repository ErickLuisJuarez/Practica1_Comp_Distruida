import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

# La unidad de tiempo
TICK = 1


class NodoBroadcast(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
        "Inicializamos el nodo"
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje
        self.seen_message =  False

    def get_id(self):
        return self.id_nodo

    def broadcast(self, env):
        ''' Algoritmo de Broadcast. Desde el nodo distinguido (0)
            vamos a enviar un mensaje a todos los demás nodos.'''
        if self.id_nodo == 0:
            self.seen_message = True
            self.mensaje = "Mensaje de Broadcast"
            self.canal_salida.envia(self.mensaje, self.vecinos)

        while True:
            msg = yield self.canal_entrada.get()
            if not self.seen_message:
                self.seen_message = True
                self.mensaje = msg
                self.canal_salida.envia(msg, self.vecinos)
