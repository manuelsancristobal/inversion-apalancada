# Inversión Apalancada - Simulación de Monte Carlo

## Impacto y Valor del Proyecto
Este simulador financiero aborda el problema de la gestión de riesgos en estrategias de inversión apalancada. Mediante simulaciones de Monte Carlo, el proyecto cuantifica la probabilidad de ruina y el impacto de la volatilidad en el capital a largo plazo bajo diferentes niveles de exposición. Es una herramienta crítica para inversores que buscan optimizar su retorno ajustado por riesgo y comprender empíricamente por qué "más apalancamiento" no siempre se traduce en mayor riqueza acumulada debido al arrastre de la volatilidad (*volatility drag*).

## Stack Tecnológico
- **Lenguaje**: Python 3.10+
- **Librerías Clave**: `Numpy` (Simulación vectorial), `Matplotlib` (Gráficos estadísticos).
- **Frontend**: JavaScript (Visualización de resultados), HTML5/CSS3.
- **Calidad de Código**: `Ruff`, `Pytest`.
- **CI/CD**: GitHub Actions.

## Arquitectura de Datos y Metodología
1. **Modelado**: Uso de Movimiento Browniano Geométrico (GBM) para proyectar precios de activos.
2. **Simulación**: Ejecución de miles de trayectorias paralelas para obtener distribuciones de probabilidad.
3. **Análisis**: Cálculo de métricas de riesgo-retorno como el Ratio de Sharpe, Máximo Drawdown y Capital Final Esperado.
4. **Visualización**: Generación de curvas de capital y distribución de resultados finales para comparación de escenarios.

## Quick Start (Reproducibilidad)
1. `git clone https://github.com/manuelsancristobal/inversion-apalancada`
2. `make install` (Instala dependencias y prepara el entorno)
3. `make test` (Ejecuta pruebas sobre el motor de simulación)
4. `make run` (Genera una nueva simulación con parámetros por defecto)
5. `make ver` (Visualiza los resultados en la interfaz web)

## Estructura del Proyecto
- `src/`: Lógica central de simulación y CLI.
- `data/`: Datos de entrada y resultados de simulación (`raw/`, `processed/`, `external/`).
- `viz/`: Interfaz de usuario para exploración de resultados.
- `tests/`: Pruebas de validación estadística y lógica.

---
**Autor**: Manuel San Cristóbal Opazo 
**Licencia**: MIT
