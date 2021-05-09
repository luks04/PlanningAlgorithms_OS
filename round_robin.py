# Imprimenta el algoritmo de planificacion de RoundRobin
# --------------------------------------------------------

class RoundRobin:
    # Constructor
    def __init__(self, quantum):
        self.__quantum = quantum

    # Cambia el quantum de la politica de planificacion
    def set_quantum(self, quantum):
        self.__quantum = quantum

    # Retorna None si no hay procesos en la cola, sino, retorna el primer
    # proceso que se encuentra en la cola
    @staticmethod
    def despachar(cola, procesos):
        if len(cola) == 0:
            return None
        else:
            return cola[0]

    # Este método indica si la política es o no apropiativa
    def es_apropiativo(self, reloj):
        if reloj % self.__quantum == 0:
            return False
        return True
