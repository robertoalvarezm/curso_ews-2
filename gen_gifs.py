"""Genera las animaciones (GIF) de la Parte III del curso.

Figuras recreadas siguiendo la exposición de Myrvoll-Nilsen (figs. 1-3) y la
figura 3 de Alvarez-Martinez & Miramontes (2026), Entropy 28, 628.
Salida: images/*.gif  (frames PNG -> ffmpeg con paleta optimizada)
"""
import os
import shutil
import subprocess

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

AZUL, ROJO, GRIS, ARENA = "#1f5673", "#b03a2e", "#444444", "#e8e2d5"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
TMP = "/tmp/frames"
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
})


def f(x, h):
    return -x ** 3 + x + h


def V(x, h):
    return x ** 4 / 4 - x ** 2 / 2 - h * x


def fijos(h):
    r = np.roots([-1, 0, 1, h])
    return np.sort(r[np.abs(r.imag) < 1e-6].real)


def a_gif(nombre, fps=12):
    """Convierte /tmp/frames/*.png en un GIF optimizado con ffmpeg."""
    destino = os.path.join(OUT, nombre)
    paleta = "/tmp/paleta.png"
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
         "-i", f"{TMP}/f%04d.png",
         "-vf", "palettegen=max_colors=64:stats_mode=diff", paleta],
        check=True)
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
         "-i", f"{TMP}/f%04d.png", "-i", paleta,
         "-lavfi", "paletteuse=dither=bayer:bayer_scale=3",
         "-loop", "0", destino],
        check=True)
    mb = os.path.getsize(destino) / 1e6
    print(f"  -> {nombre}  ({mb:.2f} MB)")


def limpiar():
    shutil.rmtree(TMP, ignore_errors=True)
    os.makedirs(TMP, exist_ok=True)


# ----------------------------------------------------------------------------
# Figura 1 - tipping inducido por RUIDO
# ----------------------------------------------------------------------------
def gif_ntipping():
    print("Figura 1 (N-tipping)")
    limpiar()
    h, sigma, dt, n = 0.15, 0.26, 0.01, 30000
    rng = np.random.default_rng(7)
    x = np.empty(n)
    x[0] = fijos(h)[0]
    for t in range(1, n):
        x[t] = x[t - 1] + dt * f(x[t - 1], h) + sigma * np.sqrt(dt) * rng.standard_normal()
    r = fijos(h)
    salto = int(np.argmax(x > r[1]))
    print(f"   cruce en t = {salto*dt:.1f}")

    xx = np.linspace(-1.8, 1.8, 400)
    Vxx = V(xx, h)
    NF = 130
    cortes = np.linspace(400, n, NF).astype(int)
    tt = np.arange(n) * dt

    for k, c in enumerate(cortes):
        fig, ax = plt.subplots(1, 2, figsize=(8.6, 3.0),
                               gridspec_kw={"width_ratios": [1, 1.85]})
        ax[0].fill_between(xx, Vxx, -1.2, color=ARENA, alpha=.55, lw=0)
        ax[0].plot(xx, Vxx, color=GRIS, lw=2)
        ax[0].plot(r[[0, 2]], V(r[[0, 2]], h), 'o', color=AZUL, ms=8)
        ax[0].plot(r[1], V(r[1], h), 'o', color=ROJO, ms=8)
        xc = x[c - 1]
        ax[0].plot([xc], [V(xc, h)], 'o', ms=13, color="#f0a202",
                   markeredgecolor="#7a5200", zorder=5)
        ax[0].set(xlabel="x", ylabel="V(x)", ylim=(Vxx.min() - .08, .55),
                  title=f"Potencial FIJO  (h = {h})")

        ax[1].plot(tt[:c], x[:c], lw=.5, color=GRIS)
        ax[1].plot(tt[c - 1], xc, 'o', ms=6, color="#f0a202",
                   markeredgecolor="#7a5200", zorder=5)
        ax[1].axhline(r[1], color=ROJO, ls="--", lw=1.1)
        ax[1].axhline(r[0], color=AZUL, ls=":", lw=1)
        ax[1].axhline(r[2], color=AZUL, ls=":", lw=1)
        ax[1].set(xlim=(0, n * dt), ylim=(-1.9, 1.9), xlabel="t", ylabel="x(t)",
                  title="Nada cambia... hasta que el ruido cruza la barrera")
        if c > salto:
            ax[1].text(.02, .93, "salto por ruido", transform=ax[1].transAxes,
                       color=ROJO, fontsize=9, fontweight="bold")
        fig.tight_layout()
        fig.savefig(f"{TMP}/f{k:04d}.png", dpi=95)
        plt.close(fig)
    a_gif("fig1-ntipping.gif", fps=14)


