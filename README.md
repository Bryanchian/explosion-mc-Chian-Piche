# Explosión Monte Carlo — Laboratorio de Simulación
**Integrantes:** Bryan Chian · Pedro Piche
## Descripción
Simulación Monte Carlo de una explosión: N proyectiles con condiciones iniciales
aleatorias vuelan bajo gravedad y se animan en tiempo real. Implementa los patrones
Factory Method, Strategy y Observer dentro de una arquitectura hexagonal.
## Instalación y uso rápido
```bash
make install # instala dependencias
make run # animación con 300 proyectiles
make run-verlet # integrador de Verlet
make run-luna # gravedad lunar (g = 1.62 m/s²)
make run-csv # exportar CSV sin animación
make test # todos los tests
make test-pure # tests del dominio sin numpy instalado
```
## Opciones de línea de comandos
| Opción | Tipo | Default | Descripción |
|--------|------|---------|-------------|
| `--n` | int | 300 | Número de proyectiles |
| `--g` | float | 9.8 | Gravedad (m/s²) |
| `--tipo` | ligero/pesado/arrastre | ligero | Tipo de proyectil |
| `--metodo` | euler/verlet | euler | Integrador numérico |
| `--salida` | animacion/csv/ambos | animacion | Modo de salida |
| `--dist-angulo` | uniforme/normal/vonmises | uniforme | Distribución de ángulos |