# -----------------------------------------------------------------------------
# Esta clase implementa una política de planificación de proceso por FCFS
# El primero que llega es el primero que es servido
# -----------------------------------------------------------------------------

class FCFS:
    # Retorna None si no hay procesos en la cola, sino, retorna el primer
    # proceso que se encuentra en la cola
    @staticmethod
    def despachar(cola, procesos):
        if len(cola) == 0:
            return None
        else:
            return cola[0]

    # Este método indica si la política es o no apropiativa
    @staticmethod
    def es_apropiativo(reloj):
        return True
