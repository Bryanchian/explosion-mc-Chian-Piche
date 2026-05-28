import math
import pytest
from dominio.modelos import Proyectil
from dominio.patrones.estrategia import Euler, Verlet
from dominio.patrones.fabrica import FabricaLigero 

@pytest.mark.parametrize("angulo_deg", [30,45,60,75])
def test_alcance_vs_analitico(angulo_deg):
    v0, g= 20.0, 9.8
    p = FabricaLigero().crear(angulo_deg, v0)
    dt = 0.02
    euler = Euler()
    while True:
        x_prev, y_prev = p.x, p.y
        euler.paso(p, dt, g)
        if p.y < 0 and p.x != 0:
            f = y_prev / (y_prev - p.y) 
            x_imp = x_prev + f * (p.x - x_prev) 
            break
    
    R_teorico = (v0**2)* math.sin(2*math.radians(angulo_deg)) / g
    assert abs(x_imp - R_teorico) / R_teorico < 0.01
    

def test_verlet_conserva_mejor_energia_que_euler():
    from dominio.patrones.fabrica import FabricaLigero
    def error_energia(estrategia):
        p = FabricaLigero().crear(45, 20)
        e0 = p.energia_total(9.8)
       
        for _ in range(500):
            estrategia.paso(p, 0.05, 9.8)
            if p.y < 0: break
        
        return abs(p.energia_total(9.8) - e0) / abs(e0)
    assert error_energia(Verlet()) < error_energia(Euler()) 