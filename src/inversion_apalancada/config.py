"""Configuración central del proyecto Inversión Apalancada."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

# ── Rutas ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
ASSETS_DIR = PROJECT_ROOT / "viz" / "assets"
CHARTS_DIR = ASSETS_DIR / "charts"
DATA_JSON_DIR = ASSETS_DIR / "data"
VIZ_DIR = PROJECT_ROOT / "viz"

# ── Jekyll ─────────────────────────────────────────────
_jekyll_env = os.getenv("JEKYLL_REPO")
JEKYLL_REPO: Path | None = Path(_jekyll_env) if _jekyll_env else None
JEKYLL_BASE = (JEKYLL_REPO / "proyectos" / "inversion-apalancada") if JEKYLL_REPO else None
JEKYLL_DATA_DIR = (JEKYLL_BASE / "assets" / "data") if JEKYLL_BASE else None
JEKYLL_CHARTS_DIR = (JEKYLL_BASE / "assets" / "charts") if JEKYLL_BASE else None
JEKYLL_CSS_DIR = (JEKYLL_BASE / "assets" / "css") if JEKYLL_BASE else None
JEKYLL_JS_DIR = (JEKYLL_BASE / "assets" / "js") if JEKYLL_BASE else None
JEKYLL_PAGE = (JEKYLL_BASE / "viz.html") if JEKYLL_BASE else None
JEKYLL_PROJECTS_DIR = (JEKYLL_REPO / "_projects") if JEKYLL_REPO else None
JEKYLL_PROJECT_MD = PROJECT_ROOT / "jekyll" / "inversion-apalancada.md"

# ── Parámetros de Simulación ───────────────────────────
P_INICIAL = 27_000_000  # Monto del crédito
N_MESES = 60  # Horizonte de 5 años
PMT = 699_125  # Cuota mensual
META = 30_000_000  # Objetivo financiero
N_SIMULACIONES = 10_000  # Número de simulaciones Monte Carlo
I_CRED = 0.0125  # Tasa de crédito mensual


# ── Fondos Mutuos ──────────────────────────────────────
@dataclass(frozen=True)
class FundParams:
    """Parámetros de un fondo mutuo."""

    name: str
    label: str
    r_anual: float  # Rentabilidad anual
    volatilidad: float  # Volatilidad anual
    tac: float  # Tasa Anual de Costos


FUND_A = FundParams(
    name="agresivo",
    label="Perfil A (Agresivo)",
    r_anual=0.1580,
    volatilidad=0.22,
    tac=0.0100,
)

FUND_C = FundParams(
    name="moderado",
    label="Perfil C (Moderado)",
    r_anual=0.1234,
    volatilidad=0.15,
    tac=0.0085,
)

# ── Estrategias ────────────────────────────────────────
STRATEGIES = {
    "agresivo_apalancado": {
        "fund": FUND_A,
        "leveraged": True,
        "label": "Agresivo Apalancado",
        "color": "#e74c3c",
    },
    "agresivo_sin_apalancamiento": {
        "fund": FUND_A,
        "leveraged": False,
        "label": "Agresivo Sin Apalancamiento",
        "color": "#f39c12",
    },
    "moderado_apalancado": {
        "fund": FUND_C,
        "leveraged": True,
        "label": "Moderado Apalancado",
        "color": "#3498db",
    },
    "moderado_sin_apalancamiento": {
        "fund": FUND_C,
        "leveraged": False,
        "label": "Moderado Sin Apalancamiento",
        "color": "#27ae60",
    },
}

# ── Estilos de Gráficos ────────────────────────────────
PLOT_DPI = 150
PLOT_STYLE = "seaborn-v0_8-whitegrid"
PLOT_FIGSIZE = (14, 7)
