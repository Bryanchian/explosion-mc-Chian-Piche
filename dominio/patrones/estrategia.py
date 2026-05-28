from dominio.modelos import Proyectil
from dominio.puertos import PuertoEstrategia

# En esta parte simplemente hacemos el llamado a los metodos de cada estrategia
# Ahora vamos a trabajar en el promedio de las aceleraciones.

class Euler(PuertoEstrategia):
    def paso(self, p: Proyectil, dt: float, g: float) -> None:
        ax = -p.coef_arrastre / p.masa * p.velocidad() * p.vx
        ay = -g - p.coef_arrastre / p.masa * p.velocidad() * p.vy

        p.x += p.vx * dt #aca trabajamos respecto de la velocidad
        p.y += p.vy * dt

        p.vx += ax * dt #aca respecto de la aceleracion
        p.vy += ay * dt

    @property
    def nombre(self) -> str:
        return "Euler (orden 1)"

#ahora vamos a trabajar con una funcion auxiliar para calcular la fuerza de arrastre y la gravedad
class Verlet(PuertoEstrategia):
    def aceleracion(self, p: Proyectil, g: float):
        v = p.velocidad()
        ax = -p.coef_arrastre / p.masa * v * p.vx
        ay = -g - p.coef_arrastre / p.masa * v * p.vy
        return ax, ay
    
    def paso(self, p: Proyectil, dt: float, g: float) -> None:
        ax1, ay1 = self.aceleracion(p, g)

        p.x += p.vx * dt + 0.5 * ax1 * dt**2
        p.y += p.vy * dt + 0.5 * ay1 * dt**2

        ax2, ay2 = self.aceleracion(p, g)

        p.vx += 0.5 * (ax1 + ax2) * dt
        p.vy += 0.5 * (ay1 + ay2) * dt

    @property
    def nombre(self) -> str:
        return "Verlet (orden 2)"