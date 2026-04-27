"""Simulación Monte Carlo de estrategias de inversión."""

from __future__ import annotations

import math

import numpy as np

from inversion_apalancada.config import (
    I_CRED,
    N_MESES,
    N_SIMULACIONES,
    P_INICIAL,
    PMT,
    STRATEGIES,
)


def pago_teorico(pv: float, i: float, n: int) -> float:
    """Calcula el pago mensual de un crédito (anualidad)."""
    if i == 0:
        return pv / n
    return pv * i / (1 - (1 + i) ** (-n))


def solve_rate_from_pmt(
    pv: float,
    pmt: float,
    n: int,
    lo: float = 0.0,
    hi: float = 0.05,
    tol: float = 1e-12,
    maxit: int = 200,
) -> float:
    """Encuentra la tasa mensual del crédito usando bisección."""
    while pago_teorico(pv, hi, n) < pmt and hi <= 1.0:
        hi *= 2

    for _ in range(maxit):
        mid = (lo + hi) / 2
        p_mid = pago_teorico(pv, mid, n)
        if abs(p_mid - pmt) < tol:
            return mid
        if p_mid < pmt:
            lo = mid
        else:
            hi = mid

    return (lo + hi) / 2


def amortizacion(pv: float, i: float, n: int, pmt: float) -> np.ndarray:
    """Calcula el vector de saldos de deuda (n+1 elementos: t=0 hasta t=n)."""
    if pv <= 0 or i < 0 or n <= 0 or pmt <= 0:
        raise ValueError("Todos los parámetros deben ser positivos")
    if pmt <= pv * i:
        raise ValueError(
            f"El pago mensual ({pmt:,.0f}) es insuficiente "
            f"para cubrir los intereses ({pv * i:,.0f})"
        )

    saldo = pv
    saldos = [pv]

    for periodo in range(n):
        interes = saldo * i
        abono_capital = pmt - interes
        nuevo_saldo = saldo - abono_capital

        if nuevo_saldo <= 0.01:
            saldos.append(0.0)
            for _ in range(periodo + 1, n):
                saldos.append(0.0)
            break
        else:
            saldo = nuevo_saldo
            saldos.append(saldo)

    return np.array(saldos)


def inversion_estocastica(
    inicial: float,
    r_anual: float,
    volatilidad_anual: float,
    tac_anual: float,
    n: int,
    aporte_mensual: float = 0.0,
    df: int = 5,
) -> np.ndarray:
    """Simula una trayectoria de inversión con retornos t-Student (colas gruesas).

    Args:
        inicial: Capital inicial
        r_anual: Rentabilidad anual nominal
        volatilidad_anual: Volatilidad anual
        tac_anual: Tasa Anual de Costos
        n: Número de períodos (meses)
        aporte_mensual: Aporte adicional cada mes
        df: Grados de libertad para distribución t-Student (menor = colas más gruesas)

    Returns:
        Array de n+1 valores (inicial + n períodos)
    """
    r_anual_neto = r_anual - tac_anual
    i_promedio_neto = r_anual_neto / 12
    volatilidad_mensual = volatilidad_anual / math.sqrt(12)

    # Escalamiento de t-Student para tener la volatilidad deseada
    escala_t = volatilidad_mensual * math.sqrt((df - 2) / df) if df > 2 else volatilidad_mensual
    retornos_t = np.random.standard_t(df, n) * escala_t + i_promedio_neto

    valores = [inicial]
    v = inicial
    for ret in retornos_t:
        v = v * (1 + ret) + aporte_mensual
        valores.append(v)

    return np.array(valores)


def _simular_trayectoria(key: str, fund, leveraged: bool, saldos_deuda: np.ndarray, df: int) -> np.ndarray:
    """Simula una trayectoria para una estrategia."""
    if leveraged:
        inv = inversion_estocastica(P_INICIAL, fund.r_anual, fund.volatilidad, fund.tac, N_MESES, 0.0, df)
        return inv - saldos_deuda
    else:
        return inversion_estocastica(0.0, fund.r_anual, fund.volatilidad, fund.tac, N_MESES, PMT, df)


def ejecutar_simulacion_completa(
    n_sim: int = N_SIMULACIONES, df: int = 5, seed: int | None = None
) -> tuple[dict[str, dict[str, np.ndarray]], dict[str, list[float]]]:
    """Ejecuta simulaciones y retorna estadísticas mes a mes + valores finales.

    Una sola corrida que produce ambos resultados necesarios:
    - Estadísticas agregadas por mes (para D3 JSON)
    - Distribución de valores finales (para charts estáticos)

    Returns:
        Tupla (estadisticas, resultados_finales):
        - estadisticas: dict por estrategia con promedio, p10, p90, min, max (arrays mes a mes)
        - resultados_finales: dict por estrategia con lista de patrimonios finales
    """
    if seed is not None:
        np.random.seed(seed)

    trayectorias = {key: np.zeros((n_sim, N_MESES + 1)) for key in STRATEGIES}
    saldos_deuda = amortizacion(P_INICIAL, I_CRED, N_MESES, PMT)

    for i in range(n_sim):
        for key, config in STRATEGIES.items():
            trayectorias[key][i] = _simular_trayectoria(
                key, config["fund"], config["leveraged"], saldos_deuda, df
            )

    # Estadísticas mes a mes
    estadisticas = {}
    for key, datos in trayectorias.items():
        estadisticas[key] = {
            "promedio": np.mean(datos, axis=0),
            "p10": np.percentile(datos, 10, axis=0),
            "p90": np.percentile(datos, 90, axis=0),
            "min": np.min(datos, axis=0),
            "max": np.max(datos, axis=0),
        }

    # Valores finales (columna del último mes)
    resultados_finales = {key: trayectorias[key][:, -1].tolist() for key in STRATEGIES}

    return estadisticas, resultados_finales


def ejecutar_simulaciones_finales(n_sim: int = N_SIMULACIONES, df: int = 5) -> dict[str, list[float]]:
    """Ejecuta simulaciones y retorna solo los valores finales (mes 60)."""
    _, resultados = ejecutar_simulacion_completa(n_sim=n_sim, df=df)
    return resultados


def generar_estadisticas_completas(
    n_sim: int = N_SIMULACIONES, df: int = 5, seed: int | None = None
) -> dict[str, dict[str, np.ndarray]]:
    """Genera estadísticas mes a mes (promedio, P10, P90, min, max) para cada estrategia."""
    estadisticas, _ = ejecutar_simulacion_completa(n_sim=n_sim, df=df, seed=seed)
    return estadisticas
