import math
import inspect
import ast
import textwrap
import pytest

from dominio.modelos import ConfigExplosion, Proyectil
from dominio.puertos import PuertoObservador
from dominio.patrones.fabrica import FabricaLigero, FabricaConArrastre

def test_fabrica_ligero_crea_proyectil_correcto():
    p = FabricaLigero().crear(45, 20)
    assert isinstance(p, Proyectil)
    assert p.masa == 0.5
    assert p.coef_arrastre == 0.0


def test_velocidad_inicial_correcta():
    p = FabricaLigero().crear(45, 20.0)
    v = math.sqrt(p.vx ** 2 + p.vy ** 2)
    assert abs(v - 20.0) < 1e-9


def test_sin_if_en_fabrica():
    """FabricaLigero.crear no debe contener ningún if/elif."""
    src = textwrap.dedent(inspect.getsource(FabricaLigero.crear))
    ifs = [n for n in ast.walk(ast.parse(src)) if isinstance(n, ast.If)]
    assert len(ifs) == 0
    
@pytest.fixture
def config_minima():
    return ConfigExplosion(n_proyectiles=20, v_min=10, v_max=20, semilla=7)

from dominio.patrones.observador import MonitorEstadisticas

@pytest.fixture
def motor_euler():
    monitor = MonitorEstadisticas()
    motor = Explosion(FabricaLigero(), Euler(), [monitor])
    return motor, monitor