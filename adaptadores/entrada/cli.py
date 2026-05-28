import argparse
from dominio.modelos import ConfigExplosion
from dominio.puertos import PuertoEntrada
from adaptadores.entrada.yaml_config import YAMLConfig


class EntradaCLI(PuertoEntrada):
    def obtener_config(self)-> ConfigExplosion:
        # Cargamos los valores por defecto desde config.yaml
        # Asi el usuario puede cambiar parametros sin tocar el codigo
        base = YAMLConfig().obtener_config()
    # Creamos el parser que lee los argumentos de la terminal
        parser = argparse.ArgumentParser(
            description="Simulación Monte Carlo de una explosión"
        )

        # Cada argumento tiene un tipo y un valor por defecto del YAML
        parser.add_argument("--n", type=int, default=base.n_proyectiles)
        parser.add_argument("--v-min", type=float, default=base.v_min)
        parser.add_argument("--v-max", type=float, default=base.v_max)
        parser.add_argument("--g", type=float, default=base.g)
        parser.add_argument("--dt", type=float, default=base.dt)
        parser.add_argument("--semilla", type=int, default=base.semilla)
        # choices limita las opciones validas para cada argumento
        parser.add_argument(
            "--tipo",
            choices=["ligero", "pesado", "arrastre"],
            default=base.tipo,
        )
        parser.add_argument(
            "--metodo",
            choices=["euler", "verlet"],
            default=base.metodo,
        )
        parser.add_argument(
            "--salida",
            choices=["animacion", "csv", "ambos"],
            default=base.salida,
        )
        parser.add_argument(
            "--dist-angulo",
            choices=["uniforme", "normal", "vonmises"],
            default=base.dist_angulo,
        )
        parser.add_argument(
            "--dist-vel",
            choices=["uniforme", "normal", "exponencial"],
            default=base.dist_velocidad,
        )
        # Lee lo que el usuario escribio en la terminal
        args = parser.parse_args()
        # Construye y devuelve el ConfigExplosion con los valores finales
        return ConfigExplosion(
            n_proyectiles=args.n,
            v_min=args.v_min,
            v_max=args.v_max,
            g=args.g,
            dt=args.dt,
            semilla=args.semilla,
            trail_length=base.trail_length,
            tipo=args.tipo,
            metodo=args.metodo,
            salida=args.salida,
            dist_angulo=args.dist_angulo,
            angulo_media=base.angulo_media,
            angulo_sigma=base.angulo_sigma,
            angulo_kappa=base.angulo_kappa,
            dist_velocidad=args.dist_vel,
            vel_media=base.vel_media,
            vel_sigma=base.vel_sigma,
            modo_ejecucion=base.modo_ejecucion,
            workers=base.workers,
        )