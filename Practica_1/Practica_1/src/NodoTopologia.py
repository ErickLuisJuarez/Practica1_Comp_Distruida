import simpy
import time
from Nodo import *
from Canales.CanalBroadcast import *

# La unidad de tiempo
TICK = 1


class NodoTopologia(Nodo):
    ''' Implementa la interfaz de Nodo para el algoritmo de Broadcast.'''

    def __init__(self, id_nodo, vecinos, canal_entrada, canal_salida, mensaje=None):
        self.id_nodo = id_nodo
        self.vecinos = vecinos
        self.canal_entrada = canal_entrada
        self.canal_salida = canal_salida
        self.mensaje = mensaje
        self.procesos_conocidos = {self.id_nodo}
        self.canales_conocidos = {(self.id_nodo,y) for y in self.vecinos}


    def topologia(self, env):
        self.canal_salida.envia((self.id_nodo,self.vecinos),self.vecinos)
        while True:
            msg = self.canal_entrada.get()
            k, vecinos_j = msg[0], msg[1]
            if k not in self.procesos_conocidos:
                self.procesos_conocidos.add(k)
                nuevos_canales = {(k,l) for l in vecinos_j}
                self.canales_conocidos.update({nuevos_canales})
                vecinos_filtrados = [m for m in self.vecinos if m != k]
                self.canal_salida.envia((k,vecinos_j),vecinos_filtrados)

                todos_conocidos = True
                for l,m in self.canales_conocidos:
                    evaluador = l in self.procesos_conocidos and m in self.procesos_conocidos
                    todos_conocidos = todos_conocidos and evaluador
                if todos_conocidos:
                    break