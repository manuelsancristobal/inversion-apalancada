# Datos: Inversión Apalancada

## Origen
- **Tipo**: Datos Sintéticos.
- **Generación**: Simulaciones de Monte Carlo basadas en parámetros estadísticos (retorno esperado, volatilidad, costo de apalancamiento).
- **Herramientas**: `numpy` para la generación de caminos aleatorios (Geometric Brownian Motion).

## Estructura
- `raw/`: Parámetros de configuración de las simulaciones.
- `processed/`: Resultados de las simulaciones consolidados para visualización.
- `external/`: Benchmarks históricos de mercado (si aplica).

## Variables Clave
- `Retorno`: Variación porcentual del capital.
- `Apalancamiento`: Factor de multiplicación de exposición.
- `Drawdown`: Máxima caída desde el pico de capital.
