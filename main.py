from dominio.explosion import Explosion
from dominio.patrones.fabrica import FabricaLigero, FabricaPesado, FabricaConArrastre
from dominio.patrones.estrategia import Euler, Verlet
from dominio.patrones.observador import MonitorEstadisticas
from adaptadores.entrada.cli import EntradaCLI
from adaptadores.salida.animacion import SalidaAnimacion
from adaptadores.salida.csv_output import SalidaCSV


def main():
    #configuración 
    config = EntradaCLI().obtener_config()

    #fábrica 
    fabricas = {
        "ligero": FabricaLigero(),
        "pesado": FabricaPesado(),
        "arrastre": FabricaConArrastre(),
    }
    fabrica = fabricas[config.tipo]

    #estrategia
    estrategia = Verlet() if config.metodo == "verlet" else Euler()

    #observadores
    monitor = MonitorEstadisticas()
    observadores = [monitor]

    if config.salida in ("csv", "ambos"):
        observadores.append(SalidaCSV())

    #motor
    motor = Explosion(fabrica, estrategia, observadores)
    trayectorias, resultados = motor.ejecutar(config)

    #resumen en consola
    resumen = monitor.resumen()
    print(f"\n{'─'*40}")
    print(f"  Proyectiles  : {resumen['n']}")
    print(f"  Alcance max  : {resumen['alcance_max']:.2f} m")
    print(f"  Alcance min  : {resumen['alcance_min']:.2f} m")
    print(f"  Promedio     : {resumen['promedio']:.2f} m")
    print(f"  Desv. std    : {resumen['desv_std']:.2f} m")
    print(f"  Altura max   : {resumen['altura_max']:.2f} m")
    print(f"{'─'*40}\n")

    #salida visual
    if config.salida in ("animacion", "ambos"):
        SalidaAnimacion().mostrar(config, trayectorias, resultados)


if __name__ == "__main__":
    main()