# ----------------------------------------------------------------------------
# Figura 2 - el potencial antes, en y despues del pliegue
# ----------------------------------------------------------------------------
def gif_potencial():
    print("Figura 2 (potencial deformandose)")
    limpiar()
    hc = 2 / np.sqrt(27)
    hs = np.concatenate([np.linspace(-0.05, 0.62, 90),
                         np.linspace(0.62, -0.05, 50)])
    xx = np.linspace(-1.75, 1.75, 500)
    canica = fijos(hs[0])[0]          # arranca en el pozo izquierdo

    for k, hh in enumerate(hs):
        for _ in range(40):           # relajación cuasi-estática hacia el mínimo
            canica += 0.02 * f(canica, hh)
        fig, ax = plt.subplots(figsize=(6.6, 3.4))
        Vxx = V(xx, hh)
        ax.fill_between(xx, Vxx, -1.2, color=ARENA, alpha=.55, lw=0)
        ax.plot(xx, Vxx, color=GRIS, lw=2.4)
        r = fijos(hh)
        r = r[np.insert(np.diff(r) > 1e-3, 0, True)] if len(r) > 1 else r
        if len(r) == 3:
            ax.plot(r[[0, 2]], V(r[[0, 2]], hh), 'o', color=AZUL, ms=9)
            ax.plot(r[1], V(r[1], hh), 'o', color=ROJO, ms=9)
        elif len(r) == 2:
            ax.plot(r[1], V(r[1], hh), 'o', color=AZUL, ms=9)
            ax.plot(r[0], V(r[0], hh), 'o', color=ROJO, ms=10, mfc="white", mew=2.2)
        else:
            ax.plot(r[0], V(r[0], hh), 'o', color=AZUL, ms=9)
        if hh < hc - 0.004:
            etq, col = "(a) antes del pliegue:  h < $h_c$", AZUL
        elif hh <= hc + 0.004:
            etq, col = "(b) EN el pliegue:  h = $h_c$", ROJO
        else:
            etq, col = "(c) después:  h > $h_c$  (el pozo izquierdo ya no existe)", ROJO
        ax.plot([canica], [V(canica, hh)], 'o', ms=13, color="#f0a202",
                markeredgecolor="#7a5200", zorder=6)
        ax.set(xlabel="x", ylabel="V(x)", ylim=(-1.15, 1.0), xlim=(-1.75, 1.75))
        ax.set_title(etq, color=col)
        ax.text(.02, .05, f"h = {hh:+.3f}      $h_c$ = {hc:.3f}",
                transform=ax.transAxes, fontsize=9, color=GRIS)
        fig.tight_layout()
        fig.savefig(f"{TMP}/f{k:04d}.png", dpi=95)
        plt.close(fig)
    a_gif("fig2-potencial.gif", fps=14)


