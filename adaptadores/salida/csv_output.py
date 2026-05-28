import csv
from dominio.puertos import PuertoObservador


class SalidaCSV(PuertoObservador):
    def __init__(self, ruta: str = "resultados.csv"):
        self._ruta = ruta
        self._archivo = None
        self._writer = None

    def al_iniciar(self, config) -> None:
        self._archivo = open(self._ruta, mode="w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._archivo)
        self._writer.writerow([
            "angulo_deg", "v0", "masa", "alcance",
            "altura_max", "tiempo_vuelo", "error_energia",
        ])

    def al_aterrizar(self, resultado) -> None:
        self._writer.writerow([
            round(resultado.angulo_deg, 4),
            round(resultado.v0, 4),
            round(resultado.masa, 4),
            round(resultado.alcance, 4),
            round(resultado.altura_max, 4),
            round(resultado.tiempo_vuelo, 4),
            round(resultado.error_energia, 6),
        ])

    def al_finalizar(self, resultados) -> None:
        if self._archivo:
            self._archivo.close() 