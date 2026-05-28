import random
import math

from dominio.modelos import ConfigExplosion, ResultadoProyectil
from dominio.puertos import PuertoFabrica, PuertoEstrategia, PuertoObservador


class Explosion:

    def __init__(
        self,
        fabrica: PuertoFabrica,
        estrategia: PuertoEstrategia,
        observadores: list[PuertoObservador] | None = None,
    ):
        self._fabrica = fabrica
        self._estrategia = estrategia
        self._observadores = list(observadores or [])

    def _generar_angulo(self, rng: random.Random, config: ConfigExplosion) -> float:
        
        if config.dist_angulo == "normal":
            return rng.gauss(config.angulo_media, config.angulo_sigma)


        if config.dist_angulo == "vonmises":
            mu = math.radians(config.angulo_media)
            return math.degrees(rng.vonmisesvariate(mu, config.angulo_kappa))
        
        return rng.uniform(0.0, 360.0)

    def _generar_velocidad(self, rng: random.Random, config: ConfigExplosion) -> float:

        if config.dist_velocidad == "normal":
            v = rng.gauss(config.vel_media, config.vel_sigma)
            return max(config.v_min, min(config.v_max, v))

        if config.dist_velocidad == "exponencial":
            v = rng.expovariate(1.0 / config.vel_media)
            return max(config.v_min, min(config.v_max, v))
        
        return rng.uniform(config.v_min, config.v_max)


    def ejecutar(self, config: ConfigExplosion) -> tuple[list, list]:
        rng = random.Random(config.semilla)
        condiciones = [
            (
                self._generar_angulo(rng, config),
                self._generar_velocidad(rng, config),
            )
            for _ in range(config.n_proyectiles)
        ]

        for obs in self._observadores:
            obs.al_iniciar(config)

        trayectorias: list = []
        resultados: list = []

        for angulo_deg, v0 in condiciones:
            p = self._fabrica.crear(angulo_deg, v0)
            energia_inicial = p.energia_total(config.g)
            trayectoria = [(p.x, p.y)]  
            altura_max = 0.0
            tiempo = 0.0
            x_land = 0.0

            while True:

        
                x_prev, y_prev = p.x, p.y
                self._estrategia.paso(p, config.dt, config.g)
                tiempo += config.dt
                if p.y > altura_max:
                    altura_max = p.y
                trayectoria.append((p.x, p.y))
                if p.y < 0:
                    denom = y_prev - p.y
                    f = y_prev / denom if abs(denom) > 1e-12 else 0.0
                    x_land = x_prev + f * (p.x - x_prev)
                    break

                if tiempo > 2000:
                    x_land = p.x
                    break

            energia_final = p.energia_total(config.g)

            # esta es la descripcion del proyectil
            resultado = ResultadoProyectil(
                angulo_deg=angulo_deg,
                v0=v0,
                masa=p.masa,
                alcance=x_land,
                altura_max=altura_max,
                tiempo_vuelo=tiempo,
                energia_inicial=energia_inicial,
                energia_final=energia_final,
                trayectoria=trayectoria,
            )

            # guardar trayectoria
            trayectorias.append(trayectoria)
            resultados.append(resultado)
            for obs in self._observadores:
                obs.al_aterrizar(resultado)

        for obs in self._observadores:
            obs.al_finalizar(resultados)
        return trayectorias, resultados