# Implementa la política de planificacion de prioridades apropiativo
# tanto no apropiativo. La prioridad máxima es cero...
# ----------------------------------------------------------------------------------

class PrioridadesApropiativo:
    # Retorna None si no hay procesos en la cola, sino, retorna el
    # proceso que deberá ocupar la CPU a continuación
    @staticmethod
    def despachar(cola, procesos):
        if len(cola) == 0:
            return None
        else:
            prior = 1_000_000
            for proc in cola:
                if procesos[proc].prioridad() < prior:
                    prior = procesos[proc].prioridad()
                    proceso = proc
            return proceso

    @staticmethod
    def es_apropiativo(reloj):
        return True


class PrioridadesNoApropiativo:
    # Retorna None si no hay procesos en la cola, sino, retorna el
    # proceso que deberá ocupar la CPU a continuación
    @staticmethod
    def despachar(cola, procesos):
        if len(cola) == 0:
            return None
        else:
            prior = 1_000_000
            for proc in cola:
                if procesos[proc].prioridad() < prior:
                    prior = procesos[proc].prioridad()
                    proceso = proc
            return proceso

    @staticmethod
    def es_apropiativo(reloj):
        return False