# ----------------------------------------------------------------------------
# Figura 3 - tipping inducido por BIFURCACION
# ----------------------------------------------------------------------------
def gif_btipping():
    print("Figura 3 (B-tipping)")
    limpiar()
    T, dt, sigma = 400.0, 0.05, 0.03
    n = int(T / dt)
    hr = np.linspace(-0.2, 0.6, n)
    rng = np.random.default_rng(1)
    x = np.empty(n)
    x[0] = fijos(hr[0])[0]
    for t in range(1, n):
        x[t] = x[t - 1] + dt * f(x[t - 1], hr[t - 1]) + sigma * np.sqrt(dt) * rng.standard_normal()
    tip = int(np.argmax(x > 0))
    hc = 2 / np.sqrt(27)
    print(f"   salto en h = {hr[tip]:.3f} (h_c = {hc:.3f})")

    hg = np.linspace(-0.6, 0.6, 600)
    lo, mi, up, uni = (np.full(600, np.nan) for _ in range(4))
    for i, hh in enumerate(hg):
        r = fijos(hh)
        if len(r) >= 3:
            lo[i], mi[i], up[i] = r
        else:
            uni[i] = r[-1]

    xx = np.linspace(-1.75, 1.75, 400)
    NF = 130
    cortes = np.linspace(60, n, NF).astype(int)
    tt = np.arange(n) * dt

    for k, c in enumerate(cortes):
        hh = hr[c - 1]
        xc = x[c - 1]
        fig, ax = plt.subplots(1, 3, figsize=(11.2, 3.0),
                               gridspec_kw={"width_ratios": [1, 1.35, 1.35]})
        Vxx = V(xx, hh)
        ax[0].fill_between(xx, Vxx, -1.2, color=ARENA, alpha=.55, lw=0)
        ax[0].plot(xx, Vxx, color=GRIS, lw=2.2)
        r = fijos(hh)
        if len(r) == 3:
            ax[0].plot(r[[0, 2]], V(r[[0, 2]], hh), 'o', color=AZUL, ms=7)
            ax[0].plot(r[1], V(r[1], hh), 'o', color=ROJO, ms=7)
        else:
            ax[0].plot(r[-1], V(r[-1], hh), 'o', color=AZUL, ms=7)
        ax[0].plot([xc], [V(xc, hh)], 'o', ms=12, color="#f0a202",
                   markeredgecolor="#7a5200", zorder=5)
        ax[0].set(xlabel="x", ylabel="V(x)", ylim=(-1.15, 1.0),
                  title=f"El pozo se aplana   (h = {hh:+.3f})")

        ax[1].plot(tt[:c], x[:c], lw=.7, color=GRIS)
        ax[1].plot(tt[c - 1], xc, 'o', ms=6, color="#f0a202",
                   markeredgecolor="#7a5200", zorder=5)
        ax[1].set(xlim=(0, T), ylim=(-1.7, 1.7), xlabel="t", ylabel="x(t)",
                  title="Serie de tiempo")

        for rama in (lo, up, uni):
            ax[2].plot(hg, rama, color=AZUL, lw=2.2)
        ax[2].plot(hg, mi, color=ROJO, lw=2.2, ls="--")
        ax[2].plot(hr[:c], x[:c], lw=.8, color=GRIS)
        ax[2].plot([hh], [xc], 'o', ms=7, color="#f0a202",
                   markeredgecolor="#7a5200", zorder=5)
        ax[2].axvline(hc, color=ROJO, lw=.8, alpha=.6)
        ax[2].set(xlim=(-0.35, 0.62), ylim=(-1.7, 1.7),
                  xlabel="h (parámetro de control)", ylabel="x",
                  title="Diagrama de bifurcación")
        if c > tip:
            ax[1].text(.02, .90, "B-tipping", transform=ax[1].transAxes,
                       color=ROJO, fontsize=9, fontweight="bold")
        fig.tight_layout()
        fig.savefig(f"{TMP}/f{k:04d}.png", dpi=92)
        plt.close(fig)
    a_gif("fig3-btipping.gif", fps=14)


