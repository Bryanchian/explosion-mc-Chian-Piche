def test_monitor_recibe_todos_los_aterrizajes(config_minima, motor_euler):
    motor, monitor = motor_euler
    motor.ejecutar(config_minima)
    assert monitor.resumen()["n"] == config_minima.n_proyectiles

def test_resumen_tiene_claves_esperadas(config_minima, motor_euler):
    motor, monitor = motor_euler
    motor.ejecutar(config_minima)
    for clave in ("n", "alcance_max", "alcance_min", "promedio", "desv_std"):
        assert clave in monitor.resumen()
        
from dominio.puertos import PuertoObservador
from dominio.modelos import ConfigExplosion
from dominio.explosion import Explosion
from dominio.patrones.fabrica import FabricaLigero 
from dominio.patrones.estrategia import Euler  

def test_nuevo_observador_sin_modficar_motor():
    eventos = []
    class ObsCustom(PuertoObservador):
        def al_aterrizar(self, r): eventos.append(r.alcance)
            
            
    config = ConfigExplosion(n_proyectiles=10, v_min=10, v_max=20, semilla=1)
    motor = Explosion(FabricaLigero(), Euler(), [ObsCustom()])
    motor.ejecutar(config)
    assert len(eventos) == 10