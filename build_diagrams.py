# -*- coding: utf-8 -*-
"""
Script que genera todos los archivos HTML y empaqueta el nuevo flujo segmentado del PAS - MPCH.
Genera:
1. diagrama_optimizado.html
2. diagrama_especiales.html
3. diagrama_ejecutivo.html
4. index.html (Portal unificado con pestañas interactivas, pan/zoom, búsqueda y drawer inspector)
"""
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(filename):
    path = os.path.join(BASE_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

optimizado_mmd = read_file("diagrama_optimizado.mmd")
especiales_mmd = read_file("diagrama_especiales.mmd")
ejecutivo_mmd = read_file("diagrama_ejecutivo.mmd")

CSS_SHARED = """
  body {
    font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background-color: #f1f5f9;
  }
  .mono {
    font-family: 'JetBrains Mono', monospace;
  }
  .diagram-viewport {
    width: 100%;
    height: 100%;
    overflow: hidden;
    background-color: #f8fafc;
    position: relative;
    touch-action: none;
    cursor: grab;
    user-select: none;
    -webkit-user-select: none;
  }
  .diagram-viewport:active {
    cursor: grabbing;
  }
  .diagram-viewport svg {
    width: 100% !important;
    height: 100% !important;
    max-width: none !important;
    touch-action: none;
  }
  
  /* BADGES DE DECISIÓN Y FLUJO - MÁXIMO CONTRASTE Y LEGIBILIDAD */
  .edgeLabel {
    background-color: transparent !important;
  }
  .edge-yes {
    background: #ecfdf5 !important;
    color: #065f46 !important;
    border: 1.5px solid #10b981 !important;
    border-radius: 9999px !important;
    padding: 3px 10px !important;
    font-weight: 800 !important;
    font-size: 11px !important;
    box-shadow: 0 2px 4px rgba(16, 185, 129, 0.2) !important;
    display: inline-block !important;
    white-space: nowrap !important;
  }
  .edge-no {
    background: #fef2f2 !important;
    color: #991b1b !important;
    border: 1.5px solid #ef4444 !important;
    border-radius: 9999px !important;
    padding: 3px 10px !important;
    font-weight: 800 !important;
    font-size: 11px !important;
    box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2) !important;
    display: inline-block !important;
    white-space: nowrap !important;
  }
  .edge-info {
    background: #eff6ff !important;
    color: #1e40af !important;
    border: 1.5px solid #3b82f6 !important;
    border-radius: 9999px !important;
    padding: 3px 10px !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2) !important;
    display: inline-block !important;
    white-space: nowrap !important;
  }
  .edge-warn {
    background: #fffbeb !important;
    color: #92400e !important;
    border: 1.5px solid #f59e0b !important;
    border-radius: 9999px !important;
    padding: 3px 10px !important;
    font-weight: 700 !important;
    font-size: 11px !important;
    box-shadow: 0 2px 4px rgba(245, 158, 11, 0.2) !important;
    display: inline-block !important;
    white-space: nowrap !important;
  }
  
  /* ROMBOS DE DECISIÓN DE ALTO CONTRASTE */
  .node.decision polygon {
    fill: #eef2ff !important;
    stroke: #4f46e5 !important;
    stroke-width: 2.5px !important;
    filter: drop-shadow(0 3px 6px rgba(79, 70, 229, 0.18)) !important;
  }
  .node.decision .nodeLabel {
    color: #1e1b4b !important;
    font-weight: 800 !important;
    font-size: 12px !important;
    line-height: 1.35 !important;
  }
  
  /* TRAZOS Y CONEXIONES NÍTIDAS */
  .edgePath .path {
    stroke: #475569 !important;
    stroke-width: 2.2px !important;
  }
  .arrowheadPath {
    fill: #334155 !important;
  }

  /* SUBGRAFOS / CLUSTERS */
  .cluster rect {
    rx: 12px !important;
    ry: 12px !important;
  }
  .cluster-label text, .cluster-label span {
    font-weight: 800 !important;
    font-size: 13px !important;
    letter-spacing: -0.01em !important;
  }

  /* EFECTOS INTERACTIVOS EN NODOS */
  .node {
    cursor: pointer;
    transition: transform 0.15s ease, filter 0.15s ease;
  }
  .node:hover {
    filter: drop-shadow(0 4px 10px rgba(2, 132, 199, 0.35)) !important;
  }

  .node-highlighted rect, .node-highlighted polygon, .node-highlighted circle {
    stroke: #f59e0b !important;
    stroke-width: 4.5px !important;
    filter: drop-shadow(0 0 14px #f59e0b) !important;
    animation: pulseHighlight 1.4s infinite alternate !important;
  }
  .node-selected rect, .node-selected polygon, .node-selected circle {
    stroke: #0284c7 !important;
    stroke-width: 4px !important;
    filter: drop-shadow(0 0 16px rgba(2, 132, 199, 0.8)) !important;
  }

  @keyframes pulseHighlight {
    from { filter: drop-shadow(0 0 4px #f59e0b); }
    to { filter: drop-shadow(0 0 18px #f59e0b); }
  }

  /* TABS ACTIVOS */
  .tab-btn.active {
    background-color: #0284c7;
    color: white;
    border-color: #0284c7;
    box-shadow: 0 2px 5px rgba(2, 132, 199, 0.3);
  }

  /* SCROLLBAR MODERNA */
  ::-webkit-scrollbar {
    width: 6px;
    height: 6px;
  }
  ::-webkit-scrollbar-track {
    background: #f1f5f9;
  }
  ::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 4px;
  }
  ::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
  }
"""

NAV_HANDLER_JS = """
    // =========================================================================
    // NAVEGACIÓN MEJORADA: PELLIZCO PARA ZOOM + 2 DEDOS PARA DESPLAZAR
    // =========================================================================
    let currentNavHandler = null;
    let wheelMode = 'pan'; // 'pan' (2 dedos para desplazar) o 'zoom' (rueda zoom)

    function getSvgPoint(clientX, clientY, svgElement) {
      const p = svgElement.createSVGPoint();
      p.x = clientX;
      p.y = clientY;
      try {
        const screenCTM = svgElement.getScreenCTM();
        if (screenCTM) {
          return p.matrixTransform(screenCTM.inverse());
        }
      } catch (err) {}
      return p;
    }

    function createNavigationHandler(svgElement, instance) {
      const container = document.getElementById('container') || svgElement;

      let touchState = {
        mode: 'none',
        startX: 0,
        startY: 0,
        lastX: 0,
        lastY: 0,
        lastMidX: 0,
        lastMidY: 0,
        lastDist: 0,
        isDragging: false
      };

      let mouseState = {
        down: false,
        startX: 0,
        startY: 0,
        isDragging: false
      };

      function onMouseDown(e) {
        if (e.button !== 0) return;
        mouseState.down = true;
        mouseState.startX = e.clientX;
        mouseState.startY = e.clientY;
        mouseState.isDragging = false;
      }

      function onMouseMove(e) {
        if (!mouseState.down) return;
        if (Math.hypot(e.clientX - mouseState.startX, e.clientY - mouseState.startY) > 5) {
          mouseState.isDragging = true;
        }
      }

      function onMouseUp() {
        mouseState.down = false;
        setTimeout(() => { mouseState.isDragging = false; }, 60);
      }

      function onWheel(e) {
        if (!instance) return;
        e.preventDefault();

        // 1. Pellizco en trackpad o Ctrl + Rueda: zoom suave centrado en la posición del cursor
        if (e.ctrlKey) {
          const zoomFactor = Math.exp(-e.deltaY * 0.006);
          const pt = getSvgPoint(e.clientX, e.clientY, svgElement);
          instance.zoomAtPointBy(zoomFactor, pt);
          return;
        }

        // 2. Modo Rueda Zoom si el usuario lo activó en el botón
        if (wheelMode === 'zoom') {
          const delta = e.deltaY || e.deltaX;
          const zoomFactor = delta > 0 ? 0.88 : 1.14;
          const pt = getSvgPoint(e.clientX, e.clientY, svgElement);
          instance.zoomAtPointBy(zoomFactor, pt);
          return;
        }

        // 3. Modo Desplazamiento por defecto ('2 Dedos: Desplazar')
        // Permite direccionar de derecha a izquierda o verticalmente a través de todo el flujo
        instance.panBy({ x: -e.deltaX, y: -e.deltaY });
      }

      function onTouchStart(e) {
        if (!instance) return;
        if (e.touches.length === 1) {
          touchState.mode = 'single';
          touchState.startX = e.touches[0].clientX;
          touchState.startY = e.touches[0].clientY;
          touchState.lastX = touchState.startX;
          touchState.lastY = touchState.startY;
          touchState.isDragging = false;
        } else if (e.touches.length >= 2) {
          touchState.mode = 'pinch';
          touchState.isDragging = true;
          const t1 = e.touches[0];
          const t2 = e.touches[1];
          touchState.lastMidX = (t1.clientX + t2.clientX) / 2;
          touchState.lastMidY = (t1.clientY + t2.clientY) / 2;
          touchState.lastDist = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
        }
      }

      function onTouchMove(e) {
        if (!instance) return;
        e.preventDefault();

        if (e.touches.length >= 2) {
          const t1 = e.touches[0];
          const t2 = e.touches[1];
          const midX = (t1.clientX + t2.clientX) / 2;
          const midY = (t1.clientY + t2.clientY) / 2;
          const dist = Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);

          if (touchState.mode !== 'pinch') {
            touchState.mode = 'pinch';
            touchState.lastMidX = midX;
            touchState.lastMidY = midY;
            touchState.lastDist = dist;
            touchState.isDragging = true;
            return;
          }

          // A) Direccionar el flujo con 2 dedos (Pan horizontal y vertical fluido)
          const dx = midX - touchState.lastMidX;
          const dy = midY - touchState.lastMidY;
          if (Math.abs(dx) > 0.2 || Math.abs(dy) > 0.2) {
            instance.panBy({ x: dx, y: dy });
          }

          // B) Gesto de pellizco para hacer zoom continuo centrado en el punto medio
          if (touchState.lastDist > 10 && dist > 10) {
            const factor = dist / touchState.lastDist;
            if (factor > 0.5 && factor < 2.0 && Math.abs(factor - 1) > 0.003) {
              const pt = getSvgPoint(midX, midY, svgElement);
              instance.zoomAtPointBy(factor, pt);
            }
          }

          touchState.lastMidX = midX;
          touchState.lastMidY = midY;
          touchState.lastDist = dist;
        } else if (e.touches.length === 1 && touchState.mode === 'single') {
          const t = e.touches[0];
          const dx = t.clientX - touchState.lastX;
          const dy = t.clientY - touchState.lastY;
          const moved = Math.hypot(t.clientX - touchState.startX, t.clientY - touchState.startY);
          if (moved > 6) {
            touchState.isDragging = true;
          }
          if (touchState.isDragging) {
            instance.panBy({ x: dx, y: dy });
          }
          touchState.lastX = t.clientX;
          touchState.lastY = t.clientY;
        }
      }

      function onTouchEnd(e) {
        if (e.touches.length === 1) {
          touchState.mode = 'single';
          touchState.lastX = e.touches[0].clientX;
          touchState.lastY = e.touches[0].clientY;
          touchState.startX = touchState.lastX;
          touchState.startY = touchState.lastY;
          touchState.isDragging = true;
        } else if (e.touches.length === 0) {
          touchState.mode = 'none';
          setTimeout(() => { touchState.isDragging = false; }, 80);
        }
      }

      container.addEventListener('wheel', onWheel, { passive: false });
      container.addEventListener('touchstart', onTouchStart, { passive: false });
      container.addEventListener('touchmove', onTouchMove, { passive: false });
      container.addEventListener('touchend', onTouchEnd, { passive: false });
      container.addEventListener('touchcancel', onTouchEnd, { passive: false });

      window.addEventListener('mousedown', onMouseDown, true);
      window.addEventListener('mousemove', onMouseMove, true);
      window.addEventListener('mouseup', onMouseUp, true);

      return {
        isUserDragging: () => touchState.isDragging || mouseState.isDragging,
        destroy: () => {
          container.removeEventListener('wheel', onWheel);
          container.removeEventListener('touchstart', onTouchStart);
          container.removeEventListener('touchmove', onTouchMove);
          container.removeEventListener('touchend', onTouchEnd);
          container.removeEventListener('touchcancel', onTouchEnd);
          window.removeEventListener('mousedown', onMouseDown, true);
          window.removeEventListener('mousemove', onMouseMove, true);
          window.removeEventListener('mouseup', onMouseUp, true);
        }
      };
    }

    function toggleWheelMode() {
      const btn = document.getElementById('wheel-mode-btn');
      if (wheelMode === 'pan') {
        wheelMode = 'zoom';
        if (btn) {
          btn.innerHTML = '<i class="fa-solid fa-magnifying-glass-plus text-amber-600"></i> <span class="hidden sm:inline">Rueda: Zoom</span>';
          btn.title = "Modo Zoom activo: La rueda hace zoom (o usa pellizco con 2 dedos)";
        }
      } else {
        wheelMode = 'pan';
        if (btn) {
          btn.innerHTML = '<i class="fa-solid fa-hand text-sky-600"></i> <span class="hidden sm:inline">2 Dedos: Desplazar</span>';
          btn.title = "Modo Desplazamiento activo: 2 dedos en trackpad desplazan el diagrama por el flujo";
        }
      }
    }
"""

def generate_standalone_html(title, subtitle, filename, mmd_content, nav_active, quick_jumps):
    jump_buttons_html = ""
    for j in quick_jumps:
        jump_buttons_html += f"""
        <button onclick="jumpToNode('{j['target']}')" class="px-2.5 py-1 text-xs font-semibold bg-white text-slate-700 border border-slate-200 rounded-lg hover:bg-slate-50 hover:text-sky-700 hover:border-sky-300 transition-all flex items-center gap-1 shadow-xs whitespace-nowrap">
          <span>{j['icon']}</span> <span>{j['label']}</span>
        </button>
        """

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - Municipalidad Provincial de Chiclayo</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
{CSS_SHARED}
  </style>
</head>
<body class="bg-slate-100 text-slate-800 flex flex-col h-screen overflow-hidden">

  <!-- CABECERA PRINCIPAL CON NAVEGACIÓN -->
  <header class="bg-white border-b border-slate-200 px-4 py-2.5 flex flex-wrap items-center justify-between gap-3 shadow-xs z-20 shrink-0">
    <div class="flex items-center gap-3">
      <a href="index.html" class="flex items-center gap-2.5 text-slate-800 hover:text-sky-700 transition-colors group" title="Ir al Portal Maestro">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-700 to-sky-500 flex items-center justify-center text-white shadow-sm group-hover:scale-105 transition-transform">
          <i class="fa-solid fa-scale-balanced text-base"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-sm font-extrabold text-slate-900 tracking-tight leading-none group-hover:text-sky-700">{title}</h1>
            <span class="px-2 py-0.5 text-[10px] font-bold bg-sky-100 text-sky-800 rounded-full border border-sky-200">RAS 2026 • MPCH</span>
          </div>
          <p class="text-[11px] text-slate-500 font-medium leading-none mt-1">{subtitle}</p>
        </div>
      </a>
    </div>

    <!-- SWITCHER DE NAVEGACIÓN GLOBAL -->
    <nav class="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 shadow-inner">
      <a href="index.html" class="px-3 py-1 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 text-slate-600 hover:text-sky-700 hover:bg-white" title="Portal con los 3 diagramas">
        <i class="fa-solid fa-house text-slate-400"></i> Portal
      </a>
      <a href="diagrama_optimizado.html" class="px-3 py-1 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 {'active bg-sky-600 text-white shadow-xs' if nav_active == 'optimizado' else 'text-slate-600 hover:text-sky-700 hover:bg-white'}">
        <i class="fa-solid fa-diagram-project"></i> Flujo Detallado
      </a>
      <a href="diagrama_especiales.html" class="px-3 py-1 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 {'active bg-sky-600 text-white shadow-xs' if nav_active == 'especiales' else 'text-slate-600 hover:text-sky-700 hover:bg-white'}">
        <i class="fa-solid fa-shield-halved"></i> Casos Especiales
      </a>
      <a href="diagrama_ejecutivo.html" class="px-3 py-1 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 {'active bg-sky-600 text-white shadow-xs' if nav_active == 'ejecutivo' else 'text-slate-600 hover:text-sky-700 hover:bg-white'}">
        <i class="fa-solid fa-layer-group"></i> Ejecutivo
      </a>
    </nav>

    <!-- HERRAMIENTAS DE EXPORTACIÓN Y VISTA -->
    <div class="flex items-center gap-1.5">
      <button onclick="toggleLegendModal()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Ver Leyenda de Colores">
        <i class="fa-solid fa-palette text-amber-600"></i> Leyenda
      </button>
      <button onclick="exportSvg()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Descargar SVG">
        <i class="fa-solid fa-download text-sky-600"></i> SVG
      </button>
      <button onclick="exportPng()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Descargar PNG">
        <i class="fa-solid fa-image text-emerald-600"></i> PNG
      </button>
      <button onclick="copyMermaidSource()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Copiar código fuente Mermaid">
        <i class="fa-regular fa-copy text-indigo-600"></i> Mermaid
      </button>
      <button onclick="toggleFullscreen()" class="p-1.5 text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors" title="Pantalla completa">
        <i class="fa-solid fa-expand text-xs"></i>
      </button>
    </div>
  </header>

  <!-- BARRA SECUNDARIA: NAVEGACIÓN RÁPIDA, BÚSQUEDA Y CONTROLES ZOOM -->
  <div class="bg-slate-50 border-b border-slate-200 px-4 py-2 flex flex-wrap items-center justify-between gap-2.5 z-10 shrink-0">
    <div class="flex items-center gap-1.5 overflow-x-auto py-0.5 max-w-full">
      <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1 shrink-0 flex items-center gap-1">
        <i class="fa-solid fa-location-dot"></i> Saltar:
      </span>
      {jump_buttons_html}
    </div>

    <div class="flex items-center gap-2 ml-auto shrink-0">
      <div class="relative flex items-center">
        <i class="fa-solid fa-magnifying-glass absolute left-2.5 text-slate-400 text-xs pointer-events-none"></i>
        <input type="text" id="search-input" placeholder="Buscar nodo, cargo, pago..." 
               class="pl-7 pr-16 py-1 text-xs border border-slate-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent w-48 transition-all"
               oninput="handleSearch()" onkeydown="handleSearchKey(event)">
        <div class="absolute right-1.5 flex items-center gap-0.5">
          <button onclick="searchPrev()" class="p-1 text-[10px] text-slate-400 hover:text-sky-700" title="Coincidencia anterior">
            <i class="fa-solid fa-chevron-up"></i>
          </button>
          <button onclick="searchNext()" class="p-1 text-[10px] text-slate-400 hover:text-sky-700" title="Siguiente coincidencia">
            <i class="fa-solid fa-chevron-down"></i>
          </button>
        </div>
      </div>
      <span id="search-status" class="text-[11px] font-semibold text-slate-500 hidden min-w-[70px]"></span>

      <button id="wheel-mode-btn" onclick="toggleWheelMode()" class="px-2.5 py-1 text-xs font-medium bg-white text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 transition-all flex items-center gap-1.5 shadow-xs" title="Alternar entre modo Desplazamiento y Zoom">
        <i class="fa-solid fa-hand text-sky-600"></i> <span class="hidden sm:inline">2 Dedos: Desplazar</span>
      </button>

      <div class="flex items-center bg-white border border-slate-300 rounded-lg shadow-xs overflow-hidden">
        <button onclick="zoomIn()" class="px-2.5 py-1 text-xs hover:bg-slate-100 text-slate-700 border-r border-slate-200" title="Acercar (Zoom +)">
          <i class="fa-solid fa-plus"></i>
        </button>
        <button onclick="zoomOut()" class="px-2.5 py-1 text-xs hover:bg-slate-100 text-slate-700 border-r border-slate-200" title="Alejar (Zoom -)">
          <i class="fa-solid fa-minus"></i>
        </button>
        <button onclick="resetZoom()" class="px-2.5 py-1 text-xs hover:bg-slate-100 text-slate-700 border-r border-slate-200" title="Ajuste óptimo / Reiniciar">
          <i class="fa-solid fa-arrows-to-eye"></i>
        </button>
        <button onclick="fitToWidth()" class="px-2.5 py-1 text-xs hover:bg-slate-100 text-slate-700" title="Ajustar al ancho">
          <i class="fa-solid fa-arrows-left-right-to-line"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- CONTENEDOR PRINCIPAL DEL DIAGRAMA Y DRAWER DE INSPECTOR -->
  <main class="flex-1 relative overflow-hidden flex">
    <div id="container" class="diagram-viewport flex-1 flex items-center justify-center">
      <div id="mermaid-target" class="w-full h-full flex items-center justify-center">
        <div class="text-slate-500 font-semibold flex items-center gap-3">
          <i class="fa-solid fa-circle-notch fa-spin text-sky-600 text-xl"></i>
          <span>Renderizando diagrama interactivo en ultra alta definición...</span>
        </div>
      </div>
    </div>

    <!-- PANEL LATERAL INSPECTOR DE NODOS (DRAWER) -->
    <aside id="node-inspector" class="w-84 bg-white border-l border-slate-200 shadow-xl flex flex-col transition-all duration-300 translate-x-full absolute right-0 top-0 bottom-0 z-30">
      <div class="p-3.5 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 rounded-md bg-sky-100 text-sky-700 flex items-center justify-center text-xs">
            <i class="fa-solid fa-info"></i>
          </div>
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Ficha de Actuación / Cargo</h3>
        </div>
        <button onclick="closeInspector()" class="text-slate-400 hover:text-slate-600 p-1">
          <i class="fa-solid fa-xmark text-sm"></i>
        </button>
      </div>
      
      <div class="p-4 overflow-y-auto flex-1 space-y-4 text-xs">
        <div>
          <span id="inspect-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-200">
            Nodo General
          </span>
          <h4 id="inspect-title" class="text-sm font-bold text-slate-900 mt-2 leading-snug">
            Selecciona un nodo
          </h4>
        </div>

        <div id="inspect-desc-box" class="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1.5">
          <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Descripción y Detalle Funcional</div>
          <p id="inspect-desc" class="text-slate-600 leading-relaxed text-[11.5px]"></p>
        </div>

        <div id="inspect-code-box" class="hidden p-3 bg-sky-50 border border-sky-200 rounded-xl space-y-1">
          <div class="text-[10px] font-bold text-sky-800 uppercase tracking-wider flex items-center justify-between">
            <span>Código de Estado / Conclusión</span>
            <button onclick="copyInspectCode()" class="text-sky-600 hover:text-sky-800 text-[11px]" title="Copiar código">
              <i class="fa-regular fa-copy"></i>
            </button>
          </div>
          <code id="inspect-code" class="text-xs font-bold text-sky-900 font-mono block break-all"></code>
        </div>

        <div id="inspect-phase-box" class="p-3 bg-amber-50/50 border border-amber-200/60 rounded-xl space-y-1">
          <div class="text-[10px] font-bold text-amber-800 uppercase tracking-wider">Fase / Unidad Orgánica Competente</div>
          <p id="inspect-phase" class="text-slate-700 font-medium text-[11.5px]"></p>
        </div>

        <div class="pt-2 flex flex-col gap-2">
          <button onclick="focusCurrentInspectedNode()" class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold rounded-lg shadow-xs flex items-center justify-center gap-1.5 transition-colors">
            <i class="fa-solid fa-crosshairs"></i> Centrar en este nodo
          </button>
        </div>
      </div>
    </aside>
  </main>

  <!-- PIE DE PÁGINA INFORMATIVO Y LEYENDA RÁPIDA -->
  <footer class="bg-white border-t border-slate-200 px-4 py-2 flex flex-wrap items-center justify-between gap-3 text-[11px] text-slate-500 z-10 shrink-0">
    <div class="flex items-center gap-4 flex-wrap">
      <span class="flex items-center gap-1.5 font-medium"><i class="fa-solid fa-circle-check text-emerald-600"></i> Conforme al RAS Modificado 2026 MPCH</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Conclusión Favorable / Pago Con Dcto.</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span> Archivo / Sanción Coactiva</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500 inline-block"></span> Decisión Jurídica</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-fuchsia-500 inline-block"></span> Acción del Administrado</span>
    </div>
    <div class="flex items-center gap-3 font-medium">
      <span>💡 2 dedos para navegar flujo • Pellizco para zoom • Clic en nodo para ver detalles</span>
    </div>
  </footer>

  <!-- MODAL DE LEYENDA DETALLADA -->
  <div id="legend-modal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center z-50 hidden p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full border border-slate-200 overflow-hidden">
      <div class="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <h3 class="text-sm font-bold text-slate-800 flex items-center gap-2">
          <i class="fa-solid fa-palette text-amber-500"></i> Leyenda Semántica del Diagrama
        </h3>
        <button onclick="toggleLegendModal()" class="text-slate-400 hover:text-slate-600 p-1">
          <i class="fa-solid fa-xmark text-base"></i>
        </button>
      </div>
      <div class="p-5 space-y-3 text-xs">
        <div class="flex items-center gap-3 p-2 rounded-lg bg-sky-50 border border-sky-200">
          <div class="w-6 h-6 rounded-md bg-sky-600 text-white flex items-center justify-center font-bold">🏁</div>
          <div><div class="font-bold text-sky-900">Inicio del Procedimiento</div><div class="text-sky-700 text-[11px]">Detección in situ, patrullaje o denuncia ciudadana</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-indigo-50 border border-indigo-200">
          <div class="w-6 h-6 rounded-md bg-indigo-600 text-white flex items-center justify-center font-bold">⚖️</div>
          <div><div class="font-bold text-indigo-900">Decisión / Bifurcación Jurídica</div><div class="text-indigo-700 text-[11px]">Evaluación legal de descargos, indicios o recursos</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-fuchsia-50 border border-fuchsia-200">
          <div class="w-6 h-6 rounded-md bg-fuchsia-600 text-white flex items-center justify-center font-bold">🧑💼</div>
          <div><div class="font-bold text-fuchsia-900">Acción del Administrado</div><div class="text-fuchsia-700 text-[11px]">Descargos (5d), alegatos (5d), apelaciones o subsanación</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-emerald-50 border border-emerald-200">
          <div class="w-6 h-6 rounded-md bg-emerald-600 text-white flex items-center justify-center font-bold">💰</div>
          <div><div class="font-bold text-emerald-900">Régimen de Pagos con Descuento</div><div class="text-emerald-700 text-[11px]">40% (60% dcto), 60% (40% dcto), 70% (atenuante), 80% (20% dcto)</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-rose-50 border border-rose-200">
          <div class="w-6 h-6 rounded-md bg-rose-600 text-white flex items-center justify-center font-bold">🛑</div>
          <div><div class="font-bold text-rose-900">Conclusión Sancionadora / Coactiva</div><div class="text-rose-700 text-[11px]">Resolución de sanción, REC, embargos o demolición</div></div>
        </div>
      </div>
      <div class="px-5 py-3 bg-slate-50 border-t border-slate-200 flex justify-end">
        <button onclick="toggleLegendModal()" class="px-4 py-1.5 bg-slate-800 text-white rounded-lg text-xs font-semibold hover:bg-slate-700">Entendido</button>
      </div>
    </div>
  </div>

  <script type="text/plain" id="raw-mermaid">
{mmd_content.strip()}
  </script>

  <script>
    mermaid.initialize({{
      startOnLoad: false,
      theme: 'default',
      securityLevel: 'loose',
      flowchart: {{
        htmlLabels: true,
        curve: 'basis',
        useMaxWidth: false
      }}
    }});

    let panZoomInstance = null;
    let currentlyInspectedElement = null;
    let searchMatches = [];
    let currentMatchIndex = -1;

{NAV_HANDLER_JS}

    async function renderDiagram() {{
      const rawCode = document.getElementById('raw-mermaid').innerText.trim();
      const target = document.getElementById('mermaid-target');
      
      if (panZoomInstance) {{
        panZoomInstance.destroy();
        panZoomInstance = null;
      }}

      try {{
        const id = 'mermaid-svg-' + Math.floor(Math.random() * 1000000);
        const {{ svg }} = await mermaid.render(id, rawCode);
        target.innerHTML = svg;
        
        const svgElement = target.querySelector('svg');
        if (svgElement) {{
          panZoomInstance = svgPanZoom(svgElement, {{
            zoomEnabled: true,
            controlIconsEnabled: false,
            fit: false,
            center: false,
            minZoom: 0.05,
            maxZoom: 15,
            zoomScaleSensitivity: 0.2,
            mouseWheelZoomEnabled: false,
            customEventsHandler: {{
              haltEventListeners: ['touchstart', 'touchend', 'touchmove', 'touchleave', 'touchcancel'],
              init: function(options) {{
                if (currentNavHandler) {{
                  currentNavHandler.destroy();
                }}
                currentNavHandler = createNavigationHandler(options.svgElement, options.instance);
              }},
              destroy: function() {{
                if (currentNavHandler) {{
                  currentNavHandler.destroy();
                  currentNavHandler = null;
                }}
              }}
            }}
          }});

          fitOptimalReading(svgElement);
          setupNodeInteractions(svgElement);
        }}
      }} catch (err) {{
        console.error('Error renderizando Mermaid:', err);
        target.innerHTML = '<div class="text-rose-600 p-6 bg-rose-50 rounded-xl border border-rose-200"><b>Error de renderizado:</b> ' + err.message + '</div>';
      }}
    }}

    function fitOptimalReading(svgElement) {{
      if (!panZoomInstance || !svgElement) return;
      const container = document.getElementById('container');
      const containerWidth = container.clientWidth;
      const bbox = svgElement.getBBox();
      
      const isLR = '{nav_active}' === 'ejecutivo';
      if (isLR) {{
        panZoomInstance.fit();
        panZoomInstance.center();
      }} else {{
        const targetScale = Math.min(1.0, (containerWidth - 60) / bbox.width);
        panZoomInstance.zoom(targetScale);
        const panX = (containerWidth - (bbox.width * targetScale)) / 2;
        panZoomInstance.pan({{ x: panX, y: 30 }});
      }}
    }}

    function fitToWidth() {{
      const svgElement = document.querySelector('#mermaid-target svg');
      if (svgElement) {{
        fitOptimalReading(svgElement);
      }}
    }}

    function zoomIn() {{
      if (panZoomInstance) panZoomInstance.zoomIn();
    }}

    function zoomOut() {{
      if (panZoomInstance) panZoomInstance.zoomOut();
    }}

    function resetZoom() {{
      if (panZoomInstance) {{
        panZoomInstance.reset();
        fitOptimalReading(document.querySelector('#mermaid-target svg'));
      }}
    }}

    function jumpToNode(nodePrefix) {{
      if (!panZoomInstance) return;
      const svg = document.querySelector('#mermaid-target svg');
      if (!svg) return;

      let targetEl = svg.querySelector(`[id^="flowchart-${{nodePrefix}}-"]`) || 
                     svg.querySelector(`[id*="${{nodePrefix}}"]`) ||
                     svg.querySelector(`.${{nodePrefix}}`);
      
      if (!targetEl) {{
        const allNodes = svg.querySelectorAll('.node, .cluster');
        for (let node of allNodes) {{
          if (node.textContent.toLowerCase().includes(nodePrefix.toLowerCase())) {{
            targetEl = node;
            break;
          }}
        }}
      }}

      if (targetEl) {{
        const bbox = targetEl.getBBox();
        const container = document.getElementById('container');
        const zoom = Math.max(0.9, panZoomInstance.getZoom());
        
        panZoomInstance.zoom(zoom);
        const panX = (container.clientWidth / 2) - (bbox.x + bbox.width / 2) * zoom;
        const panY = 70 - (bbox.y * zoom);
        
        panZoomInstance.pan({{ x: panX, y: panY }});
        
        targetEl.classList.add('node-highlighted');
        setTimeout(() => targetEl.classList.remove('node-highlighted'), 2500);

        if (targetEl.classList.contains('node')) {{
          inspectNode(targetEl);
        }}
      }}
    }}

    function setupNodeInteractions(svg) {{
      svg.querySelectorAll('.node').forEach(node => {{
        node.addEventListener('click', (e) => {{
          if (currentNavHandler && currentNavHandler.isUserDragging()) return;
          e.stopPropagation();
          inspectNode(node);
        }});
      }});

      svg.addEventListener('click', () => {{
        if (currentNavHandler && currentNavHandler.isUserDragging()) return;
        if (currentlyInspectedElement) {{
          currentlyInspectedElement.classList.remove('node-selected');
          currentlyInspectedElement = null;
        }}
      }});
    }}

    function inspectNode(nodeEl) {{
      if (currentlyInspectedElement) {{
        currentlyInspectedElement.classList.remove('node-selected');
      }}
      currentlyInspectedElement = nodeEl;
      nodeEl.classList.add('node-selected');

      const drawer = document.getElementById('node-inspector');
      const badge = document.getElementById('inspect-badge');
      const title = document.getElementById('inspect-title');
      const desc = document.getElementById('inspect-desc');
      const codeBox = document.getElementById('inspect-code-box');
      const code = document.getElementById('inspect-code');
      const phase = document.getElementById('inspect-phase');

      const fullText = nodeEl.textContent.trim();
      
      const codeMatch = fullText.match(/📌\\s*([A-Z0-9_]+)/);
      if (codeMatch) {{
        codeBox.classList.remove('hidden');
        code.innerText = codeMatch[1];
      }} else {{
        codeBox.classList.add('hidden');
      }}

      const smallEl = nodeEl.querySelector('small');
      const bEl = nodeEl.querySelector('b') || nodeEl.querySelector('strong');

      if (bEl) {{
        title.innerHTML = bEl.innerHTML;
      }} else {{
        title.innerText = fullText.split('\\n')[0].replace(/📌.*/, '');
      }}

      if (smallEl) {{
        desc.innerHTML = smallEl.innerHTML;
      }} else {{
        desc.innerText = fullText.replace(/📌.*/, '').replace(title.innerText, '').trim() || 'Actuación dentro del procedimiento administrativo según RAS 2026.';
      }}

      let clusterEl = nodeEl.closest('.cluster');
      if (clusterEl) {{
        const clusterLabel = clusterEl.querySelector('.cluster-label') || clusterEl.querySelector('text');
        phase.innerText = clusterLabel ? clusterLabel.textContent.trim() : 'Fase General del Procedimiento';
      }} else {{
        phase.innerText = 'Flujo del Procedimiento Administrativo Sancionador (PAS)';
      }}

      if (nodeEl.classList.contains('termOk')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300';
        badge.innerText = 'Conclusión Favorable / Archivo';
      }} else if (nodeEl.classList.contains('pago')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-green-100 text-green-800 border border-green-300';
        badge.innerText = 'Régimen de Pago Extintivo';
      }} else if (nodeEl.classList.contains('admin')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-fuchsia-100 text-fuchsia-800 border border-fuchsia-300';
        badge.innerText = 'Acción del Administrado';
      }} else if (nodeEl.classList.contains('termWarn')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-rose-100 text-rose-800 border border-rose-300';
        badge.innerText = 'Archivo / Conclusión Sancionadora';
      }} else if (nodeEl.classList.contains('decision')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-indigo-100 text-indigo-800 border border-indigo-300';
        badge.innerText = 'Decisión Jurídica';
      }} else if (nodeEl.classList.contains('alerta')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-amber-100 text-amber-800 border border-amber-300';
        badge.innerText = 'Punto Crítico / Alerta';
      }} else if (nodeEl.classList.contains('destacado')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-sky-100 text-sky-800 border border-sky-300';
        badge.innerText = 'Acto Administrativo Formal';
      }} else {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-200';
        badge.innerText = 'Actividad de Trámite';
      }}

      drawer.classList.remove('translate-x-full');
    }}

    function closeInspector() {{
      const drawer = document.getElementById('node-inspector');
      drawer.classList.add('translate-x-full');
      if (currentlyInspectedElement) {{
        currentlyInspectedElement.classList.remove('node-selected');
        currentlyInspectedElement = null;
      }}
    }}

    function focusCurrentInspectedNode() {{
      if (!currentlyInspectedElement || !panZoomInstance) return;
      const bbox = currentlyInspectedElement.getBBox();
      const container = document.getElementById('container');
      const zoom = Math.max(1.2, panZoomInstance.getZoom());
      panZoomInstance.zoom(zoom);
      panZoomInstance.pan({{
        x: (container.clientWidth / 2) - (bbox.x + bbox.width / 2) * zoom,
        y: (container.clientHeight / 2) - (bbox.y + bbox.height / 2) * zoom
      }});
    }}

    function copyInspectCode() {{
      const code = document.getElementById('inspect-code').innerText;
      navigator.clipboard.writeText(code).then(() => {{
        alert('Código copiado: ' + code);
      }});
    }}

    function handleSearch() {{
      const query = document.getElementById('search-input').value.trim().toLowerCase();
      const svg = document.querySelector('#mermaid-target svg');
      const status = document.getElementById('search-status');
      
      if (!svg) return;

      svg.querySelectorAll('.node-highlighted').forEach(el => el.classList.remove('node-highlighted'));
      searchMatches = [];
      currentMatchIndex = -1;

      if (!query) {{
        status.classList.add('hidden');
        return;
      }}

      const allNodes = svg.querySelectorAll('.node');
      allNodes.forEach(node => {{
        if (node.textContent.toLowerCase().includes(query)) {{
          node.classList.add('node-highlighted');
          searchMatches.push(node);
        }}
      }});

      status.classList.remove('hidden');
      if (searchMatches.length > 0) {{
        status.innerText = `${{searchMatches.length}} coincidencia(s)`;
        status.className = 'text-[11px] font-bold text-sky-700 block';
        currentMatchIndex = 0;
        focusSearchMatch(0);
      }} else {{
        status.innerText = 'Sin resultados';
        status.className = 'text-[11px] font-medium text-rose-600 block';
      }}
    }}

    function handleSearchKey(e) {{
      if (e.key === 'Enter') {{
        if (e.shiftKey) {{
          searchPrev();
        }} else {{
          searchNext();
        }}
      }}
    }}

    function searchNext() {{
      if (searchMatches.length === 0) return;
      currentMatchIndex = (currentMatchIndex + 1) % searchMatches.length;
      focusSearchMatch(currentMatchIndex);
    }}

    function searchPrev() {{
      if (searchMatches.length === 0) return;
      currentMatchIndex = (currentMatchIndex - 1 + searchMatches.length) % searchMatches.length;
      focusSearchMatch(currentMatchIndex);
    }}

    function focusSearchMatch(index) {{
      if (index < 0 || index >= searchMatches.length || !panZoomInstance) return;
      const target = searchMatches[index];
      const bbox = target.getBBox();
      const container = document.getElementById('container');
      const zoom = Math.max(1.0, panZoomInstance.getZoom());
      panZoomInstance.zoom(zoom);
      panZoomInstance.pan({{
        x: (container.clientWidth / 2) - (bbox.x + bbox.width / 2) * zoom,
        y: (container.clientHeight / 2) - (bbox.y + bbox.height / 2) * zoom
      }});
      inspectNode(target);
    }}

    function toggleLegendModal() {{
      const modal = document.getElementById('legend-modal');
      modal.classList.toggle('hidden');
    }}

    function copyMermaidSource() {{
      const rawCode = document.getElementById('raw-mermaid').innerText.trim();
      navigator.clipboard.writeText(rawCode).then(() => {{
        alert('Código fuente Mermaid copiado al portapapeles.');
      }});
    }}

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(err => alert('No se pudo activar pantalla completa'));
      }} else {{
        document.exitFullscreen();
      }}
    }}

    function exportSvg() {{
      const svg = document.querySelector('#mermaid-target svg');
      if (!svg) return;
      const serializer = new XMLSerializer();
      const svgBlob = new Blob([serializer.serializeToString(svg)], {{type: 'image/svg+xml;charset=utf-8'}});
      const url = URL.createObjectURL(svgBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = '{filename.replace(".html", "")}.svg';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }}

    function exportPng() {{
      const svg = document.querySelector('#mermaid-target svg');
      if (!svg) return;
      const serializer = new XMLSerializer();
      const svgString = serializer.serializeToString(svg);
      const svgBlob = new Blob([svgString], {{type: 'image/svg+xml;charset=utf-8'}});
      const URLObj = window.URL || window.webkitURL || window;
      const blobURL = URLObj.createObjectURL(svgBlob);
      
      const image = new Image();
      image.onload = () => {{
        const canvas = document.createElement('canvas');
        canvas.width = svg.getBoundingClientRect().width * 2;
        canvas.height = svg.getBoundingClientRect().height * 2;
        const context = canvas.getContext('2d');
        context.fillStyle = '#ffffff';
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.drawImage(image, 0, 0, canvas.width, canvas.height);
        
        const png = canvas.toDataURL('image/png');
        const a = document.createElement('a');
        a.href = png;
        a.download = '{filename.replace(".html", "")}.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }};
      image.src = blobURL;
    }}

    window.addEventListener('DOMContentLoaded', renderDiagram);
    window.addEventListener('resize', () => {{
      const svg = document.querySelector('#mermaid-target svg');
      if (svg && panZoomInstance) fitOptimalReading(svg);
    }});
  </script>
</body>
</html>
"""
    return html

# 1. Flujo Detallado
jumps_optimizado = [
    {"target": "FASE1", "icon": "📡", "label": "1. Detección (Dcto 60%)"},
    {"target": "FASE2", "icon": "⚖️", "label": "2. Instrucción (Dcto 40% / Exim / Aten)"},
    {"target": "FASE3", "icon": "🏛️", "label": "3. Sanción (Dcto 20% / GM)"},
    {"target": "FASE4", "icon": "🚨", "label": "4. Coactiva SATCH (100% + Costas)"}
]
html_optimizado = generate_standalone_html(
    title="Diagrama de Flujo Integral del PAS (RAS 2026)",
    subtitle="Mapeo detallado de cargos, subdirecciones, acciones del administrado y régimen de pagos",
    filename="diagrama_optimizado.html",
    mmd_content=optimizado_mmd,
    nav_active="optimizado",
    quick_jumps=jumps_optimizado
)

# 2. Casos Especiales y Caducidad
jumps_especiales = [
    {"target": "SG_CAD", "icon": "⏱️", "label": "Caducidad y Prescripción"},
    {"target": "P_CLAU", "icon": "🔒", "label": "Clausura (48h)"},
    {"target": "P_RET", "icon": "📦", "label": "Retención y Donación"},
    {"target": "P_SAN", "icon": "🥫", "label": "Decomiso Sanitario (5d)"},
    {"target": "P_OBRA", "icon": "🏗️", "label": "Paralización de Obra (15d)"},
    {"target": "P_CAUTELAR", "icon": "🛡️", "label": "Medidas Cautelares (2d)"}
]
html_especiales = generate_standalone_html(
    title="Procedimientos Especiales y Control de Plazos",
    subtitle="Medidas complementarias, procedimiento cautelar, caducidad y prescripción",
    filename="diagrama_especiales.html",
    mmd_content=especiales_mmd,
    nav_active="especiales",
    quick_jumps=jumps_especiales
)

# 3. Diagrama Ejecutivo
jumps_ejecutivo = [
    {"target": "M1", "icon": "👮", "label": "1. Campo (Dcto 60%)"},
    {"target": "M2", "icon": "⚖️", "label": "2. Instrucción (Dcto 40% / 0% / 30%)"},
    {"target": "M3", "icon": "🏛️", "label": "3. Sanción (Dcto 20% / Recursos)"},
    {"target": "M4", "icon": "💰", "label": "4. Coactiva (100% + Costas)"},
    {"target": "M5", "icon": "🛡️", "label": "5. Garantías y Plazos"}
]
html_ejecutivo = generate_standalone_html(
    title="Diagrama Ejecutivo Panorámico Macro",
    subtitle="Visión global de las 4 fases del PAS, responsables por área y régimen económico",
    filename="diagrama_ejecutivo.html",
    mmd_content=ejecutivo_mmd,
    nav_active="ejecutivo",
    quick_jumps=jumps_ejecutivo
)

# 4. Portal Unificado index.html
jumps_portal_json = json.dumps({
    "optimizado": jumps_optimizado,
    "especiales": jumps_especiales,
    "ejecutivo": jumps_ejecutivo
})

html_index = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portal de Fiscalización y PAS - Municipalidad Provincial de Chiclayo</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/svg-pan-zoom@3.6.1/dist/svg-pan-zoom.min.js"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
{CSS_SHARED}
  </style>
</head>
<body class="bg-slate-100 text-slate-800 flex flex-col h-screen overflow-hidden">

  <!-- CABECERA PRINCIPAL DEL PORTAL -->
  <header class="bg-white border-b border-slate-200 px-4 py-2.5 flex flex-wrap items-center justify-between gap-3 shadow-xs z-20 shrink-0">
    <div class="flex items-center gap-3">
      <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-700 to-sky-500 flex items-center justify-center text-white shadow-sm">
        <i class="fa-solid fa-city text-base"></i>
      </div>
      <div>
        <div class="flex items-center gap-2">
          <h1 class="text-sm font-extrabold text-slate-900 tracking-tight leading-none">Portal Integral de Fiscalización y PAS</h1>
          <span class="px-2 py-0.5 text-[10px] font-bold bg-sky-100 text-sky-800 rounded-full border border-sky-200">MPCH • RAS 2026</span>
        </div>
        <p class="text-[11px] text-slate-500 font-medium leading-none mt-1">Visor Unificado de Flujos Procedimentales según RAS Modificado y Ley N° 27444</p>
      </div>
    </div>

    <!-- PESTAÑAS DE CAMBIO DIRECTO ENTRE LOS 3 DIAGRAMAS -->
    <div class="flex items-center bg-slate-100 p-1 rounded-xl border border-slate-200 shadow-inner">
      <button id="tab-optimizado" onclick="switchView('optimizado')" class="tab-btn px-3 py-1 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 active">
        <i class="fa-solid fa-diagram-project"></i> Flujo Detallado
      </button>
      <button id="tab-especiales" onclick="switchView('especiales')" class="tab-btn px-3 py-1 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 text-slate-600 hover:text-sky-700">
        <i class="fa-solid fa-shield-halved"></i> Casos Especiales
      </button>
      <button id="tab-ejecutivo" onclick="switchView('ejecutivo')" class="tab-btn px-3 py-1 text-xs font-semibold rounded-lg transition-all flex items-center gap-1.5 text-slate-600 hover:text-sky-700">
        <i class="fa-solid fa-layer-group"></i> Ejecutivo
      </button>
    </div>

    <!-- ACCIONES: ABRIR EN PESTAÑA INDEPENDIENTE, GUÍA RAS Y EXPORTACIÓN -->
    <div class="flex items-center gap-1.5">
      <a id="btn-open-standalone" href="diagrama_optimizado.html" target="_blank" class="px-2.5 py-1.5 text-xs font-semibold text-sky-700 bg-sky-50 border border-sky-200 rounded-lg hover:bg-sky-100 transition-colors flex items-center gap-1.5 shadow-xs" title="Abrir en pestaña independiente">
        <i class="fa-solid fa-arrow-up-right-from-square"></i> <span class="hidden md:inline">Vista Independiente</span>
      </a>
      <button onclick="toggleRasModal()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Ver Resumen de Plazos y Descuentos RAS">
        <i class="fa-solid fa-book-bookmark text-sky-600"></i> <span class="hidden sm:inline">Guía RAS</span>
      </button>
      <button onclick="toggleLegendModal()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Ver Leyenda de Colores">
        <i class="fa-solid fa-palette text-amber-600"></i> Leyenda
      </button>
      <button onclick="exportSvg()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Descargar SVG">
        <i class="fa-solid fa-download text-sky-600"></i> SVG
      </button>
      <button onclick="exportPng()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Descargar PNG">
        <i class="fa-solid fa-image text-emerald-600"></i> PNG
      </button>
      <button onclick="copyCurrentMermaid()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Copiar código fuente Mermaid">
        <i class="fa-regular fa-copy text-indigo-600"></i>
      </button>
      <button onclick="toggleFullscreen()" class="p-1.5 text-slate-600 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors" title="Pantalla completa">
        <i class="fa-solid fa-expand text-xs"></i>
      </button>
    </div>
  </header>

  <!-- BARRA SECUNDARIA DINÁMICA -->
  <div class="bg-slate-50 border-b border-slate-200 px-4 py-2 flex flex-wrap items-center justify-between gap-2.5 z-10 shrink-0">
    <div id="quick-jumps-bar" class="flex items-center gap-1.5 overflow-x-auto py-0.5 max-w-full"></div>

    <div class="flex items-center gap-2 ml-auto shrink-0">
      <div class="relative flex items-center">
        <i class="fa-solid fa-magnifying-glass absolute left-2.5 text-slate-400 text-xs pointer-events-none"></i>
        <input type="text" id="search-input" placeholder="Buscar nodo, cargo, pago..." 
               class="pl-7 pr-16 py-1 text-xs border border-slate-300 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent w-48 transition-all"
               oninput="handleSearch()" onkeydown="handleSearchKey(event)">
        <div class="absolute right-1.5 flex items-center gap-0.5">
          <button onclick="searchPrev()" class="p-1 text-[10px] text-slate-400 hover:text-sky-700" title="Coincidencia anterior">
            <i class="fa-solid fa-chevron-up"></i>
          </button>
          <button onclick="searchNext()" class="p-1 text-[10px] text-slate-400 hover:text-sky-700" title="Siguiente coincidencia">
            <i class="fa-solid fa-chevron-down"></i>
          </button>
        </div>
      </div>
      <span id="search-status" class="text-[11px] font-semibold text-slate-500 hidden min-w-[70px]"></span>

      <button id="wheel-mode-btn" onclick="toggleWheelMode()" class="px-2.5 py-1 text-xs font-medium bg-white text-slate-700 border border-slate-300 rounded-lg hover:bg-slate-50 transition-all flex items-center gap-1.5 shadow-xs" title="Alternar entre modo Desplazamiento y Zoom">
        <i class="fa-solid fa-hand text-sky-600"></i> <span class="hidden sm:inline">2 Dedos: Desplazar</span>
      </button>

      <div class="flex items-center bg-white border border-slate-300 rounded-lg shadow-xs overflow-hidden">
        <button onclick="zoomIn()" class="px-2.5 py-1 text-xs hover:bg-slate-100 text-slate-700 border-r border-slate-200" title="Acercar (Zoom +)">
          <i class="fa-solid fa-plus"></i>
        </button>
        <button onclick="zoomOut()" class="px-2.5 py-1 text-xs hover:bg-slate-100 text-slate-700 border-r border-slate-200" title="Alejar (Zoom -)">
          <i class="fa-solid fa-minus"></i>
        </button>
        <button onclick="resetZoom()" class="px-2.5 py-1 text-xs hover:bg-slate-100 text-slate-700 border-r border-slate-200" title="Ajuste óptimo / Reiniciar">
          <i class="fa-solid fa-arrows-to-eye"></i>
        </button>
        <button onclick="fitToWidth()" class="px-2.5 py-1 text-xs hover:bg-slate-100 text-slate-700" title="Ajustar al ancho">
          <i class="fa-solid fa-arrows-left-right-to-line"></i>
        </button>
      </div>
    </div>
  </div>

  <!-- CONTENEDOR DEL DIAGRAMA Y DRAWER DE INSPECTOR -->
  <main class="flex-1 relative overflow-hidden flex">
    <div id="container" class="diagram-viewport flex-1 flex items-center justify-center">
      <div id="mermaid-target" class="w-full h-full flex items-center justify-center">
        <div class="text-slate-500 font-semibold flex items-center gap-3">
          <i class="fa-solid fa-circle-notch fa-spin text-sky-600 text-xl"></i>
          <span>Cargando visualizador...</span>
        </div>
      </div>
    </div>

    <!-- PANEL LATERAL INSPECTOR DE NODOS (DRAWER) -->
    <aside id="node-inspector" class="w-84 bg-white border-l border-slate-200 shadow-xl flex flex-col transition-all duration-300 translate-x-full absolute right-0 top-0 bottom-0 z-30">
      <div class="p-3.5 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 rounded-md bg-sky-100 text-sky-700 flex items-center justify-center text-xs">
            <i class="fa-solid fa-info"></i>
          </div>
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Ficha de Actuación / Cargo</h3>
        </div>
        <button onclick="closeInspector()" class="text-slate-400 hover:text-slate-600 p-1">
          <i class="fa-solid fa-xmark text-sm"></i>
        </button>
      </div>
      
      <div class="p-4 overflow-y-auto flex-1 space-y-4 text-xs">
        <div>
          <span id="inspect-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-200">
            Nodo General
          </span>
          <h4 id="inspect-title" class="text-sm font-bold text-slate-900 mt-2 leading-snug">
            Selecciona un nodo
          </h4>
        </div>

        <div id="inspect-desc-box" class="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1.5">
          <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Descripción y Detalle Funcional</div>
          <p id="inspect-desc" class="text-slate-600 leading-relaxed text-[11.5px]"></p>
        </div>

        <div id="inspect-code-box" class="hidden p-3 bg-sky-50 border border-sky-200 rounded-xl space-y-1">
          <div class="text-[10px] font-bold text-sky-800 uppercase tracking-wider flex items-center justify-between">
            <span>Código de Estado / Conclusión</span>
            <button onclick="copyInspectCode()" class="text-sky-600 hover:text-sky-800 text-[11px]" title="Copiar código">
              <i class="fa-regular fa-copy"></i>
            </button>
          </div>
          <code id="inspect-code" class="text-xs font-bold text-sky-900 font-mono block break-all"></code>
        </div>

        <div id="inspect-phase-box" class="p-3 bg-amber-50/50 border border-amber-200/60 rounded-xl space-y-1">
          <div class="text-[10px] font-bold text-amber-800 uppercase tracking-wider">Fase / Unidad Orgánica Competente</div>
          <p id="inspect-phase" class="text-slate-700 font-medium text-[11.5px]"></p>
        </div>

        <div class="pt-2 flex flex-col gap-2">
          <button onclick="focusCurrentInspectedNode()" class="w-full py-2 bg-sky-600 hover:bg-sky-700 text-white font-semibold rounded-lg shadow-xs flex items-center justify-center gap-1.5 transition-colors">
            <i class="fa-solid fa-crosshairs"></i> Centrar en este nodo
          </button>
        </div>
      </div>
    </aside>
  </main>

  <!-- PIE DE PÁGINA INFORMATIVO Y LEYENDA RÁPIDA -->
  <footer class="bg-white border-t border-slate-200 px-4 py-2 flex flex-wrap items-center justify-between gap-3 text-[11px] text-slate-500 z-10 shrink-0">
    <div class="flex items-center gap-4 flex-wrap">
      <span class="flex items-center gap-1.5 font-medium"><i class="fa-solid fa-circle-check text-emerald-600"></i> RAS Modificado 2026 • Municipalidad Provincial de Chiclayo</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Conclusión Favorable / Pago Con Dcto.</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span> Archivo / Coactiva</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500 inline-block"></span> Decisión Jurídica</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-fuchsia-500 inline-block"></span> Acción del Administrado</span>
    </div>
    <div class="flex items-center gap-3 font-medium">
      <span>💡 2 dedos para navegar flujo • Pellizco para zoom • Clic en nodo para ver detalles</span>
    </div>
  </footer>

  <!-- MODAL DE LA GUÍA NORMATIVA RAS -->
  <div id="ras-modal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center z-50 hidden p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full border border-slate-200 overflow-hidden max-h-[90vh] flex flex-col">
      <div class="px-6 py-4 bg-sky-800 text-white flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <i class="fa-solid fa-scale-balanced text-lg text-sky-200"></i>
          <h3 class="text-sm font-bold tracking-tight">Guía Operativa del RAS Modificado 2026 - MPCH</h3>
        </div>
        <button onclick="toggleRasModal()" class="text-sky-200 hover:text-white p-1">
          <i class="fa-solid fa-xmark text-base"></i>
        </button>
      </div>
      <div class="p-6 overflow-y-auto space-y-4 text-xs">
        <div>
          <h4 class="font-bold text-slate-800 uppercase tracking-wider text-[11px] mb-2 text-sky-900 border-b pb-1">
            1. Esquema de Gradualidad y Descuentos de Multas (Art. 16 y 41 RAS)
          </h4>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-2.5">
            <div class="p-2.5 rounded-xl bg-emerald-50 border border-emerald-200">
              <div class="font-bold text-emerald-900">Pronto Pago (Art. 16.a)</div>
              <div class="text-[11px] text-emerald-800 font-semibold mt-0.5">Paga el 40% (60% de descuento)</div>
              <p class="text-slate-600 text-[10.5px] mt-1">Dentro de 5 días hábiles siguientes a la papeleta, al contado y sin haber presentado descargos.</p>
            </div>
            <div class="p-2.5 rounded-xl bg-blue-50 border border-blue-200">
              <div class="font-bold text-blue-900">Pago Anticipado (Art. 16.b)</div>
              <div class="text-[11px] text-blue-800 font-semibold mt-0.5">Paga el 60% (40% de descuento)</div>
              <p class="text-slate-600 text-[10.5px] mt-1">Del 6to día hábil posterior a la papeleta hasta antes de notificar el Inicio del PAS, sin descargos.</p>
            </div>
            <div class="p-2.5 rounded-xl bg-purple-50 border border-purple-200">
              <div class="font-bold text-purple-900">Régimen Atenuante (Art. 41)</div>
              <div class="text-[11px] text-purple-800 font-semibold mt-0.5">Paga el 70% (30% de descuento)</div>
              <p class="text-slate-600 text-[10.5px] mt-1">Por allanamiento expreso o regularización voluntaria post-inicio antes del IFI. MPCH no aplica medida final.</p>
            </div>
            <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-200">
              <div class="font-bold text-amber-900">Pago Voluntario Sanción (Art. 16.c)</div>
              <div class="text-[11px] text-amber-800 font-semibold mt-0.5">Paga el 80% (20% de descuento)</div>
              <p class="text-slate-600 text-[10.5px] mt-1">Dentro de los 15 días hábiles de notificada la sanción, sin haber presentado ningún recurso.</p>
            </div>
          </div>
          <div class="mt-2.5 p-2 rounded-lg bg-rose-50 border border-rose-200 text-[11px] text-rose-900">
            <b>Cobranza Coactiva SATCH (Art. 82):</b> Vencidos los 15 días tras la sanción sin recurso ni pago voluntario, se deriva al SATCH para cobro del <b>100% de la multa + costas y gastos procesales</b>.
          </div>
        </div>

        <div>
          <h4 class="font-bold text-slate-800 uppercase tracking-wider text-[11px] mb-2 text-sky-900 border-b pb-1">
            2. Plazos Perentorios para el Administrado y la Autoridad
          </h4>
          <ul class="space-y-1.5 text-slate-600 text-[11px]">
            <li><b>Descargos al Inicio del PAS:</b> 5 días hábiles tras notificación de la resolución de inicio (Art. 38).</li>
            <li><b>Descargos / Alegatos al IFI:</b> 5 días hábiles tras notificación del IFI por la Gerencia de Seguridad Ciudadana (Art. 43).</li>
            <li><b>Recurso de Reconsideración:</b> 15 días hábiles con prueba nueva ante el Gerente Sancionador (Art. 49).</li>
            <li><b>Recurso de Apelación:</b> 15 días hábiles por puro derecho ante Gerencia Municipal (agota la vía) (Art. 50).</li>
            <li><b>Apelación contra Medida Cautelar:</b> 3 días calendario ante Subgerente; Gerente resuelve en 2 días (Art. 79).</li>
            <li><b>Levantamiento de Clausura Temporal:</b> Subgerencia de Fiscalización resuelve en 48 horas (silencio positivo) (Art. 65.a).</li>
            <li><b>Caducidad del PAS:</b> 9 meses perentorios prorrogables a 12 meses antes del vencimiento (Art. 62).</li>
            <li><b>Prescripción de Infracciones:</b> 4 años desde la papeleta o cese de la conducta (Art. 60).</li>
          </ul>
        </div>
      </div>
      <div class="px-6 py-3 bg-slate-50 border-t border-slate-200 flex justify-end">
        <button onclick="toggleRasModal()" class="px-4 py-1.5 bg-slate-800 text-white rounded-lg text-xs font-semibold hover:bg-slate-700">Cerrar Guía</button>
      </div>
    </div>
  </div>

  <!-- MODAL DE LEYENDA DETALLADA -->
  <div id="legend-modal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center z-50 hidden p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full border border-slate-200 overflow-hidden">
      <div class="px-5 py-3.5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
        <h3 class="text-sm font-bold text-slate-800 flex items-center gap-2">
          <i class="fa-solid fa-palette text-amber-500"></i> Leyenda Semántica del Diagrama
        </h3>
        <button onclick="toggleLegendModal()" class="text-slate-400 hover:text-slate-600 p-1">
          <i class="fa-solid fa-xmark text-base"></i>
        </button>
      </div>
      <div class="p-5 space-y-3 text-xs">
        <div class="flex items-center gap-3 p-2 rounded-lg bg-sky-50 border border-sky-200">
          <div class="w-6 h-6 rounded-md bg-sky-600 text-white flex items-center justify-center font-bold">🏁</div>
          <div><div class="font-bold text-sky-900">Inicio del Procedimiento</div><div class="text-sky-700 text-[11px]">Detección in situ o denuncia ciudadana</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-indigo-50 border border-indigo-200">
          <div class="w-6 h-6 rounded-md bg-indigo-600 text-white flex items-center justify-center font-bold">⚖️</div>
          <div><div class="font-bold text-indigo-900">Decisión / Bifurcación Jurídica</div><div class="text-indigo-700 text-[11px]">Evaluación legal de descargos, indicios o recursos</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-fuchsia-50 border border-fuchsia-200">
          <div class="w-6 h-6 rounded-md bg-fuchsia-600 text-white flex items-center justify-center font-bold">🧑💼</div>
          <div><div class="font-bold text-fuchsia-900">Acción del Administrado</div><div class="text-fuchsia-700 text-[11px]">Descargos (5d), alegatos (5d), apelaciones o subsanación</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-emerald-50 border border-emerald-200">
          <div class="w-6 h-6 rounded-md bg-emerald-600 text-white flex items-center justify-center font-bold">💰</div>
          <div><div class="font-bold text-emerald-900">Régimen de Pagos con Descuento</div><div class="text-emerald-700 text-[11px]">40% (60% dcto), 60% (40% dcto), 70% (atenuante), 80% (20% dcto)</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-rose-50 border border-rose-200">
          <div class="w-6 h-6 rounded-md bg-rose-600 text-white flex items-center justify-center font-bold">🛑</div>
          <div><div class="font-bold text-rose-900">Conclusión Sancionadora / Coactiva</div><div class="text-rose-700 text-[11px]">Resolución de sanción, REC, embargos o demolición</div></div>
        </div>
      </div>
      <div class="px-5 py-3 bg-slate-50 border-t border-slate-200 flex justify-end">
        <button onclick="toggleLegendModal()" class="px-4 py-1.5 bg-slate-800 text-white rounded-lg text-xs font-semibold hover:bg-slate-700">Entendido</button>
      </div>
    </div>
  </div>

  <!-- CÓDIGO FUENTE DE LOS 3 DIAGRAMAS EN BEACONS JS -->
  <script type="text/plain" id="source-optimizado">
{optimizado_mmd.strip()}
  </script>
  <script type="text/plain" id="source-especiales">
{especiales_mmd.strip()}
  </script>
  <script type="text/plain" id="source-ejecutivo">
{ejecutivo_mmd.strip()}
  </script>

  <script>
    mermaid.initialize({{
      startOnLoad: false,
      theme: 'default',
      securityLevel: 'loose',
      flowchart: {{
        htmlLabels: true,
        curve: 'basis',
        useMaxWidth: false
      }}
    }});

    const QUICK_JUMPS_MAP = {jumps_portal_json};

    let currentView = 'optimizado';
    let panZoomInstance = null;
    let currentlyInspectedElement = null;
    let searchMatches = [];
    let currentMatchIndex = -1;

{NAV_HANDLER_JS}

    async function switchView(viewName) {{
      currentView = viewName;
      
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active', 'bg-sky-600', 'text-white', 'shadow-xs'));
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.add('text-slate-600'));
      
      const activeBtn = document.getElementById('tab-' + viewName);
      if (activeBtn) {{
        activeBtn.classList.add('active', 'bg-sky-600', 'text-white', 'shadow-xs');
        activeBtn.classList.remove('text-slate-600');
      }}

      const btnStandalone = document.getElementById('btn-open-standalone');
      btnStandalone.href = 'diagrama_' + viewName + '.html';

      updateQuickJumpsBar(viewName);

      const target = document.getElementById('mermaid-target');
      target.innerHTML = `
        <div class="text-slate-500 font-semibold flex items-center gap-3">
          <i class="fa-solid fa-circle-notch fa-spin text-sky-600 text-xl"></i>
          <span>Cargando vista de ${{viewName}}...</span>
        </div>
      `;

      closeInspector();

      if (panZoomInstance) {{
        panZoomInstance.destroy();
        panZoomInstance = null;
      }}

      const rawCode = document.getElementById('source-' + viewName).innerText.trim();

      try {{
        const id = 'mermaid-svg-' + Math.floor(Math.random() * 1000000);
        const {{ svg }} = await mermaid.render(id, rawCode);
        target.innerHTML = svg;
        
        const svgElement = target.querySelector('svg');
        if (svgElement) {{
          panZoomInstance = svgPanZoom(svgElement, {{
            zoomEnabled: true,
            controlIconsEnabled: false,
            fit: false,
            center: false,
            minZoom: 0.05,
            maxZoom: 15,
            zoomScaleSensitivity: 0.2,
            mouseWheelZoomEnabled: false,
            customEventsHandler: {{
              haltEventListeners: ['touchstart', 'touchend', 'touchmove', 'touchleave', 'touchcancel'],
              init: function(options) {{
                if (currentNavHandler) {{
                  currentNavHandler.destroy();
                }}
                currentNavHandler = createNavigationHandler(options.svgElement, options.instance);
              }},
              destroy: function() {{
                if (currentNavHandler) {{
                  currentNavHandler.destroy();
                  currentNavHandler = null;
                }}
              }}
            }}
          }});

          fitOptimalReading(svgElement);
          setupNodeInteractions(svgElement);
        }}
      }} catch (err) {{
        console.error('Error renderizando Mermaid:', err);
        target.innerHTML = '<div class="text-rose-600 p-6 bg-rose-50 rounded-xl border border-rose-200"><b>Error de renderizado:</b> ' + err.message + '</div>';
      }}
    }}

    function updateQuickJumpsBar(viewName) {{
      const bar = document.getElementById('quick-jumps-bar');
      const jumps = QUICK_JUMPS_MAP[viewName] || [];
      let html = `
        <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1 shrink-0 flex items-center gap-1">
          <i class="fa-solid fa-location-dot"></i> Saltar:
        </span>
      `;
      jumps.forEach(j => {{
        html += `
          <button onclick="jumpToNode('${{j.target}}')" class="px-2.5 py-1 text-xs font-semibold bg-white text-slate-700 border border-slate-200 rounded-lg hover:bg-slate-50 hover:text-sky-700 hover:border-sky-300 transition-all flex items-center gap-1 shadow-xs whitespace-nowrap">
            <span>${{j.icon}}</span> <span>${{j.label}}</span>
          </button>
        `;
      }});
      bar.innerHTML = html;
    }}

    function fitOptimalReading(svgElement) {{
      if (!panZoomInstance || !svgElement) return;
      const container = document.getElementById('container');
      const containerWidth = container.clientWidth;
      const bbox = svgElement.getBBox();
      
      const isLR = currentView === 'ejecutivo';
      if (isLR) {{
        panZoomInstance.fit();
        panZoomInstance.center();
      }} else {{
        const targetScale = Math.min(1.0, (containerWidth - 60) / bbox.width);
        panZoomInstance.zoom(targetScale);
        const panX = (containerWidth - (bbox.width * targetScale)) / 2;
        panZoomInstance.pan({{ x: panX, y: 30 }});
      }}
    }}

    function fitToWidth() {{
      const svgElement = document.querySelector('#mermaid-target svg');
      if (svgElement) fitOptimalReading(svgElement);
    }}

    function zoomIn() {{
      if (panZoomInstance) panZoomInstance.zoomIn();
    }}

    function zoomOut() {{
      if (panZoomInstance) panZoomInstance.zoomOut();
    }}

    function resetZoom() {{
      if (panZoomInstance) {{
        panZoomInstance.reset();
        fitOptimalReading(document.querySelector('#mermaid-target svg'));
      }}
    }}

    function jumpToNode(nodePrefix) {{
      if (!panZoomInstance) return;
      const svg = document.querySelector('#mermaid-target svg');
      if (!svg) return;

      let targetEl = svg.querySelector(`[id^="flowchart-${{nodePrefix}}-"]`) || 
                     svg.querySelector(`[id*="${{nodePrefix}}"]`) ||
                     svg.querySelector(`.${{nodePrefix}}`);
      
      if (!targetEl) {{
        const allNodes = svg.querySelectorAll('.node, .cluster');
        for (let node of allNodes) {{
          if (node.textContent.toLowerCase().includes(nodePrefix.toLowerCase())) {{
            targetEl = node;
            break;
          }}
        }}
      }}

      if (targetEl) {{
        const bbox = targetEl.getBBox();
        const container = document.getElementById('container');
        const zoom = Math.max(0.9, panZoomInstance.getZoom());
        
        panZoomInstance.zoom(zoom);
        const panX = (container.clientWidth / 2) - (bbox.x + bbox.width / 2) * zoom;
        const panY = 70 - (bbox.y * zoom);
        
        panZoomInstance.pan({{ x: panX, y: panY }});
        
        targetEl.classList.add('node-highlighted');
        setTimeout(() => targetEl.classList.remove('node-highlighted'), 2500);

        if (targetEl.classList.contains('node')) {{
          inspectNode(targetEl);
        }}
      }}
    }}

    function setupNodeInteractions(svg) {{
      svg.querySelectorAll('.node').forEach(node => {{
        node.addEventListener('click', (e) => {{
          if (currentNavHandler && currentNavHandler.isUserDragging()) return;
          e.stopPropagation();
          inspectNode(node);
        }});
      }});

      svg.addEventListener('click', () => {{
        if (currentNavHandler && currentNavHandler.isUserDragging()) return;
        if (currentlyInspectedElement) {{
          currentlyInspectedElement.classList.remove('node-selected');
          currentlyInspectedElement = null;
        }}
      }});
    }}

    function inspectNode(nodeEl) {{
      if (currentlyInspectedElement) {{
        currentlyInspectedElement.classList.remove('node-selected');
      }}
      currentlyInspectedElement = nodeEl;
      nodeEl.classList.add('node-selected');

      const drawer = document.getElementById('node-inspector');
      const badge = document.getElementById('inspect-badge');
      const title = document.getElementById('inspect-title');
      const desc = document.getElementById('inspect-desc');
      const codeBox = document.getElementById('inspect-code-box');
      const code = document.getElementById('inspect-code');
      const phase = document.getElementById('inspect-phase');

      const fullText = nodeEl.textContent.trim();
      
      const codeMatch = fullText.match(/📌\\s*([A-Z0-9_]+)/);
      if (codeMatch) {{
        codeBox.classList.remove('hidden');
        code.innerText = codeMatch[1];
      }} else {{
        codeBox.classList.add('hidden');
      }}

      const smallEl = nodeEl.querySelector('small');
      const bEl = nodeEl.querySelector('b') || nodeEl.querySelector('strong');

      if (bEl) {{
        title.innerHTML = bEl.innerHTML;
      }} else {{
        title.innerText = fullText.split('\\n')[0].replace(/📌.*/, '');
      }}

      if (smallEl) {{
        desc.innerHTML = smallEl.innerHTML;
      }} else {{
        desc.innerText = fullText.replace(/📌.*/, '').replace(title.innerText, '').trim() || 'Actuación dentro del procedimiento administrativo según RAS 2026.';
      }}

      let clusterEl = nodeEl.closest('.cluster');
      if (clusterEl) {{
        const clusterLabel = clusterEl.querySelector('.cluster-label') || clusterEl.querySelector('text');
        phase.innerText = clusterLabel ? clusterLabel.textContent.trim() : 'Fase General del Procedimiento';
      }} else {{
        phase.innerText = 'Flujo del Procedimiento Administrativo Sancionador (PAS)';
      }}

      if (nodeEl.classList.contains('termOk')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300';
        badge.innerText = 'Conclusión Favorable / Archivo';
      }} else if (nodeEl.classList.contains('pago')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-green-100 text-green-800 border border-green-300';
        badge.innerText = 'Régimen de Pago Extintivo';
      }} else if (nodeEl.classList.contains('admin')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-fuchsia-100 text-fuchsia-800 border border-fuchsia-300';
        badge.innerText = 'Acción del Administrado';
      }} else if (nodeEl.classList.contains('termWarn')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-rose-100 text-rose-800 border border-rose-300';
        badge.innerText = 'Archivo / Conclusión Sancionadora';
      }} else if (nodeEl.classList.contains('decision')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-indigo-100 text-indigo-800 border border-indigo-300';
        badge.innerText = 'Decisión Jurídica';
      }} else if (nodeEl.classList.contains('alerta')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-amber-100 text-amber-800 border border-amber-300';
        badge.innerText = 'Punto Crítico / Alerta';
      }} else if (nodeEl.classList.contains('destacado')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-sky-100 text-sky-800 border border-sky-300';
        badge.innerText = 'Acto Administrativo Formal';
      }} else {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-slate-100 text-slate-700 border border-slate-200';
        badge.innerText = 'Actividad de Trámite';
      }}

      drawer.classList.remove('translate-x-full');
    }}

    function closeInspector() {{
      const drawer = document.getElementById('node-inspector');
      drawer.classList.add('translate-x-full');
      if (currentlyInspectedElement) {{
        currentlyInspectedElement.classList.remove('node-selected');
        currentlyInspectedElement = null;
      }}
    }}

    function focusCurrentInspectedNode() {{
      if (!currentlyInspectedElement || !panZoomInstance) return;
      const bbox = currentlyInspectedElement.getBBox();
      const container = document.getElementById('container');
      const zoom = Math.max(1.2, panZoomInstance.getZoom());
      panZoomInstance.zoom(zoom);
      panZoomInstance.pan({{
        x: (container.clientWidth / 2) - (bbox.x + bbox.width / 2) * zoom,
        y: (container.clientHeight / 2) - (bbox.y + bbox.height / 2) * zoom
      }});
    }}

    function copyInspectCode() {{
      const code = document.getElementById('inspect-code').innerText;
      navigator.clipboard.writeText(code).then(() => {{
        alert('Código copiado: ' + code);
      }});
    }}

    function handleSearch() {{
      const query = document.getElementById('search-input').value.trim().toLowerCase();
      const svg = document.querySelector('#mermaid-target svg');
      const status = document.getElementById('search-status');
      
      if (!svg) return;

      svg.querySelectorAll('.node-highlighted').forEach(el => el.classList.remove('node-highlighted'));
      searchMatches = [];
      currentMatchIndex = -1;

      if (!query) {{
        status.classList.add('hidden');
        return;
      }}

      const allNodes = svg.querySelectorAll('.node');
      allNodes.forEach(node => {{
        if (node.textContent.toLowerCase().includes(query)) {{
          node.classList.add('node-highlighted');
          searchMatches.push(node);
        }}
      }});

      status.classList.remove('hidden');
      if (searchMatches.length > 0) {{
        status.innerText = `${{searchMatches.length}} coincidencia(s)`;
        status.className = 'text-[11px] font-bold text-sky-700 block';
        currentMatchIndex = 0;
        focusSearchMatch(0);
      }} else {{
        status.innerText = 'Sin resultados';
        status.className = 'text-[11px] font-medium text-rose-600 block';
      }}
    }}

    function handleSearchKey(e) {{
      if (e.key === 'Enter') {{
        if (e.shiftKey) {{
          searchPrev();
        }} else {{
          searchNext();
        }}
      }}
    }}

    function searchNext() {{
      if (searchMatches.length === 0) return;
      currentMatchIndex = (currentMatchIndex + 1) % searchMatches.length;
      focusSearchMatch(currentMatchIndex);
    }}

    function searchPrev() {{
      if (searchMatches.length === 0) return;
      currentMatchIndex = (currentMatchIndex - 1 + searchMatches.length) % searchMatches.length;
      focusSearchMatch(currentMatchIndex);
    }}

    function focusSearchMatch(index) {{
      if (index < 0 || index >= searchMatches.length || !panZoomInstance) return;
      const target = searchMatches[index];
      const bbox = target.getBBox();
      const container = document.getElementById('container');
      const zoom = Math.max(1.0, panZoomInstance.getZoom());
      panZoomInstance.zoom(zoom);
      panZoomInstance.pan({{
        x: (container.clientWidth / 2) - (bbox.x + bbox.width / 2) * zoom,
        y: (container.clientHeight / 2) - (bbox.y + bbox.height / 2) * zoom
      }});
      inspectNode(target);
    }}

    function toggleRasModal() {{
      const modal = document.getElementById('ras-modal');
      modal.classList.toggle('hidden');
    }}

    function toggleLegendModal() {{
      const modal = document.getElementById('legend-modal');
      modal.classList.toggle('hidden');
    }}

    function copyCurrentMermaid() {{
      const rawCode = document.getElementById('source-' + currentView).innerText.trim();
      navigator.clipboard.writeText(rawCode).then(() => {{
        alert('Código fuente Mermaid de [' + currentView + '] copiado al portapapeles.');
      }});
    }}

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen().catch(err => alert('No se pudo activar pantalla completa'));
      }} else {{
        document.exitFullscreen();
      }}
    }}

    function exportSvg() {{
      const svg = document.querySelector('#mermaid-target svg');
      if (!svg) return;
      const serializer = new XMLSerializer();
      const svgBlob = new Blob([serializer.serializeToString(svg)], {{type: 'image/svg+xml;charset=utf-8'}});
      const url = URL.createObjectURL(svgBlob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'diagrama_' + currentView + '.svg';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }}

    function exportPng() {{
      const svg = document.querySelector('#mermaid-target svg');
      if (!svg) return;
      const serializer = new XMLSerializer();
      const svgString = serializer.serializeToString(svg);
      const svgBlob = new Blob([svgString], {{type: 'image/svg+xml;charset=utf-8'}});
      const URLObj = window.URL || window.webkitURL || window;
      const blobURL = URLObj.createObjectURL(svgBlob);
      
      const image = new Image();
      image.onload = () => {{
        const canvas = document.createElement('canvas');
        canvas.width = svg.getBoundingClientRect().width * 2;
        canvas.height = svg.getBoundingClientRect().height * 2;
        const context = canvas.getContext('2d');
        context.fillStyle = '#ffffff';
        context.fillRect(0, 0, canvas.width, canvas.height);
        context.drawImage(image, 0, 0, canvas.width, canvas.height);
        
        const png = canvas.toDataURL('image/png');
        const a = document.createElement('a');
        a.href = png;
        a.download = 'diagrama_' + currentView + '.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }};
      image.src = blobURL;
    }}

    window.addEventListener('DOMContentLoaded', () => switchView('optimizado'));
    window.addEventListener('resize', () => {{
      const svg = document.querySelector('#mermaid-target svg');
      if (svg && panZoomInstance) fitOptimalReading(svg);
    }});
  </script>
</body>
</html>
"""

# Guardar en BASE_DIR y en FlujoSegmentadoRAS
TARGET_DIRS = [BASE_DIR, os.path.join(BASE_DIR, "FlujoSegmentadoRAS")]

for directory in TARGET_DIRS:
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, "diagrama_optimizado.html"), "w", encoding="utf-8") as f:
        f.write(html_optimizado)
    with open(os.path.join(directory, "diagrama_especiales.html"), "w", encoding="utf-8") as f:
        f.write(html_especiales)
    with open(os.path.join(directory, "diagrama_ejecutivo.html"), "w", encoding="utf-8") as f:
        f.write(html_ejecutivo)
    with open(os.path.join(directory, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_index)

print("✓ Todos los archivos HTML generados exitosamente en ambos directorios.")