# ----------------------------------------------------------------------------
# Figura 4 - ventanas movil vs expandible  (cf. Fig. 3 de Alvarez & Miramontes)
# ----------------------------------------------------------------------------
def gif_ventanas():
    print("Figura 4 (ventana móvil vs expandible)")
    limpiar()
    from scipy.ndimage import gaussian_filter1d
    from scipy.stats import kendalltau

    dt, sigma, n = 0.05, 0.035, 8000
    # escenario multifase: meseta estable larga + rampa tardía hacia el pliegue
    hr = np.concatenate([np.full(int(.35 * n), -0.2),
                         np.linspace(-0.2, 0.6, n - int(.35 * n))])
    rng = np.random.default_rng(4)
    x = np.empty(n)
    x[0] = fijos(hr[0])[0]
    for t in range(1, n):
        x[t] = x[t - 1] + dt * f(x[t - 1], hr[t - 1]) + sigma * np.sqrt(dt) * rng.standard_normal()
    trans = int(np.argmax(x > 0))
    pre = x[:trans - 30]
    res = pre - gaussian_filter1d(pre, 200, mode="nearest")
    m = len(res)

    w = 800          # ventana móvil (fija)
    burn = 800       # arranque de la expandible
    idx = np.arange(max(w, burn), m)
    var_mov = np.array([res[i - w:i].var() for i in idx])
    var_exp = np.array([res[:i].var() for i in idx])
    tt = idx * dt
    ymin = min(var_mov.min(), var_exp.min()) / 1.6
    ymax = max(var_mov.max(), var_exp.max()) * 1.6
    rmax = 4.2 * res.std()

    NF = 120
    pasos = np.linspace(0, len(idx) - 1, NF).astype(int)
    tp = np.arange(m) * dt

    for k, p in enumerate(pasos):
        i = idx[p]
        fig, ax = plt.subplots(2, 2, figsize=(10.4, 4.6),
                               gridspec_kw={"width_ratios": [1.6, 1]})
        for fila, (a0, b0, etq, col) in enumerate([
                (i - w, i, f"(A) ventana MÓVIL: ancho fijo w = {w}", AZUL),
                (0, i, "(B) ventana EXPANDIBLE: acumula desde el inicio", "#8a5a00")]):
            a = ax[fila, 0]
            a.plot(tp, res, lw=.4, color="#cccccc")
            a.plot(tp[a0:b0], res[a0:b0], lw=.5, color=GRIS)
            a.axvspan(tp[a0], tp[b0 - 1], color=col, alpha=.16, lw=0)
            a.axvline(tp[a0], color=col, lw=1.2)
            a.axvline(tp[b0 - 1], color=col, lw=1.2)
            a.set(ylim=(-rmax, rmax), xlim=(0, tp[-1]), ylabel="residuo")
            a.set_title(etq, color=col)
            if fila == 1:
                a.set_xlabel("t")

            b = ax[fila, 1]
            serie = var_mov if fila == 0 else var_exp
            b.plot(tt[:p + 1], serie[:p + 1], lw=1.7, color=col)
            b.plot(tt[p], serie[p], 'o', ms=5, color=col)
            b.set_yscale("log")
            b.set(xlim=(tt[0], tt[-1]), ylim=(ymin, ymax),
                  ylabel="varianza estimada (log)")
            b.set_title(f"×{serie[p]/serie[0]:.1f} respecto al inicio", color=col)
            if fila == 1:
                b.set_xlabel("t")
        fig.tight_layout()
        fig.savefig(f"{TMP}/f{k:04d}.png", dpi=92)
        plt.close(fig)

    print(f"   tau var movil = {kendalltau(tt, var_mov)[0]:+.2f} | "
          f"expandible = {kendalltau(tt, var_exp)[0]:+.2f}")
    print(f"   amplificacion movil = x{var_mov[-1]/var_mov[0]:.1f} | "
          f"expandible = x{var_exp[-1]/var_exp[0]:.1f}")
    a_gif("fig4-ventanas.gif", fps=12)


if __name__ == "__main__":
    gif_ntipping()
    gif_potencial()
    gif_btipping()
    gif_ventanas()
