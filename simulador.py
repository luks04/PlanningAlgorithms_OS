"""
El simulador del planificador de procesos de un sistema operativo.
El objetivo es ver como se comportan los despachadores de procesos
con diversas políticas y tratar de medir su eficiencia
"""

# Paquetes con los que trabajaremos
import csv
import fcfs
import round_robin
import sjf
import srtf
import prioridades

# --------------------------------------------------------------------------------
# Clase donde se mantiene la información de un proceso
# --------------------------------------------------------------------------------
class Proceso:
    # Constructor
    def __init__(self, identificador, prioridad, llegada, cpu):
        self._identificador = identificador
        self._prioridad = prioridad
        self._llegada = llegada
        self._cpu = cpu

    # Métodos analizadores, para obtener cada uno de los atributos del proceso
    def identificador(self):
        return self._identificador

    def prioridad(self):
        return self._prioridad

    def llegada(self):
        return self._llegada

    def cpu(self):
        return self._cpu

    # Método que modifica el tiempo que le falta al proceso para finalizar
    def decrementar_tiempo_cpu(self):
        if self._cpu > 0:
            self._cpu = self._cpu - 1


# ------------------------------------------------------------------------------
# Los despachadores deben seguir las directivas de esta clase
# ------------------------------------------------------------------------------
class Despachador:
    # Constructor
    def __init__(self):
        self.apropiativo = False

    # Permite saber si es o no apropiativo el proceso
    def es_apropiativo(self):
        return False

    # Obtiene el siguiente proceso a ocupar el CPU
    def despachar(cola_procesos, bloque_procesos):
        return None


# ------------------------------------------------------------------------------
# Esta es la clase que realiza la simulación de la tarea de planificación de
# procesos en un sistema operativo
# ------------------------------------------------------------------------------

class Simulador:
    # Constructor de la clase
    def __init__(self, despachador):
        # Atributos
        self._reloj = 0
        self._colaProcesos = []
        self._procesos = {}
        self._procesoCPU = ""
        self._despachador = despachador

    # Obtiene los datos de configuración para la simulación
    def leer_configuracion(self, nombre_archivo):
        with open(nombre_archivo, newline='') as archivo:
            reader = csv.reader(archivo)
            n = 1
            for row in reader:
                if n > 1:
                    nuevo_proceso = Proceso(identificador=row[0],
                                            prioridad=int(row[1]),
                                            llegada=int(row[2]),
                                            cpu=int(row[3]))
                    self._procesos[row[0]] = nuevo_proceso
                n = n + 1

    # Buscar procesos que inician de primero en el CPU
    # Retorne el reloj en que debe comenzar la simulación
    def tiempo_inicio_simulacion(self):
        tmax = 1_000_000
        procesos_iniciales = []
        for proceso in self._procesos.values():
            if proceso.llegada() < tmax:
                tmax = proceso.llegada()
                procesos_iniciales = [proceso.identificador()]
            elif proceso.llegada() == tmax:
                procesos_iniciales.append(proceso.identificador())
        return tmax, procesos_iniciales

    # Obtiene el número de procesos que hay en la tabla de procesos
    def num_procesos(self):
        return len(self._procesos)

    # Obtiene la informacion del proceso que tiene el identificador dado
    def info_proceso(self, identificador):
        return self._procesos[identificador]

    # Obtener el proceso que está usando la CPU
    def proceso_en_cpu(self):
        return self._procesoCPU

    # Obtener el reloj del simulador
    def reloj(self):
        return self._reloj

    # Obtiene los procesos que nacen en el mismo momento del reloj actual
    def nacen_procesos(self):
        for proceso in self._procesos.values():
            if proceso.llegada() == self._reloj:
                self._colaProcesos.append(proceso.identificador())

    # Elimina e proceso de la cola de procesos
    def eliminar_proceso(self, pid):
        self._colaProcesos.remove(pid)

    # Agregar el proceso a la cola de procesos
    def agregar_proceso(self, pid):
        if not (pid in self._colaProcesos):
            self._colaProcesos.append(pid)

    # Inicialización de la operación del simuador
    def tiempo_cero(self):
        (t, lprocs) = self.tiempo_inicio_simulacion()
        if not lprocs:
            return False

        self._reloj = t
        self._colaProcesos = lprocs

        if not (self._despachador is None):
            proc = self.despachar()
            if proc is None:
                return False
            else:
                self._procesoCPU = proc
                self.eliminar_proceso(proc)
                return True
        else:
            return False

    # Imprime la información del estado actual de la simulación
    def imprimir_info_simulacion(self):
        print("+----+----+")
        print("|%3d | %s |" % (self._reloj, self._procesoCPU))

    # Decrementa el tiempo en CPU  del proceso que está actualmente siendo ejecutado
    def decrementar_tiempo_cpu_proceso(self):
        proc = self._procesos[self._procesoCPU]
        if not (proc is None):
            proc.decrementar_tiempo_cpu()

    # Obtiene el siguiente proceso a ocupar la CPU
    def despachar(self):
        return self._despachador.despachar(self._colaProcesos, self._procesos)

    # Permite saber si el proceso que está en la CPU ya finalizó
    def proceso_cpu_finalizo(self):
        proc = self._procesos[self._procesoCPU]
        if not (proc is None):
            return proc.cpu() == 0
        else:
            return False

    # Ejecuta el simulador y su política de funcionamiento
    def ejecutar(self):
        if not self.tiempo_cero():
            print("FIN SIMULACION: imprevisto!")
            return False

        self.imprimir_info_simulacion()

        while True:
            self._reloj = self._reloj + 1  # Incrementamos el reloj

            self.nacen_procesos()
            self.decrementar_tiempo_cpu_proceso()

            if self.proceso_cpu_finalizo():
                proc = self.despachar()
                if proc is None:
                    print("+----+----+")
                    print("FIN SIMULACION: OK")
                    return True
                else:
                    self._procesoCPU = proc
                    self.eliminar_proceso(proc)
            else:
                if not self._despachador.es_apropiativo(self._reloj):
                    self._colaProcesos.append(self._procesoCPU)
                    proc = self.despachar()
                    if not (proc is None) and proc != self._procesoCPU:
                        self.eliminar_proceso(proc)
                        self._procesoCPU = proc
                    else:
                        self.eliminar_proceso(self._procesoCPU)

            self.imprimir_info_simulacion()


# -------------------------------------------------------------------------------
# Programa principal
# -------------------------------------------------------------------------------
def main():
    print("SIMULADOR DE PLANIFICACION DE PROCESOS")
    archivo = input("Archivo con la información de los procesos: ")
    print("Cual politica de planificación simular?")
    print("0. FCFS")
    print("1. Round Robin")
    print("2. SJF")
    print("3. SRTF")
    print("4. Prioridades apropiativo")
    print("5. Prioridades no apropiativo")
    politica = int(input("> "))
    q = 1
    if politica == 1:
        q = int(input("Cual es el quantum para el algoritmo: "))
    planificadores = [fcfs.FCFS(), round_robin.RoundRobin(q),
                      sjf.SJF(), srtf.SRTF(),
                      prioridades.PrioridadesApropiativo(),
                      prioridades.PrioridadesNoApropiativo()]
    despachador = planificadores[politica]
    sim = Simulador(despachador)
    sim.leer_configuracion(archivo)
    sim.ejecutar()


main()
