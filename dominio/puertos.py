from abc import ABC, abstractmethod

from dominio.modelos import ConfigExplosion, Proyectil, ResultadoProyectil


class PuertoEntrada(ABC):
    @abstractmethod
    def obtener_config(self) -> ConfigExplosion:
        pass


class PuertoFabrica(ABC):
    @abstractmethod
    def crear(self, angulo_deg: float, v0: float) -> Proyectil:
        pass

    @property
    @abstractmethod
    def nombre(self) -> str:
        pass


class PuertoEstrategia(ABC):
    @abstractmethod
    def paso(self, proyectil: Proyectil, dt: float, g: float) -> None:
        pass

    @property
    @abstractmethod
    def nombre(self) -> str:
        pass


class PuertoObservador(ABC):
    def al_iniciar(self, config: ConfigExplosion) -> None:
        pass

    @abstractmethod
    def al_aterrizar(self, resultado: ResultadoProyectil) -> None:
        pass

    def al_finalizar(self, resultados: list) -> None:
        pass


class PuertoSalida(ABC):
    @abstractmethod
    def mostrar(self, config, trayectorias, resultados) -> None:
        pass