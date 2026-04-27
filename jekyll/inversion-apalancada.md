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

## Visualización Interactiva

¿Endeudarse para invertir o ahorrar paso a paso? Esta pregunta no tiene una respuesta única. Depende de tu tolerancia al riesgo, tu capacidad de pago y tus circunstancias personales. Para ayudarte a tomar una decisión informada, realicé una simulación Monte Carlo que compara cuatro estrategias diferentes: dos con apalancamiento (usando fondos mutuos reales de BancoEstado AGF) y dos sin deuda.

La visualización interactiva a continuación te permite explorar los 10,000 escenarios posibles para los próximos 5 años, viendo cómo evolucionan tus fondos mes a mes bajo diferentes condiciones de mercado.

<div style="position: relative; width: 100%; padding-bottom: 62%; overflow: hidden; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
  <iframe
    src="/proyectos/inversion-apalancada/viz.html"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none;"
    loading="lazy"
    title="Simulación Monte Carlo de estrategias de inversión"
    allowfullscreen>
  </iframe>
</div>

## Las Cuatro Estrategias Analizadas

### 1. **Apalancamiento Agresivo**
Pides $27 millones, inviertes todo en Fondo Perfil A (agresivo), pagas $699,125 mensuales.
- **Rentabilidad esperada:** 14.8% anual (neta de costos)
- **Volatilidad:** 22% anual
- **Perfil:** Alto riesgo, alto potencial de retorno

### 2. **Aportes Agresivos**
Inviertes $699,125 mensuales en Fondo Perfil A, sin deuda.
- **Rentabilidad esperada:** 14.8% anual (neta de costos)
- **Volatilidad:** 22% anual
- **Perfil:** Riesgo moderado-alto, construcción gradual

### 3. **Apalancamiento Moderado**
Pides $27 millones, inviertes todo en Fondo Perfil C (moderado), pagas $699,125 mensuales.
- **Rentabilidad esperada:** 11.5% anual (neta de costos)
- **Volatilidad:** 15% anual
- **Perfil:** Riesgo moderado, rendimiento moderado

### 4. **Aportes Moderados**
Inviertes $699,125 mensuales en Fondo Perfil C, sin deuda.
- **Rentabilidad esperada:** 11.5% anual (neta de costos)
- **Volatilidad:** 15% anual
- **Perfil:** Bajo riesgo, crecimiento constante

## Metodología

### Monte Carlo con Colas Gruesas

En lugar de asumir que los mercados tienen distribución normal, utilicé **distribución t-Student con 5 grados de libertad**. Esto captura mejor la realidad: los mercados financieros tienen más eventos extremos (tanto ganancias excepcionales como pérdidas severas) de lo que predice una distribución normal.

### Datos Reales

Los parámetros de rentabilidad y volatilidad provienen de datos históricos reales de los fondos mutuos de BancoEstado AGF correspondientes al período 2024. Aunque esto es una muestra pequeña, es lo más preciso disponible para la simulación.

### Descuentos de Costos

Cada simulación automáticamente descuenta:
- **TAC (Tasa Anual de Costos)** del fondo (1% para Perfil A, 0.85% para Perfil C)
- **Intereses del crédito** (1.25% mensual) en las estrategias apalancadas

## Resultados

**Estrategia de Apalancamiento Agresivo:**
- Patrimonio promedio al mes 60: **~$56 millones**
- Rango P10-P90: $26M - $93M
- Alta dispersión: máximo potencial pero también mayor riesgo

**Estrategia de Aportes Agresivos (sin deuda):**
- Patrimonio promedio al mes 60: **~$62 millones**
- Rango P10-P90: $41M - $87M
- Mejor rendimiento promedio con menor dispersión que el apalancado

**Estrategia de Apalancamiento Moderado:**
- Patrimonio promedio al mes 60: **~$48 millones**
- Rango P10-P90: $29M - $69M

**Estrategia de Aportes Moderados (sin deuda):**
- Patrimonio promedio al mes 60: **~$56 millones**
- Rango P10-P90: $43M - $71M
- Menor dispersión de todas las estrategias

## La Decisión Final

No existe una estrategia "mejor" universalmente. La decisión correcta es la que se alinea con tu capacidad financiera, tolerancia al riesgo y circunstancias personales.

- **Elige apalancamiento si:** Tienes tolerancia alta al riesgo, puedes mantener el pago de la deuda incluso si tus ingresos bajan, y tienes horizonte largo (5+ años).
- **Elige aportes sin apalancamiento si:** Prefieres estabilidad, quieres evitar deuda, o tienes capacidad limitada de pago extra.

**Advertencia:** Este análisis es educativo. Consulta con un asesor financiero certificado antes de implementar cualquier estrategia de inversión, especialmente con apalancamiento.

---

### Notas Técnicas

Este proyecto fue desarrollado usando Python (NumPy, Matplotlib) para las simulaciones y JavaScript/D3.js para la visualización interactiva. El código está disponible en [GitHub]({{ page.github_url }}) bajo licencia MIT.

La simulación ejecuta 10,000 trayectorias independientes para cada estrategia, calculando estadísticas mes a mes (promedio, percentiles 10 y 90, mínimos y máximos) para capturar tanto el escenario esperado como los rangos de riesgo.
