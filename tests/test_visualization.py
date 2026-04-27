"""Tests para el módulo de visualización."""

from __future__ import annotations

import tempfile
from pathlib import Path

import numpy as np
import pytest

from inversion_apalancada.visualization import generate_charts


@pytest.fixture
def sample_results() -> dict[str, list[float]]:
    """Fixture con resultados de simulación de prueba."""
    np.random.seed(42)
    return {
        "agresivo_apalancado": np.random.normal(38e6, 18e6, 1000).tolist(),
        "agresivo_sin_apalancamiento": np.random.normal(32e6, 12e6, 1000).tolist(),
        "moderado_apalancado": np.random.normal(35e6, 10e6, 1000).tolist(),
        "moderado_sin_apalancamiento": np.random.normal(32e6, 6e6, 1000).tolist(),
    }


def test_generate_charts_creates_files(sample_results: dict[str, list[float]]) -> None:
    """Test que generate_charts crea los 4 archivos PNG."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        paths = generate_charts(sample_results, output_dir)

        # Debe retornar 4 rutas
        assert len(paths) == 4

        # Los archivos deben existir
        assert all(p.exists() for p in paths)

        # Los nombres deben ser los esperados
        nombres = {p.name for p in paths}
        assert "01_histogram.png" in nombres
        assert "02_boxplot.png" in nombres
        assert "03_cdf.png" in nombres
        assert "04_risk_return.png" in nombres


def test_generate_charts_returns_paths(sample_results: dict[str, list[float]]) -> None:
    """Test que generate_charts retorna Path objects."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        paths = generate_charts(sample_results, output_dir)

        # Todos deben ser Path
        assert all(isinstance(p, Path) for p in paths)

        # Todos deben tener extensión .png
        assert all(p.suffix == ".png" for p in paths)


def test_generate_charts_creates_output_dir(sample_results: dict[str, list[float]]) -> None:
    """Test que generate_charts crea el directorio si no existe."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "nonexistent" / "nested"
        assert not output_dir.exists()

        generate_charts(sample_results, output_dir)

        # El directorio debe existir ahora
        assert output_dir.exists()
        assert output_dir.is_dir()


def test_generate_charts_file_sizes(sample_results: dict[str, list[float]]) -> None:
    """Test que los archivos PNG generados tienen tamaño razonable."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        paths = generate_charts(sample_results, output_dir)

        # Los archivos deben tener tamaño > 0
        for p in paths:
            assert p.stat().st_size > 0
            # PNGs generados por matplotlib generalmente son > 10KB
            assert p.stat().st_size > 10000
