# Implementa la política de planificacion SJF apropiativo
# ----------------------------------------------------------------------------------

class SJF:
    # Retorna None si no hay procesos en la cola, sino, retorna el
    # proceso que deberá ocupar la CPU a continuación
    @staticmethod
    def despachar(cola, procesos):
        menor = 1_000_000
        proceso = None
        for proc in cola:
            if procesos[proc].cpu() < menor:
                menor = procesos[proc].cpu()
                proceso = proc
        return proceso

    @staticmethod
    def es_apropiativo(reloj):
        return True

