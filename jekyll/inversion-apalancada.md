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

## ¿Deuda o Ahorro Gradual? El Dilema de la Inversión

Todo comenzó con una duda simple tras leer una oferta de crédito: ¿Valdría la pena endeudarse para invertir agresivamente? La respuesta intuitiva no bastaba, así que recurrí a la **Simulación de Monte Carlo**.

Esta técnica, en lugar de darnos un único resultado estático, nos permite "lanzar los dados" miles de veces. Simulamos 10,000 futuros posibles (trayectorias) para ver cómo se comportarían nuestros ahorros bajo las fluctuaciones reales del mercado. Al final del ejercicio, la conclusión fue contundente: **los aportes mensuales sin deuda ofrecen un rendimiento promedio superior y un riesgo significativamente menor que las estrategias apalancadas.**

Para este análisis, fijé un patrimonio meta de **30 millones de pesos en 5 años**, con un presupuesto mensual de **$699.125**. Mientras que la estrategia de **Aportes Agresivos** alcanzó un promedio de **~$62 millones**, el **Apalancamiento Agresivo** se quedó atrás con **~$56 millones**, cargando además con el peso de los intereses.

## Visualización Interactiva de Escenarios

La herramienta a continuación permite explorar estas 10,000 trayectorias a lo largo de 60 meses. Cada línea representa una evolución posible de los fondos; esta dispersión es vital para entender que en finanzas no solo importa el "promedio", sino también qué tan mal nos puede ir en el peor de los casos.

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

<div style="overflow-x: auto; margin: 1.5rem 0; border-radius: 8px; border: 1px solid #eee;">
  <table style="width: 100%; border-collapse: collapse; min-width: 500px; font-size: 0.95rem;">
    <thead style="background: var(--bg-light);">
      <tr>
        <th style="padding: 12px; border-bottom: 2px solid #ddd; text-align: left; width: 30%;">Estrategia</th>
        <th style="padding: 12px; border-bottom: 2px solid #ddd; text-align: left;">Fondo Agresivo (Perfil A)</th>
        <th style="padding: 12px; border-bottom: 2px solid #ddd; text-align: left;">Fondo Moderado (Perfil C)</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td style="padding: 12px; border-bottom: 1px solid #eee; background: var(--bg-light); font-weight: 600;">Aportes Mensuales<br><span style="font-weight: normal; font-size: 0.85rem; color: #666;">(Sin Deuda)</span></td>
        <td style="padding: 12px; border-bottom: 1px solid #eee;">
          <strong>~$62 Millones</strong><br>
          <span style="font-size: 0.85rem; color: #555;">Máximo rendimiento. El patrimonio crece libre de intereses bancarios.</span>
        </td>
        <td style="padding: 12px; border-bottom: 1px solid #eee;">
          <strong>~$56 Millones</strong><br>
          <span style="font-size: 0.85rem; color: #555;">Máxima estabilidad. Es la opción con menor dispersión de resultados.</span>
        </td>
      </tr>
      <tr>
        <td style="padding: 12px; background: var(--bg-light); font-weight: 600;">Apalancamiento<br><span style="font-weight: normal; font-size: 0.85rem; color: #666;">(Crédito $27M)</span></td>
        <td style="padding: 12px;">
          <strong>~$56 Millones</strong><br>
          <span style="font-size: 0.85rem; color: #555;">Riesgo alto. La volatilidad puede mermar el capital mientras la deuda sigue intacta.</span>
        </td>
        <td style="padding: 12px;">
          <strong>~$48 Millones</strong><br>
          <span style="font-size: 0.85rem; color: #555;">Retorno mermado. Los intereses del crédito consumen gran parte de la rentabilidad.</span>
        </td>
      </tr>
    </tbody>
  </table>
</div>

## Metodología y Datos

### Simulación con Colas Gruesas
Para que la simulación de Monte Carlo sea realista, utilicé una **distribución t-Student con 5 grados de libertad** (un parámetro estadístico que permite modelar eventos extremos o <abbr title="Un suceso sorpresivo, de gran impacto socioeconómico y que, una vez pasado, se racionaliza por retrospección.">cisnes negros</abbr> con mayor frecuencia). A diferencia de los modelos tradicionales que asumen que las crisis son eventos "imposibles", este enfoque captura la realidad financiera: los mercados sufren caídas extremas con más frecuencia de lo que nos gustaría.

### Parámetros del Mundo Real
Los datos de rentabilidad y volatilidad se basan en registros históricos de BancoEstado AGF (2024). Puedes consultar las fuentes de datos originales en estos enlaces: [Tasas de Crédito de Consumo](https://drive.google.com/file/d/1OLy9RsLsmzWdvyZ7heFeRE08ITHcoo10/view) y [Rentabilidad Histórica de Fondos](https://drive.google.com/file/d/1--ukCU5LhXP1Ex8ov3Do0AYlV1TAmtHj/view). 

El modelo descuenta automáticamente:
- **TAC (Tasa Anual de Costos):** 1% para Perfil A y 0.85% para Perfil C.
- **Intereses del crédito:** 1.25% mensual para los escenarios con deuda.

## La Decisión Final

La simulación nos enseña que no hay una "mejor" estrategia absoluta, sino una que se adapta a tu perfil:

- **Considera el apalancamiento solo si:** Tienes una tolerancia al riesgo extremadamente alta y la cuota del crédito no compromete tu estabilidad si tus ingresos bajan.
- **Prefiere los aportes sin deuda si:** Buscas optimizar el rendimiento promedio y quieres dormir tranquilo sabiendo que no le debes nada al banco mientras construyes tu patrimonio.

**Advertencia:** Este análisis es un ejercicio académico y técnico. Antes de tomar decisiones financieras reales, consulta con un profesional certificado. No te la jueguues solo.

---

### Notas Técnicas
Proyecto desarrollado con Python (NumPy) para el motor de simulación y D3.js para la interfaz interactiva. La simulación ejecuta 10,000 trayectorias para capturar tanto el escenario esperado como los límites de riesgo.

<div class="methodology-box" style="margin-top: 2rem; padding: 1.5rem; background: var(--bg-light); border-radius: 8px; border-left: 4px solid var(--secondary);">
    <p style="margin: 0; font-size: 0.95rem;">📌 <strong>Sobre este proyecto:</strong> Esta es una reversión del análisis original. El proyecto original está disponible en <a href="https://colab.research.google.com/drive/1aIuY07LmFaVrT9pR0Q2wX7yj6XsPo1QW" target="_blank" style="color: var(--secondary); font-weight: 600;">Google Colab</a>.</p>
</div>