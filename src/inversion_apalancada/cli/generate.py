"""Genera assets: JSON para D3 + PNGs de análisis."""

from __future__ import annotations

import json
import logging

from inversion_apalancada.config import (
    CHARTS_DIR,
    DATA_JSON_DIR,
    N_SIMULACIONES,
    STRATEGIES,
)
from inversion_apalancada.simulation import ejecutar_simulacion_completa
from inversion_apalancada.visualization import generate_charts

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def generate() -> None:
    """Orquesta la generación de assets: simulaciones → JSON → PNGs."""
    logger.info("Iniciando generación de assets...")

    # Crear directorios
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    DATA_JSON_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Ejecutar simulaciones (una sola corrida produce ambos resultados)
    logger.info("Ejecutando simulaciones Monte Carlo (%d simulaciones)...", N_SIMULACIONES)
    estadisticas, resultados = ejecutar_simulacion_completa(n_sim=N_SIMULACIONES)

    # 2. Generar PNGs
    logger.info("Generando gráficos PNG...")
    charts_created = generate_charts(resultados, CHARTS_DIR)
    logger.info(f"Gráficos creados: {len(charts_created)} archivos")

    # 3. Exportar JSON para D3
    logger.info("Exportando JSON para visualización D3...")
    json_data = {
        "metadata": {
            "n_simulaciones": N_SIMULACIONES,
            "n_meses": 60,
            "meta": 30_000_000,
            "P_inicial": 27_000_000,
            "pmt": 699_125,
        },
        "strategies": {},
    }

    for key in STRATEGIES:
        json_data["strategies"][key] = {
            "label": STRATEGIES[key]["label"],
            "color": STRATEGIES[key]["color"],
            "promedio": estadisticas[key]["promedio"].tolist(),
            "p10": estadisticas[key]["p10"].tolist(),
            "p90": estadisticas[key]["p90"].tolist(),
            "min": estadisticas[key]["min"].tolist(),
            "max": estadisticas[key]["max"].tolist(),
        }

    json_path = DATA_JSON_DIR / "simulation_stats.json"
    with open(json_path, "w") as f:
        json.dump(json_data, f, indent=2)
    logger.info(f"JSON guardado: {json_path}")

    # Resumen
    logger.info("=== RESUMEN ESTADÍSTICAS FINALES ===")
    for key in STRATEGIES:
        promedio = estadisticas[key]["promedio"][-1] / 1e6
        p10 = estadisticas[key]["p10"][-1] / 1e6
        p90 = estadisticas[key]["p90"][-1] / 1e6
        logger.info(f"{STRATEGIES[key]['label']}: Promedio=${promedio:.1f}M, P10-P90: ${p10:.1f}M-${p90:.1f}M")

    logger.info("Assets generados exitosamente.")


if __name__ == "__main__":
    generate()
