"""Generación de gráficos estáticos para análisis."""

from __future__ import annotations

from pathlib import Path

import matplotlib

# Usar backend no-interactivo (debe ir antes de importar pyplot)
matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from inversion_apalancada.config import META, PLOT_DPI, PLOT_FIGSIZE, PLOT_STYLE, STRATEGIES  # noqa: E402


def generate_charts(resultados: dict[str, list[float]], output_dir: Path) -> list[Path]:
    """Genera 4 gráficos PNG de análisis del patrimonio final.

    Args:
        resultados: Dict con key=estrategia, value=lista de patrimonios finales
        output_dir: Directorio donde guardar los PNGs

    Returns:
        Lista de rutas de archivos generados
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Aplicar estilo
    plt.style.use(PLOT_STYLE)

    guardados = []

    # ── Gráfico 1: Histograma de densidad ──
    fig, ax = plt.subplots(figsize=PLOT_FIGSIZE)
    colores = []
    datos_list = []
    labels_list = []

    for key in STRATEGIES:
        datos_list.append(resultados[key])
        labels_list.append(STRATEGIES[key]["label"])
        colores.append(STRATEGIES[key]["color"])

    for datos, color, label in zip(datos_list, colores, labels_list):
        ax.hist(datos, bins=40, alpha=0.6, label=label, color=color, density=True)

    ax.axvline(META, color="black", linestyle="--", linewidth=2, label="Meta $30MM", zorder=5)
    ax.set_xlabel("Patrimonio Neto Final ($)", fontsize=12)
    ax.set_ylabel("Densidad", fontsize=12)
    ax.set_title("Distribución del Patrimonio Neto Final", fontsize=14, fontweight="bold")
    ax.legend(loc="upper right", fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x/1e6:.1f}M"))

    path1 = output_dir / "01_histogram.png"
    fig.savefig(path1, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    guardados.append(path1)

    # ── Gráfico 2: Box plot ──
    fig, ax = plt.subplots(figsize=PLOT_FIGSIZE)
    datos_box = [resultados[key] for key in STRATEGIES]
    labels_box = [STRATEGIES[key]["label"] for key in STRATEGIES]
    colores_box = [STRATEGIES[key]["color"] for key in STRATEGIES]

    bp = ax.boxplot(datos_box, tick_labels=labels_box, patch_artist=True)
    for patch, color in zip(bp["boxes"], colores_box):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    ax.axhline(META, color="black", linestyle="--", linewidth=2, label="Meta $30MM", zorder=5)
    ax.set_ylabel("Patrimonio Neto Final ($)", fontsize=12)
    ax.set_title("Comparación por Cuartiles", fontsize=14, fontweight="bold")
    ax.tick_params(axis="x", rotation=15)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x/1e6:.0f}M"))

    path2 = output_dir / "02_boxplot.png"
    fig.savefig(path2, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    guardados.append(path2)

    # ── Gráfico 3: CDF (Función de Distribución Acumulativa) ──
    fig, ax = plt.subplots(figsize=PLOT_FIGSIZE)

    for key in STRATEGIES:
        valores = np.array(resultados[key])
        valores_sorted = np.sort(valores)
        prob_acum = np.arange(1, len(valores_sorted) + 1) / len(valores_sorted)
        ax.plot(valores_sorted, prob_acum, label=STRATEGIES[key]["label"], color=STRATEGIES[key]["color"], linewidth=2)

    ax.axvline(META, color="black", linestyle="--", alpha=0.7, linewidth=2, label="Meta $30MM")
    ax.set_xlabel("Patrimonio Neto ($)", fontsize=12)
    ax.set_ylabel("Probabilidad Acumulativa", fontsize=12)
    ax.set_title("Función de Distribución Acumulativa", fontsize=14, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x/1e6:.0f}M"))

    path3 = output_dir / "03_cdf.png"
    fig.savefig(path3, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    guardados.append(path3)

    # ── Gráfico 4: Riesgo vs Rendimiento ──
    fig, ax = plt.subplots(figsize=PLOT_FIGSIZE)

    for key in STRATEGIES:
        media = np.mean(resultados[key])
        std = np.std(resultados[key])
        ax.scatter(std, media, s=150, color=STRATEGIES[key]["color"], alpha=0.8)
        ax.annotate(
            STRATEGIES[key]["label"],
            (std, media),
            xytext=(10, 10),
            textcoords="offset points",
            fontsize=10,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.7),
        )

    ax.set_xlabel("Riesgo (Desviación Estándar)", fontsize=12)
    ax.set_ylabel("Rendimiento Esperado (Media)", fontsize=12)
    ax.set_title("Frontera Riesgo-Rendimiento", fontsize=14, fontweight="bold")
    ax.grid(True, alpha=0.3)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x/1e6:.0f}M"))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f"${x/1e6:.0f}M"))

    path4 = output_dir / "04_risk_return.png"
    fig.savefig(path4, dpi=PLOT_DPI, bbox_inches="tight")
    plt.close(fig)
    guardados.append(path4)

    return guardados
