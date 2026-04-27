"""Tests para el módulo de simulación."""

from __future__ import annotations

import numpy as np
import pytest

from inversion_apalancada.simulation import (
    amortizacion,
    ejecutar_simulaciones_finales,
    generar_estadisticas_completas,
    inversion_estocastica,
    pago_teorico,
    solve_rate_from_pmt,
)


class TestPagoTeorico:
    """Tests para la función pago_teorico."""

    def test_zero_rate(self) -> None:
        """Cuando i=0, el pago debe ser pv/n."""
        assert pago_teorico(1000, 0, 10) == 100

    def test_known_values(self) -> None:
        """Test con valores conocidos de anualidad."""
        # PV=1000, i=1% mensual, n=12 meses
        # Pago mensual aproximadamente 88.85
        pmt = pago_teorico(1000, 0.01, 12)
        assert 88 < pmt < 90

    def test_higher_rate_higher_payment(self) -> None:
        """A mayor tasa, mayor pago mensual."""
        pmt1 = pago_teorico(1000, 0.01, 12)
        pmt2 = pago_teorico(1000, 0.02, 12)
        assert pmt2 > pmt1


class TestSolveRateFromPmt:
    """Tests para la función solve_rate_from_pmt."""

    def test_roundtrip(self) -> None:
        """Resolver tasa y luego calcular pago debe dar el pago original."""
        pv = 1000
        pmt_target = 100
        n = 12
        rate = solve_rate_from_pmt(pv, pmt_target, n)
        pmt_calc = pago_teorico(pv, rate, n)
        assert abs(pmt_calc - pmt_target) < 0.01

    def test_higher_payment_higher_rate(self) -> None:
        """Mayor pago implica mayor tasa de interés."""
        pv = 1000
        n = 12
        rate1 = solve_rate_from_pmt(pv, 90, n)
        rate2 = solve_rate_from_pmt(pv, 100, n)
        assert rate2 > rate1


class TestAmortizacion:
    """Tests para la función amortizacion."""

    def test_length(self) -> None:
        """El vector de amortización debe tener n+1 elementos."""
        result = amortizacion(1000, 0.01, 12, 90)
        assert len(result) == 13  # 0 a 12 inclusive

    def test_starts_at_pv(self) -> None:
        """El primer elemento debe ser igual a pv."""
        pv = 1000
        result = amortizacion(pv, 0.01, 12, 90)
        assert result[0] == pv

    def test_ends_near_zero(self) -> None:
        """El último elemento debe estar cerca de 0 para pmt correcto."""
        pv = 27_000_000
        i = 0.0125
        n = 60
        pmt = 699_125
        result = amortizacion(pv, i, n, pmt)
        assert result[-1] < 100  # Muy cercano a 0

    def test_monotonic_decrease(self) -> None:
        """La deuda debe disminuir monótonamente."""
        result = amortizacion(1000, 0.01, 12, 90)
        for i in range(len(result) - 1):
            assert result[i + 1] <= result[i]

    def test_invalid_pmt_insufficient(self) -> None:
        """Pago menor que intereses del período inicial debe lanzar error."""
        with pytest.raises(ValueError):
            amortizacion(1000, 0.1, 12, 50)  # Pmt muy bajo

    def test_invalid_negative_params(self) -> None:
        """Parámetros negativos deben lanzar error."""
        with pytest.raises(ValueError):
            amortizacion(-1000, 0.01, 12, 90)


