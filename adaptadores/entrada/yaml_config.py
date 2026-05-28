import yaml
from dominio.modelos import ConfigExplosion
from dominio.puertos import PuertoEntrada


class YAMLConfig(PuertoEntrada):
    def __init__(self, ruta: str = "config.yaml"):
        # Guardamos la ruta del archivo YAML
        self.ruta = ruta

    def obtener_config(self) -> ConfigExplosion:
        try: # Abrimos y leemos el archivo YAML
            with open(self.ruta, "r") as f:
                # safe_load convierte el YAML en un diccionario de Python
                data = yaml.safe_load(f)
        except FileNotFoundError:
            # Si no existe el archivo usamos valores por defecto
            return ConfigExplosion()
        # Extraemos cada seccion del diccionario
        # El {} evita errores si falta alguna seccion
        sim = data.get("simulacion", {})
        viz = data.get("visualizacion", {})
        dist = data.get("distribucion", {})
        ejec = data.get("ejecucion", {})
        # Extraemos las subsecciones de distribucion
        ang = dist.get("angulo", {})
        vel = dist.get("velocidad", {})
        # Construimos ConfigExplosion con los valores del YAML
        # Cada get tiene un valor por defecto si la clave no existe
        return ConfigExplosion(
            n_proyectiles=sim.get("n_proyectiles", 300),
            v_min=sim.get("v_min", 5.0),
            v_max=sim.get("v_max", 30.0),
            g=sim.get("g", 9.8),
            dt=sim.get("dt", 0.04),
            semilla=sim.get("semilla", 42),
            trail_length=viz.get("trail", 18),
            tipo=sim.get("tipo", "ligero"),
            metodo=sim.get("metodo", "euler"),
            salida=sim.get("salida", "animacion"),
            dist_angulo=ang.get("tipo", "uniforme"),
            angulo_media=ang.get("media", 90.0),
            angulo_sigma=ang.get("sigma", 20.0),
            angulo_kappa=ang.get("kappa", 6.0),
            dist_velocidad=vel.get("tipo", "uniforme"),
            vel_media=vel.get("media", 12.0),
            vel_sigma=vel.get("sigma", 4.0),
            modo_ejecucion=ejec.get("modo", "secuencial"),
            workers=ejec.get("workers", None),
        )