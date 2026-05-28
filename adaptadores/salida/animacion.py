import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from matplotlib.collections import LineCollection

from dominio.puertos import PuertoSalida


class SalidaAnimacion(PuertoSalida):

    def mostrar(self, config, trayectorias, resultados) -> None:
        trail = config.trail_length

        fig = plt.figure(figsize=(14, 7), facecolor="#0a0f0a")
        gs = gridspec.GridSpec(
            2, 2, figure=fig,
            width_ratios=[2.2, 1],
            hspace=0.45, wspace=0.35,
        )
        ax_t = fig.add_subplot(gs[:, 0])
        ax_h = fig.add_subplot(gs[0, 1])
        ax_s = fig.add_subplot(gs[1, 1])

        BG, GREEN, ORANGE = "#0a0f0a", "#00ff41", "#ff8800"
        DIM = "#003300"

        for ax in (ax_t, ax_h, ax_s):
            ax.set_facecolor(BG)
            ax.tick_params(colors=GREEN, labelsize=7)
            for sp in ax.spines.values():
                sp.set_edgecolor(DIM)

        all_x = [p[0] for tray in trayectorias for p in tray]
        all_y = [p[1] for tray in trayectorias for p in tray]
        xpad = max((max(all_x) - min(all_x)) * 0.06, 5)
        ypad = max(all_y) * 0.10

        ax_t.set_xlim(min(all_x) - xpad, max(all_x) + xpad)
        ax_t.set_ylim(-1, max(all_y) + ypad)
        ax_t.set_xlabel("x (m)", color=GREEN, fontsize=8)
        ax_t.set_ylabel("y (m)", color=GREEN, fontsize=8)
        ax_t.grid(True, color=DIM, alpha=0.4, linewidth=0.5)

        dist_a = config.dist_angulo
        dist_v = config.dist_velocidad
        ax_t.set_title(
            f"EXPLOSIÓN  —  ángulo {dist_a}  ·  vel {dist_v}",
            color=GREEN, fontsize=9,
        )

        alcances = [r.alcance for r in resultados]
        rng_alcances = (min(alcances), max(alcances))
        ax_h.set_xlim(rng_alcances[0] * 1.05, rng_alcances[1] * 1.05)
        ax_h.set_xlabel("alcance (m)", color=GREEN, fontsize=7)
        ax_h.set_ylabel("frecuencia", color=GREEN, fontsize=7)
        ax_h.set_title("distribución de alcances", color=GREEN, fontsize=8)

        ax_s.set_xticks([])
        ax_s.set_yticks([])
        for sp in ax_s.spines.values():
            sp.set_visible(False)

        stats_txt = ax_s.text(
            0.05, 0.95, "",
            transform=ax_s.transAxes,
            color=GREEN, fontsize=8, va="top",
            fontfamily="monospace",
        )

        lc = LineCollection([], colors=GREEN, linewidths=0.8, alpha=0.75)
        ax_t.add_collection(lc)

        impacts, = ax_t.plot([], [], "x", color=ORANGE,
                             markersize=5, markeredgewidth=1.2)
        info_txt = ax_t.text(
            0.01, 0.98, "",
            transform=ax_t.transAxes,
            color=GREEN, fontsize=8, va="top",
        )

        lengths = [len(t) for t in trayectorias]
        max_frames = max(lengths)

        impact_xs: list[float] = []
        impactos_ya: set[int] = set()

        drawn_segments: list = [[] for _ in trayectorias]

        def update(frame: int):
            en_vuelo = 0
            aterrizados = 0
            segments = []

            for i, tray in enumerate(trayectorias):
                end = min(frame + 1, lengths[i])

                # Acumular puntos permanentes
                if end > len(drawn_segments[i]):
                    drawn_segments[i] = tray[:end]

                pts = drawn_segments[i]
                if len(pts) >= 2:
                    segments.append(pts)

                if frame >= lengths[i] - 1:
                    aterrizados += 1
                    if i not in impactos_ya:
                        impactos_ya.add(i)
                        impact_xs.append(resultados[i].alcance)
                else:
                    en_vuelo += 1

            lc.set_segments(segments)
            impacts.set_data(impact_xs, [0.0] * len(impact_xs))

            t_sim = frame * config.dt
            info_txt.set_text(
                f"t = {t_sim:.1f} s   "
                f"vuelo: {en_vuelo}   tierra: {aterrizados}"
            )

            if aterrizados > 1 and (frame % 5 == 0 or frame == max_frames - 1):
                ax_h.cla()
                ax_h.set_facecolor(BG)
                ax_h.tick_params(colors=GREEN, labelsize=7)
                for sp in ax_h.spines.values():
                    sp.set_edgecolor(DIM)
                ax_h.set_xlabel("alcance (m)", color=GREEN, fontsize=7)
                ax_h.set_ylabel("frecuencia", color=GREEN, fontsize=7)
                ax_h.set_title("distribución de alcances", color=GREEN, fontsize=8)
                datos = [resultados[i].alcance for i in range(len(trayectorias))
                         if frame >= lengths[i] - 1]
                n_bins = min(40, max(8, len(datos) // 6))
                ax_h.hist(datos, bins=n_bins,
                          color="#00aa33", edgecolor=DIM,
                          range=rng_alcances)

            if aterrizados > 0:
                datos_stats = [resultados[i].alcance
                               for i in range(len(trayectorias))
                               if frame >= lengths[i] - 1]
                avg = sum(datos_stats) / len(datos_stats)
                stats_txt.set_text(
                    f"proyectiles : {aterrizados}\n\n"
                    f"máximo      : {max(datos_stats):.1f} m\n"
                    f"mínimo      : {min(datos_stats):.1f} m\n"
                    f"promedio    : {avg:.1f} m\n"
                    f"desv_std    : "
                    f"{(sum((x-avg)**2 for x in datos_stats)/len(datos_stats))**0.5:.1f} m"
                )

        anim = FuncAnimation(
            fig, update,
            frames=max_frames,
            interval=20,
            blit=False,
            repeat=False,
        )
        plt.show()