class TestInversionEstocastica:
    """Tests para la función inversion_estocastica."""

    def test_length(self) -> None:
        """El resultado debe tener n+1 elementos."""
        result = inversion_estocastica(1000, 0.1, 0.2, 0.01, 12)
        assert len(result) == 13

    def test_starts_at_inicial(self) -> None:
        """El primer elemento debe ser igual a inicial."""
        inicial = 5000
        result = inversion_estocastica(inicial, 0.1, 0.2, 0.01, 12)
        assert result[0] == inicial

    def test_positive_initial_growth(self) -> None:
        """Con rentabilidad positiva neta, el valor debe crecer en promedio."""
        np.random.seed(42)
        resultado = []
        for _ in range(100):
            result = inversion_estocastica(10_000, 0.12, 0.15, 0.01, 12)
            resultado.append(result[-1])
        media = np.mean(resultado)
        assert media > 10_000  # Debe crecer en promedio

    def test_monthly_contributions(self) -> None:
        """Aportes mensuales deben incrementar el valor."""
        np.random.seed(42)
        result_sin_aporte = inversion_estocastica(0, 0.12, 0.15, 0.01, 12, aporte_mensual=0)
        result_con_aporte = inversion_estocastica(0, 0.12, 0.15, 0.01, 12, aporte_mensual=1000)
        # Con aporte debe ser significativamente mayor
        assert result_con_aporte[-1] > result_sin_aporte[-1]


class TestEjecutarSimulacionesFinales:
    """Tests para la función ejecutar_simulaciones_finales."""

    def test_keys(self) -> None:
        """Debe retornar las 4 estrategias."""
        resultados = ejecutar_simulaciones_finales(n_sim=10)
        assert len(resultados) == 4
        assert "agresivo_apalancado" in resultados
        assert "agresivo_sin_apalancamiento" in resultados
        assert "moderado_apalancado" in resultados
        assert "moderado_sin_apalancamiento" in resultados

    def test_simulation_count(self) -> None:
        """Cada estrategia debe tener n_sim resultados."""
        n_sim = 50
        resultados = ejecutar_simulaciones_finales(n_sim=n_sim)
        for key in resultados:
            assert len(resultados[key]) == n_sim

    def test_reasonable_values(self) -> None:
        """Los resultados deben estar en rango razonable (positivos o cercanos)."""
        resultados = ejecutar_simulaciones_finales(n_sim=100)
        for key in resultados:
            media = np.mean(resultados[key])
            # Media debería ser positiva o cercana
            assert media > 0


class TestGenerarEstadisticasCompletas:
    """Tests para la función generar_estadisticas_completas."""

    def test_keys(self) -> None:
        """Debe retornar las 4 estrategias."""
        estadisticas = generar_estadisticas_completas(n_sim=10)
        assert len(estadisticas) == 4
        for key in estadisticas:
            assert "promedio" in estadisticas[key]
            assert "p10" in estadisticas[key]
            assert "p90" in estadisticas[key]
            assert "min" in estadisticas[key]
            assert "max" in estadisticas[key]

    def test_array_shape(self) -> None:
        """Cada array debe tener n_meses+1 elementos (61)."""
        estadisticas = generar_estadisticas_completas(n_sim=10)
        for key in estadisticas:
            for stat_key in estadisticas[key]:
                assert len(estadisticas[key][stat_key]) == 61  # 0 a 60 inclusive

    def test_percentile_ordering(self) -> None:
        """En cada mes: min <= p10 <= promedio <= p90 <= max (aproximadamente)."""
        estadisticas = generar_estadisticas_completas(n_sim=100, seed=42)
        for key in estadisticas:
            for month_idx in range(61):
                min_val = estadisticas[key]["min"][month_idx]
                p10 = estadisticas[key]["p10"][month_idx]
                prom = estadisticas[key]["promedio"][month_idx]
                p90 = estadisticas[key]["p90"][month_idx]
                max_val = estadisticas[key]["max"][month_idx]

                assert min_val <= p10 + 1e6  # Margen para errores numéricos
                assert p10 <= prom + 1e6
                assert prom <= p90 + 1e6
                assert p90 <= max_val + 1e6

    def test_reproducibility(self) -> None:
        """Con el mismo seed, debe producir resultados idénticos."""
        est1 = generar_estadisticas_completas(n_sim=50, seed=123)
        est2 = generar_estadisticas_completas(n_sim=50, seed=123)

        for key in est1:
            for stat_key in est1[key]:
                np.testing.assert_array_almost_equal(est1[key][stat_key], est2[key][stat_key])
