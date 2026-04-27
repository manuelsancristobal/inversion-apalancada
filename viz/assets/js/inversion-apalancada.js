(function () {
  "use strict";

  // ── Configuración ──────────────────────────────────────
  const FRAME_MS = 120;
  const MARGIN = { top: 60, right: 40, bottom: 50, left: 80 };
  const DATA_PATH = "assets/data/simulation_stats.json";

  // Formateo números
  const fmtM = (v) => `$${(v / 1e6).toFixed(1)}M`;

  // ── Estado ─────────────────────────────────────────────
  let state = {
    playing: false,
    monthIndex: 0,
    data: null,
    visibleStrategies: new Set(["agresivo_apalancado", "agresivo_sin_apalancamiento", "moderado_apalancado", "moderado_sin_apalancamiento"]),
    timer: null,
  };

  // ── Referencias DOM ────────────────────────────────────
  const chartEl = document.getElementById("chart");
  const slider = document.getElementById("month-slider");
  const monthLabel = document.getElementById("month-label");
  const btnPlay = document.getElementById("btn-play");
  const statsPanel = document.getElementById("stats-panel");

  // ── Setup SVG ──────────────────────────────────────────
  const width = 940;
  const height = 520;
  const innerWidth = width - MARGIN.left - MARGIN.right;
  const innerHeight = height - MARGIN.top - MARGIN.bottom;

  const svg = d3.select("#chart").append("svg").attr("viewBox", `0 0 ${width} ${height}`).attr("preserveAspectRatio", "xMidYMid meet");

  const g = svg.append("g").attr("transform", `translate(${MARGIN.left},${MARGIN.top})`);

  // Escalas
  const x = d3.scaleLinear().domain([0, 60]).range([0, innerWidth]);
  const y = d3.scaleLinear().range([innerHeight, 0]);

  // Ejes
  const xAxis = d3.axisBottom(x).ticks(12);
  const yAxis = d3.axisLeft(y);

  const gXAxis = g.append("g").attr("class", "x-axis").attr("transform", `translate(0,${innerHeight})`);
  const gYAxis = g.append("g").attr("class", "y-axis");

  // Grupo para las líneas
  const gLines = g.append("g").attr("class", "lines");

  // Línea de meta
  const gMeta = g.append("g").attr("class", "meta-line");

  // Labels
  svg.append("text").attr("x", width / 2).attr("y", 30).attr("text-anchor", "middle").attr("font-size", "18px").attr("font-weight", "bold").text("Evolución de Estrategias - 60 Meses");

  svg.append("text").attr("x", MARGIN.left + innerWidth / 2).attr("y", height - 10).attr("text-anchor", "middle").attr("font-size", "12px").attr("fill", "#999").text("Meses");

  svg.append("text").attr("transform", "rotate(-90)").attr("y", 15).attr("x", -(MARGIN.top + innerHeight / 2)).attr("text-anchor", "middle").attr("font-size", "12px").attr("fill", "#999").text("Patrimonio Neto ($)");

  // ── Funciones ─────────────────────────────────────────
  async function loadData() {
    try {
      const response = await fetch(DATA_PATH);
      state.data = await response.json();
      return true;
    } catch (err) {
      console.error("Error cargando datos:", err);
      return false;
    }
  }

  // Todas las claves de estrategia para poder limpiar SVG al hacer toggle
  const ALL_STRATEGY_KEYS = ["agresivo_apalancado", "agresivo_sin_apalancamiento", "moderado_apalancado", "moderado_sin_apalancamiento"];

  function draw(monthIdx) {
    if (!state.data) return;

    // Obtener datos hasta el mes actual
    const visibleKeys = Array.from(state.visibleStrategies);
    let yMin = Infinity,
      yMax = -Infinity;

    for (const key of visibleKeys) {
      const strat = state.data.strategies[key];
      yMin = Math.min(yMin, Math.min(...strat.min.slice(0, monthIdx + 1)));
      yMax = Math.max(yMax, Math.max(...strat.max.slice(0, monthIdx + 1)));
    }

    // Agregar margen
    yMin = yMin < 0 ? yMin * 1.1 : yMin * 0.9;
    yMax = yMax * 1.05;

    y.domain([yMin, yMax]);

    // Actualizar ejes
    gXAxis.call(xAxis);
    gYAxis.call(yAxis);

    // Formatear labels del eje Y en millones
    gYAxis.selectAll("text").attr("font-size", "11px");
    gYAxis.selectAll(".tick text").text((d) => fmtM(d));

    // Línea de meta
    gMeta.selectAll("*").remove();
    gMeta
      .append("line")
      .attr("x1", 0)
      .attr("x2", innerWidth)
      .attr("y1", y(30e6))
      .attr("y2", y(30e6))
      .attr("stroke", "black")
      .attr("stroke-dasharray", "4,4")
      .attr("stroke-width", 2)
      .attr("opacity", 0.6);

    gMeta.append("text").attr("x", innerWidth + 5).attr("y", y(30e6) + 4).attr("font-size", "11px").attr("fill", "black").text("Meta $30M");

    // Limpiar estrategias ocultas
    for (const key of ALL_STRATEGY_KEYS) {
      if (!state.visibleStrategies.has(key)) {
        gLines.selectAll(`.area-${key}`).remove();
        gLines.selectAll(`.line-${key}`).remove();
        gLines.selectAll(`.line-min-${key}`).remove();
        gLines.selectAll(`.line-max-${key}`).remove();
        gLines.selectAll(`.dot-${key}`).remove();
      }
    }

    // Dibujar estrategias
    for (const key of visibleKeys) {
      const strat = state.data.strategies[key];
      const color = strat.color;

      // Datos hasta el mes actual
      const months = d3.range(0, monthIdx + 1);

      // Banda P10-P90
      const areaP1090 = d3
        .area()
        .x((m) => x(m))
        .y0((m) => y(strat.p10[m]))
        .y1((m) => y(strat.p90[m]));

      gLines
        .selectAll(`.area-${key}`)
        .data([1])
        .join("path")
        .attr("class", `area-${key}`)
        .attr("d", areaP1090(months))
        .attr("fill", color)
        .attr("opacity", 0.15);

      // Línea promedio
      const lineAvg = d3
        .line()
        .x((m) => x(m))
        .y((m) => y(strat.promedio[m]));

      gLines
        .selectAll(`.line-${key}`)
        .data([1])
        .join("path")
        .attr("class", `line-${key}`)
        .attr("d", lineAvg(months))
        .attr("stroke", color)
        .attr("stroke-width", 2.5)
        .attr("fill", "none");

      // Líneas punteadas min/max
      const lineMin = d3
        .line()
        .x((m) => x(m))
        .y((m) => y(strat.min[m]));

      const lineMax = d3
        .line()
        .x((m) => x(m))
        .y((m) => y(strat.max[m]));

      gLines
        .selectAll(`.line-min-${key}`)
        .data([1])
        .join("path")
        .attr("class", `line-min-${key}`)
        .attr("d", lineMin(months))
        .attr("stroke", color)
        .attr("stroke-width", 1)
        .attr("stroke-dasharray", "2,2")
        .attr("fill", "none")
        .attr("opacity", 0.5);

      gLines
        .selectAll(`.line-max-${key}`)
        .data([1])
        .join("path")
        .attr("class", `line-max-${key}`)
        .attr("d", lineMax(months))
        .attr("stroke", color)
        .attr("stroke-width", 1)
        .attr("stroke-dasharray", "2,2")
        .attr("fill", "none")
        .attr("opacity", 0.5);

      // Punto en el mes actual
      gLines
        .selectAll(`.dot-${key}`)
        .data([monthIdx])
        .join("circle")
        .attr("class", `dot-${key}`)
        .attr("cx", x(monthIdx))
        .attr("cy", y(strat.promedio[monthIdx]))
        .attr("r", 4)
        .attr("fill", color)
        .attr("stroke", "white")
        .attr("stroke-width", 2);
    }

    // Actualizar labels
    monthLabel.textContent = `Mes ${monthIdx}`;
    slider.value = monthIdx;

    // Actualizar panel de estadísticas
    if (statsPanel) {
      let html = `<div style="font-weight: bold; margin-bottom: 10px;">Mes ${monthIdx}</div>`;
      for (const key of visibleKeys) {
        const label = state.data.strategies[key].label;
        const prom = state.data.strategies[key].promedio[monthIdx];
        const p10 = state.data.strategies[key].p10[monthIdx];
        const p90 = state.data.strategies[key].p90[monthIdx];

        html += `
          <div style="margin-bottom: 12px; padding: 8px; background: white; border-radius: 4px; border-left: 3px solid ${state.data.strategies[key].color};">
            <div style="font-weight: 600; color: ${state.data.strategies[key].color};">${label}</div>
            <div style="font-size: 12px; color: #666;">
              Promedio: <strong>${fmtM(prom)}</strong><br>
              P10-P90: <strong>${fmtM(p10)} - ${fmtM(p90)}</strong>
            </div>
          </div>
        `;
      }
      statsPanel.innerHTML = html;
    }
  }

  function play() {
    // Reiniciar si ya está al final
    if (state.monthIndex >= 60) {
      state.monthIndex = 0;
      draw(0);
    }

    state.playing = true;
    btnPlay.textContent = "⏸ Pausa";
    btnPlay.classList.add("playing");

    state.timer = d3.interval(() => {
      state.monthIndex++;
      if (state.monthIndex > 60) {
        pause();
        state.monthIndex = 60;
      } else {
        draw(state.monthIndex);
      }
    }, FRAME_MS);
  }

  function pause() {
    state.playing = false;
    btnPlay.textContent = "▶ Play";
    btnPlay.classList.remove("playing");
    if (state.timer) {
      state.timer.stop();
      state.timer = null;
    }
  }

  // ── Event Listeners ────────────────────────────────────
  btnPlay.addEventListener("click", () => {
    if (state.playing) {
      pause();
    } else {
      play();
    }
  });

  slider.addEventListener("input", (e) => {
    pause();
    state.monthIndex = parseInt(e.target.value, 10);
    draw(state.monthIndex);
  });

  // Strategy toggles
  document.querySelectorAll('.strategy-toggles input[type="checkbox"]').forEach((checkbox) => {
    checkbox.addEventListener("change", (e) => {
      const strategy = e.target.dataset.strategy;
      if (e.target.checked) {
        state.visibleStrategies.add(strategy);
      } else {
        state.visibleStrategies.delete(strategy);
      }
      draw(state.monthIndex);
    });
  });

  // ── Inicialización ─────────────────────────────────────
  (async () => {
    if (await loadData()) {
      draw(0);
    } else {
      chartEl.innerHTML = '<p style="color: red;">Error cargando datos de simulación.</p>';
    }
  })();
})();
