import math
from dominio.puertos import PuertoObservador


class MonitorEstadisticas(PuertoObservador):
    def __init__(self):
        self._alcances: list[float] = []
        self._altura_max: float = 0.0

    def al_aterrizar(self, resultado) -> None:
        self._alcances.append(resultado.alcance)
        if resultado.altura_max > self._altura_max:
            self._altura_max = resultado.altura_max

    def resumen(self) -> dict:
        if not self._alcances:
            return {}

        n = len(self._alcances)
        avg = sum(self._alcances) / n
        std = math.sqrt(sum((x - avg) ** 2 for x in self._alcances) / n)

        return {
            "n": n,
            "alcance_max": max(self._alcances),
            "alcance_min": min(self._alcances),
            "promedio": avg,
            "desv_std": std,
            "altura_max": self._altura_max,
        }