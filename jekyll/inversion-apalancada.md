---
layout: project
title: "Inversión Apalancada: Simulación Monte Carlo"
category: Finanzas Cuantitativas
description: "Simulación Monte Carlo de 10,000 escenarios comparando estrategias de inversión con y sin apalancamiento en fondos mutuos reales."
github_url: "https://github.com/manuelsancristobal/inversion-apalancada"
tech_stack:
  - Python
  - NumPy
  - Matplotlib
  - JavaScript
  - D3.js
  - Monte Carlo
---

## Comparativa de Resultados: ¿Deuda o Ahorro Gradual?

**Los aportes sin deuda ofrecen un rendimiento promedio superior con menor riesgo que las estrategias apalancadas.** Como se aprecia en los resultados de la simulación a 5 años, la estrategia de **Aportes Agresivos** alcanza un patrimonio promedio de **~$62 millones**, superando los **~$56 millones** del **Apalancamiento Agresivo**.

Como se observa en el rango de percentiles **P10-P90** de la visualización, la inversión con deuda presenta una dispersión de resultados mucho más amplia ($26M - $93M). Esto implica un potencial de retorno elevado pero con un riesgo de pérdida de capital significativo ante escenarios de mercado adversos.

## Visualización Interactiva de Escenarios

La herramienta a continuación permite explorar 10,000 trayectorias posibles para los próximos 60 meses. Como se vio en los párrafos de resultados, cada línea representa una evolución de fondos bajo condiciones de mercado variables.

<div style="position: relative; width: 100%; padding-bottom: 62%; overflow: hidden; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
  <iframe
    src="/proyectos/inversion-apalancada/viz.html"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
    loading="lazy"
    title="Simulación Monte Carlo de estrategias de inversión"
    allowfullscreen>
  </iframe>
</div>

## Resumen de Estrategias Analizadas

### 1. **Apalancamiento Agresivo**
Crédito de $27 millones invertido en Fondo Perfil A (agresivo).
- **Riesgo:** Alto, con alta dispersión en el rango **P10-P90**.
- **Costo:** Pago de cuota mensual fija de $699,125.

### 2. **Aportes Agresivos (Sin Deuda)**
Inversión mensual de $699,125 en Fondo Perfil A.
- **Riesgo:** Moderado-alto, con mejor protección ante caídas.
- **Resultado:** Mayor patrimonio promedio al final del periodo.

### 3. **Apalancamiento Moderado**
Crédito de $27 millones invertido en Fondo Perfil C (moderado).
- **Patrimonio promedio:** ~$48 millones.

### 4. **Aportes Moderados (Sin Deuda)**
Inversión mensual de $699,125 en Fondo Perfil C.
- **Patrimonio promedio:** ~$56 millones.
- **Estabilidad:** Menor dispersión de todas las estrategias en el gráfico.

## Metodología y Datos

### Simulación con Colas Gruesas
En lugar de una distribución normal, utilicé la **distribución t-Student con 5 grados de libertad**. Este enfoque captura la realidad de forma más precisa: los mercados financieros sufren eventos extremos con una frecuencia mayor a la prevista por modelos clásicos.

### Parámetros Reales
Los datos de rentabilidad y volatilidad corresponden a registros históricos de BancoEstado AGF del periodo 2024. El sistema descuenta de forma automática:
- **TAC (Tasa Anual de Costos)** del fondo (1% en Perfil A, 0.85% en Perfil C).
- **Intereses del crédito** (1.25% mensual) para escenarios con deuda.

## La Decisión Final

No existe una estrategia con superioridad en todos los casos. La elección correcta depende de la capacidad financiera y la tolerancia al riesgo en lo personal:

- **Elige apalancamiento si:** Posees una tolerancia alta al riesgo y el pago de la deuda no compromete tu estabilidad ante una baja de ingresos.
- **Elige aportes sin deuda si:** Prefieres la estabilidad, deseas evitar compromisos financieros o buscas el mejor rendimiento promedio histórico.

**Advertencia:** Este análisis posee fines educativos. Consulta con un asesor financiero antes de implementar estrategias de inversión con deuda.

---

### Notas Técnicas
Proyecto desarrollado con Python (NumPy) para el motor de simulación y D3.js para la interfaz interactiva. La simulación ejecuta 10,000 trayectorias para capturar tanto el escenario esperado como los límites de riesgo.
