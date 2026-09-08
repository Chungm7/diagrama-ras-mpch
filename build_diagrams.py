# -*- coding: utf-8 -*-
"""
Generador de Visualizadores HTML Interactivos para los diagramas Mermaid del PAS - MPCH.
Genera:
1. diagrama_optimizado.html (Flujo detallado completo e independiente)
2. diagrama_especiales.html (Medidas complementarias y control de caducidad)
3. diagrama_ejecutivo.html (Visión panorámica macro)
4. index.html (Portal central unificado con navegación integrada entre los 3 diagramas)
"""

import os
import json

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(filename):
    path = os.path.join(WORKSPACE_DIR, filename)
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
    font-size: 12.5px !important;
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
    font-size: 13.5px !important;
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

  /* EFECTO DE RESALTADO EN BÚSQUEDA Y SELECCIÓN */
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

  <!-- CABECERA PRINCIPAL CON NAVEGACIÓN ENTRE DIAGRAMAS -->
  <header class="bg-white border-b border-slate-200 px-4 py-2.5 flex flex-wrap items-center justify-between gap-3 shadow-xs z-20 shrink-0">
    <div class="flex items-center gap-3">
      <a href="index.html" class="flex items-center gap-2.5 text-slate-800 hover:text-sky-700 transition-colors group" title="Ir al Portal Maestro">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-700 to-sky-500 flex items-center justify-center text-white shadow-sm group-hover:scale-105 transition-transform">
          <i class="fa-solid fa-scale-balanced text-base"></i>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h1 class="text-sm font-extrabold text-slate-900 tracking-tight leading-none group-hover:text-sky-700">{title}</h1>
            <span class="px-2 py-0.5 text-[10px] font-bold bg-sky-100 text-sky-800 rounded-full border border-sky-200">RAS • MPCH</span>
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
      <button onclick="exportSvg()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Descargar en formato vectorial SVG">
        <i class="fa-solid fa-download text-sky-600"></i> SVG
      </button>
      <button onclick="exportPng()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Descargar como imagen PNG de alta resolución">
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
        <input type="text" id="search-input" placeholder="Buscar nodo, artículo..." 
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
    <aside id="node-inspector" class="w-80 bg-white border-l border-slate-200 shadow-xl flex flex-col transition-all duration-300 translate-x-full absolute right-0 top-0 bottom-0 z-30">
      <div class="p-3.5 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 rounded-md bg-sky-100 text-sky-700 flex items-center justify-center text-xs">
            <i class="fa-solid fa-info"></i>
          </div>
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Ficha de Nodo / Actuación</h3>
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
          <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Descripción y Detalle</div>
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
          <div class="text-[10px] font-bold text-amber-800 uppercase tracking-wider">Fase / Módulo Pertinente</div>
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
      <span class="flex items-center gap-1.5 font-medium"><i class="fa-solid fa-circle-check text-emerald-600"></i> Mapeo 100% Norma RAS</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Conclusión Favorable</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span> Archivo / Sanción Coactiva</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500 inline-block"></span> Decisión Jurídica</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span> Alerta de Caducidad / Plazo</span>
    </div>
    <div class="flex items-center gap-3 font-medium">
      <span>💡 Haz clic en cualquier nodo para ver sus detalles normativos</span>
      <span class="text-slate-300">|</span>
      <span>Generado con estándar Archify</span>
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
          <div><div class="font-bold text-sky-900">Inicio del Procedimiento</div><div class="text-sky-700 text-[11px]">Punto de arranque del PAS (Detección in situ o Denuncia)</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-indigo-50 border border-indigo-200">
          <div class="w-6 h-6 rounded-md bg-indigo-600 text-white flex items-center justify-center font-bold">⚖️</div>
          <div><div class="font-bold text-indigo-900">Decisión / Bifurcación Jurídica</div><div class="text-indigo-700 text-[11px]">Evaluación con plazos y alternativas procedimentales</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-blue-50 border border-blue-200">
          <div class="w-6 h-6 rounded-md bg-blue-600 text-white flex items-center justify-center font-bold">📄</div>
          <div><div class="font-bold text-blue-900">Acto Administrativo Destacado</div><div class="text-blue-700 text-[11px]">Papeleta, Resolución de Inicio, IFI o Resolución de Sanción</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-emerald-50 border border-emerald-200">
          <div class="w-6 h-6 rounded-md bg-emerald-600 text-white flex items-center justify-center font-bold">✅</div>
          <div><div class="font-bold text-emerald-900">Conclusión Favorable / Archivo</div><div class="text-emerald-700 text-[11px]">Pago pronto, subsanación, eximente, absolución o revocación</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-rose-50 border border-rose-200">
          <div class="w-6 h-6 rounded-md bg-rose-600 text-white flex items-center justify-center font-bold">🛑</div>
          <div><div class="font-bold text-rose-900">Conclusión Sancionadora / Coactiva</div><div class="text-rose-700 text-[11px]">Archivo preliminar, caducidad o embargo coactivo forzoso</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-amber-50 border border-amber-200">
          <div class="w-6 h-6 rounded-md bg-amber-600 text-white flex items-center justify-center font-bold">⚠️</div>
          <div><div class="font-bold text-amber-900">Alerta Crítica / Caducidad / Firmeza</div><div class="text-amber-700 text-[11px]">Puntos ciegos de demora pericial o consentimiento de plazos</div></div>
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
              init: function() {{}},
              destroy: function() {{}}
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
          e.stopPropagation();
          inspectNode(node);
        }});
      }});

      svg.addEventListener('click', () => {{
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
        desc.innerText = fullText.replace(/📌.*/, '').replace(title.innerText, '').trim() || 'Actuación dentro del procedimiento administrativo según ordenanza.';
      }}

      let clusterEl = nodeEl.closest('.cluster');
      if (clusterEl) {{
        const clusterLabel = clusterEl.querySelector('.cluster-label') || clusterEl.querySelector('text');
        phase.innerText = clusterLabel ? clusterLabel.textContent.trim() : 'Fase General del Procedimiento';
      }} else {{
        phase.innerText = 'Flujo de Fiscalización y Sanción (PAS)';
      }}

      if (nodeEl.classList.contains('termOk')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300';
        badge.innerText = 'Conclusión Favorable / Archivo';
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

    function focusSearchMatch(idx) {{
      if (idx < 0 || idx >= searchMatches.length || !panZoomInstance) return;
      const targetNode = searchMatches[idx];
      const bbox = targetNode.getBBox();
      const container = document.getElementById('container');
      const zoom = Math.max(1.0, panZoomInstance.getZoom());
      panZoomInstance.zoom(zoom);
      panZoomInstance.pan({{
        x: (container.clientWidth / 2) - (bbox.x + bbox.width / 2) * zoom,
        y: (container.clientHeight / 2) - (bbox.y + bbox.height / 2) * zoom
      }});
      inspectNode(targetNode);
    }}

    function exportSvg() {{
      const svgEl = document.querySelector('#mermaid-target svg');
      if (!svgEl) return;
      const clone = svgEl.cloneNode(true);
      clone.removeAttribute('style');
      const svgData = new XMLSerializer().serializeToString(clone);
      const blob = new Blob([svgData], {{ type: 'image/svg+xml;charset=utf-8' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `PAS_Chiclayo_{nav_active}_${{Date.now()}}.svg`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}

    function exportPng() {{
      const svgEl = document.querySelector('#mermaid-target svg');
      if (!svgEl) return;
      const clone = svgEl.cloneNode(true);
      clone.removeAttribute('style');
      const svgData = new XMLSerializer().serializeToString(clone);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();
      const svgBlob = new Blob([svgData], {{ type: 'image/svg+xml;charset=utf-8' }});
      const url = URL.createObjectURL(svgBlob);
      
      img.onload = function() {{
        const scale = 2;
        canvas.width = img.width * scale;
        canvas.height = img.height * scale;
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(url);
        
        const a = document.createElement('a');
        a.download = `PAS_Chiclayo_{nav_active}_${{Date.now()}}.png`;
        a.href = canvas.toDataURL('image/png');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }};
      img.src = url;
    }}

    function copyMermaidSource() {{
      const rawCode = document.getElementById('raw-mermaid').innerText.trim();
      navigator.clipboard.writeText(rawCode).then(() => {{
        alert('¡Código Mermaid ({nav_active}) copiado con éxito al portapapeles!');
      }}).catch(err => {{
        console.error('Error al copiar:', err);
      }});
    }}

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen();
      }} else if (document.exitFullscreen) {{
        document.exitFullscreen();
      }}
    }}

    function toggleLegendModal() {{
      const modal = document.getElementById('legend-modal');
      modal.classList.toggle('hidden');
    }}

    let wheelMode = localStorage.getItem('pas_wheel_mode') || 'pan';

    function toggleWheelMode() {{
      wheelMode = (wheelMode === 'pan') ? 'zoom' : 'pan';
      localStorage.setItem('pas_wheel_mode', wheelMode);
      updateWheelModeUI();
    }}

    function updateWheelModeUI() {{
      const btn = document.getElementById('wheel-mode-btn');
      if (!btn) return;
      if (wheelMode === 'pan') {{
        btn.innerHTML = '<i class="fa-solid fa-hand text-sky-600"></i> <span class="hidden sm:inline">2 Dedos: Desplazar</span>';
        btn.className = 'px-2.5 py-1 text-xs font-medium bg-sky-50 text-sky-800 border border-sky-300 rounded-lg hover:bg-sky-100 transition-all flex items-center gap-1.5 shadow-xs';
        btn.title = 'Modo actual: 2 dedos desplazan el plano en panel táctil. Clic para cambiar a Rueda = Zoom.';
      }} else {{
        btn.innerHTML = '<i class="fa-solid fa-magnifying-glass-plus text-amber-600"></i> <span class="hidden sm:inline">Rueda: Zoom</span>';
        btn.className = 'px-2.5 py-1 text-xs font-medium bg-amber-50 text-amber-900 border border-amber-300 rounded-lg hover:bg-amber-100 transition-all flex items-center gap-1.5 shadow-xs';
        btn.title = 'Modo actual: La rueda del ratón hace zoom directo. Clic para cambiar a 2 dedos desplazan.';
      }}
    }}

    function zoomAtScreenPoint(scaleMultiplier, clientX, clientY) {{
      if (!panZoomInstance) return;
      const svgElement = document.querySelector('#mermaid-target svg');
      if (!svgElement) return;

      try {{
        const ctm = svgElement.getScreenCTM();
        if (ctm) {{
          const p = svgElement.createSVGPoint();
          p.x = clientX;
          p.y = clientY;
          const svgPoint = p.matrixTransform(ctm.inverse());
          panZoomInstance.zoomAtPointBy(scaleMultiplier, svgPoint);
          return;
        }}
      }} catch (err) {{}}
      panZoomInstance.zoomBy(scaleMultiplier);
    }}

    function initGestures() {{
      const container = document.getElementById('container');
      if (!container) return;

      container.addEventListener('wheel', function(e) {{
        if (!panZoomInstance) return;
        e.preventDefault();

        if (e.ctrlKey) {{
          let delta = -e.deltaY;
          if (e.deltaMode === 1) delta *= 20;
          const step = Math.max(-80, Math.min(80, delta));
          const zoomFactor = Math.exp(step * 0.0035);
          zoomAtScreenPoint(zoomFactor, e.clientX, e.clientY);
          return;
        }}

        const multiplier = (e.deltaMode === 1) ? 20 : (e.deltaMode === 2 ? 500 : 1);
        const hasHorizontal = Math.abs(e.deltaX) > 0;

        if (hasHorizontal || wheelMode === 'pan') {{
          panZoomInstance.panBy({{
            x: -e.deltaX * multiplier,
            y: -e.deltaY * multiplier
          }});
        }} else {{
          let delta = -e.deltaY;
          if (e.deltaMode === 1) delta *= 20;
          const step = Math.max(-100, Math.min(100, delta));
          const zoomFactor = Math.exp(step * 0.0025);
          zoomAtScreenPoint(zoomFactor, e.clientX, e.clientY);
        }}
      }}, {{ passive: false }});
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      initGestures();
      updateWheelModeUI();
      renderDiagram();
    }});
  </script>
</body>
</html>
"""
    return html

# 1. Configuración y generación de diagrama_optimizado.html
jumps_optimizado = [
    {"target": "INI", "icon": "🏁", "label": "Inicio"},
    {"target": "FASE1", "icon": "📡", "label": "Fase 1: Detección"},
    {"target": "FASE2", "icon": "⚖️", "label": "Fase 2: Instrucción"},
    {"target": "FASE3", "icon": "🏛️", "label": "Fase 3: Sanción"},
    {"target": "FASE4", "icon": "🚨", "label": "Fase 4: Coactiva"},
    {"target": "SUB_EXIMENTE", "icon": "⚖️", "label": "Eximentes"},
    {"target": "SUB_APOYO", "icon": "🏢", "label": "Apoyo Técnico"},
    {"target": "SUB_RECURSOS", "icon": "📜", "label": "Recursos"},
    {"target": "T2_CADUCIDAD", "icon": "⏱️", "label": "Caducidad"}
]
html_optimizado = generate_standalone_html(
    title="Flujo de Fiscalización PAS (Detallado)",
    subtitle="Procedimiento Administrativo Sancionador Integral según RAS • Ley N° 27444",
    filename="diagrama_optimizado.html",
    mmd_content=optimizado_mmd,
    nav_active="optimizado",
    quick_jumps=jumps_optimizado
)
with open(os.path.join(WORKSPACE_DIR, "diagrama_optimizado.html"), "w", encoding="utf-8") as f:
    f.write(html_optimizado)
print("✓ Generado: diagrama_optimizado.html")

# 2. Configuración y generación de diagrama_especiales.html
jumps_especiales = [
    {"target": "SG_CAD", "icon": "⏱️", "label": "Control de Caducidad"},
    {"target": "P_CLAU", "icon": "🔒", "label": "1. Clausura Temporal"},
    {"target": "P_RET", "icon": "📦", "label": "2. Retención de Bienes"},
    {"target": "P_SAN", "icon": "🥫", "label": "3. Decomiso Sanitario"},
    {"target": "P_OBRA", "icon": "🏗️", "label": "4. Paralización de Obra"},
    {"target": "C_PRES", "icon": "⚖️", "label": "Prescripción (4 Años)"}
]
html_especiales = generate_standalone_html(
    title="Procedimientos Especiales y Control de Caducidad",
    subtitle="Medidas Complementarias (Clausura, Retención, Decomiso, Paralización) • Arts. 60-72 RAS",
    filename="diagrama_especiales.html",
    mmd_content=especiales_mmd,
    nav_active="especiales",
    quick_jumps=jumps_especiales
)
with open(os.path.join(WORKSPACE_DIR, "diagrama_especiales.html"), "w", encoding="utf-8") as f:
    f.write(html_especiales)
print("✓ Generado: diagrama_especiales.html")

# 3. Configuración y generación de diagrama_ejecutivo.html
jumps_ejecutivo = [
    {"target": "INI", "icon": "🏁", "label": "Inicio PAS"},
    {"target": "M1", "icon": "1️⃣", "label": "1. Detección y Campo"},
    {"target": "M2", "icon": "2️⃣", "label": "2. Instrucción Formal"},
    {"target": "M3", "icon": "3️⃣", "label": "3. Sanción y Recursos"},
    {"target": "M4", "icon": "4️⃣", "label": "4. Ejecución Coactiva"},
    {"target": "M5", "icon": "🛡️", "label": "5. Garantías y Caducidad"}
]
html_ejecutivo = generate_standalone_html(
    title="Diagrama Ejecutivo Consolidado",
    subtitle="Visión Panorámica de 4 Macro-Fases y Cápsulas de Conclusión del PAS",
    filename="diagrama_ejecutivo.html",
    mmd_content=ejecutivo_mmd,
    nav_active="ejecutivo",
    quick_jumps=jumps_ejecutivo
)
with open(os.path.join(WORKSPACE_DIR, "diagrama_ejecutivo.html"), "w", encoding="utf-8") as f:
    f.write(html_ejecutivo)
print("✓ Generado: diagrama_ejecutivo.html")

# 4. Generación del portal unificado index.html
html_index = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Portal de Fiscalización Municipal PAS - Municipalidad Provincial de Chiclayo</title>
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
          <span class="px-2 py-0.5 text-[10px] font-bold bg-sky-100 text-sky-800 rounded-full border border-sky-200">MPCH • RAS</span>
        </div>
        <p class="text-[11px] text-slate-500 font-medium leading-none mt-1">Visor Unificado de Flujos Procedimentales según RAS y Ley N° 27444</p>
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

    <!-- ACCIONES: ABRIR EN PESTAÑA INDEPENDIENTE, RESUMEN NORMATIVO, EXPORTACIÓN -->
    <div class="flex items-center gap-1.5">
      <a id="btn-open-standalone" href="diagrama_optimizado.html" target="_blank" class="px-2.5 py-1.5 text-xs font-semibold text-sky-700 bg-sky-50 border border-sky-200 rounded-lg hover:bg-sky-100 transition-colors flex items-center gap-1.5 shadow-xs" title="Abrir este diagrama en una pestaña independiente">
        <i class="fa-solid fa-arrow-up-right-from-square"></i> <span class="hidden md:inline">Vista Independiente</span>
      </a>
      <button onclick="toggleRasModal()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Ver Resumen de Plazos y Descuentos RAS">
        <i class="fa-solid fa-book-bookmark text-sky-600"></i> <span class="hidden sm:inline">Guía RAS</span>
      </button>
      <button onclick="toggleLegendModal()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Ver Leyenda de Colores">
        <i class="fa-solid fa-palette text-amber-600"></i> Leyenda
      </button>
      <button onclick="exportSvg()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Descargar en formato SVG">
        <i class="fa-solid fa-download text-sky-600"></i> SVG
      </button>
      <button onclick="exportPng()" class="px-2.5 py-1.5 text-xs font-medium text-slate-700 bg-white border border-slate-300 rounded-lg hover:bg-slate-50 transition-colors flex items-center gap-1.5 shadow-xs" title="Descargar como imagen PNG de alta resolución">
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

  <!-- BARRA SECUNDARIA DINÁMICA: HITOS SEGÚN EL DIAGRAMA SELECCIONADO Y CONTROLES -->
  <div class="bg-slate-50 border-b border-slate-200 px-4 py-2 flex flex-wrap items-center justify-between gap-2.5 z-10 shrink-0">
    <div id="quick-jumps-bar" class="flex items-center gap-1.5 overflow-x-auto py-0.5 max-w-full"></div>

    <div class="flex items-center gap-2 ml-auto shrink-0">
      <div class="relative flex items-center">
        <i class="fa-solid fa-magnifying-glass absolute left-2.5 text-slate-400 text-xs pointer-events-none"></i>
        <input type="text" id="search-input" placeholder="Buscar nodo, trámite..." 
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
    <aside id="node-inspector" class="w-80 bg-white border-l border-slate-200 shadow-xl flex flex-col transition-all duration-300 translate-x-full absolute right-0 top-0 bottom-0 z-30">
      <div class="p-3.5 border-b border-slate-200 bg-slate-50 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <div class="w-6 h-6 rounded-md bg-sky-100 text-sky-700 flex items-center justify-center text-xs">
            <i class="fa-solid fa-info"></i>
          </div>
          <h3 class="text-xs font-bold text-slate-800 uppercase tracking-wider">Ficha del Trámite</h3>
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
          <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Descripción y Detalle</div>
          <p id="inspect-desc" class="text-slate-600 leading-relaxed text-[11.5px]"></p>
        </div>

        <div id="inspect-code-box" class="hidden p-3 bg-sky-50 border border-sky-200 rounded-xl space-y-1">
          <div class="text-[10px] font-bold text-sky-800 uppercase tracking-wider flex items-center justify-between">
            <span>Código de Conclusión / Estado</span>
            <button onclick="copyInspectCode()" class="text-sky-600 hover:text-sky-800 text-[11px]" title="Copiar código">
              <i class="fa-regular fa-copy"></i>
            </button>
          </div>
          <code id="inspect-code" class="text-xs font-bold text-sky-900 font-mono block break-all"></code>
        </div>

        <div id="inspect-phase-box" class="p-3 bg-amber-50/50 border border-amber-200/60 rounded-xl space-y-1">
          <div class="text-[10px] font-bold text-amber-800 uppercase tracking-wider">Módulo / Subgrafo</div>
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

  <!-- PIE DE PÁGINA INFORMATIVO Y RESUMEN METADATOS -->
  <footer class="bg-white border-t border-slate-200 px-4 py-2 flex flex-wrap items-center justify-between gap-3 text-[11px] text-slate-500 z-10 shrink-0">
    <div class="flex items-center gap-4 flex-wrap">
      <span class="flex items-center gap-1.5 font-semibold text-slate-700"><i class="fa-solid fa-landmark text-sky-600"></i> Mapeo Integral RAS Chiclayo</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span> Conclusión Favorable</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-rose-500 inline-block"></span> Sanción / Coactiva</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-indigo-500 inline-block"></span> Decisión Jurídica</span>
      <span class="flex items-center gap-1.5"><span class="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span> Alerta de Plazo / Caducidad</span>
    </div>
    <div class="flex items-center gap-3 font-medium">
      <span>💡 Puedes alternar libremente de diagrama con las pestañas superiores</span>
      <span class="text-slate-300">|</span>
      <span>Generado con estándar Archify</span>
    </div>
  </footer>

  <!-- MODAL DE RESUMEN NORMATIVO RAS -->
  <div id="ras-modal" class="fixed inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center z-50 hidden p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full border border-slate-200 overflow-hidden max-h-[90vh] flex flex-col">
      <div class="px-5 py-4 bg-gradient-to-r from-sky-700 to-sky-600 text-white flex items-center justify-between shrink-0">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-lg bg-white/20 flex items-center justify-center text-white">
            <i class="fa-solid fa-scale-unbalanced text-sm"></i>
          </div>
          <div>
            <h3 class="text-sm font-bold leading-tight">Síntesis Normativa del RAS - Chiclayo</h3>
            <p class="text-[11px] text-sky-100">Reglamento de Aplicación de Sanciones Administrativas</p>
          </div>
        </div>
        <button onclick="toggleRasModal()" class="text-white/80 hover:text-white p-1">
          <i class="fa-solid fa-xmark text-lg"></i>
        </button>
      </div>
      
      <div class="p-6 overflow-y-auto space-y-4 text-xs">
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div class="p-3 rounded-xl bg-emerald-50 border border-emerald-200">
            <div class="text-[10px] font-extrabold text-emerald-800 uppercase">Pronto Pago (Fase 1)</div>
            <div class="text-xl font-black text-emerald-600 mt-1">60% Dcto.</div>
            <p class="text-[11px] text-emerald-700 mt-1">Art. 16.a RAS: Dentro de los primeros 5 días hábiles tras la papeleta.</p>
          </div>
          <div class="p-3 rounded-xl bg-blue-50 border border-blue-200">
            <div class="text-[10px] font-extrabold text-blue-800 uppercase">Pago Anticipado (Fase 2)</div>
            <div class="text-xl font-black text-blue-600 mt-1">40% Dcto.</div>
            <p class="text-[11px] text-blue-700 mt-1">Art. 16.b RAS: Antes de emitirse la Resolución de Inicio formal.</p>
          </div>
          <div class="p-3 rounded-xl bg-purple-50 border border-purple-200">
            <div class="text-[10px] font-extrabold text-purple-800 uppercase">Pago Voluntario (Fase 3)</div>
            <div class="text-xl font-black text-purple-600 mt-1">20% Dcto.</div>
            <p class="text-[11px] text-purple-700 mt-1">Art. 16.c RAS: Dentro de los 15 días tras notificada la Resolución de Sanción.</p>
          </div>
        </div>

        <div class="space-y-2">
          <h4 class="font-bold text-slate-900 uppercase text-[11px] tracking-wider">Reglas Críticas de Caducidad y Prescripción</h4>
          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200 space-y-2 text-slate-700 leading-relaxed">
            <p>⏱️ <b>Caducidad Ordinaria (Art. 62 RAS / Ley 27444):</b> El plazo perentorio máximo para resolver y notificar el PAS es de <b>9 meses</b> computados desde la notificación de la Imputación de Cargos.</p>
            <p>⏳ <b>Ampliación Excepcional:</b> Puede ampliarse por <b>3 meses adicionales</b> (total 12 meses) solo mediante resolución motivada emitida antes del vencimiento original.</p>
            <p>⚖️ <b>Prescripción de la Infracción (Art. 60 RAS):</b> La facultad de la autoridad para determinar infracciones prescribe a los <b>4 años</b> computados desde cometida la falta.</p>
            <p>🛡️ <b>Medidas Complementarias (Arts. 65-72 RAS):</b> Clausura temporal (levantamiento automático si no hay objeción en 48h), Retención (1 día perecibles, 30 días no perecibles), Decomiso (peritaje bromatológico máx. 5 días), y Paralización de Obra (subsanación 30 días).</p>
          </div>
        </div>
      </div>

      <div class="px-5 py-3 bg-slate-50 border-t border-slate-200 flex justify-end shrink-0">
        <button onclick="toggleRasModal()" class="px-4 py-1.5 bg-slate-800 text-white rounded-lg text-xs font-semibold hover:bg-slate-700">Cerrar</button>
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
          <div><div class="font-bold text-sky-900">Inicio del Procedimiento</div><div class="text-sky-700 text-[11px]">Punto de arranque del PAS (Detección in situ o Denuncia)</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-indigo-50 border border-indigo-200">
          <div class="w-6 h-6 rounded-md bg-indigo-600 text-white flex items-center justify-center font-bold">⚖️</div>
          <div><div class="font-bold text-indigo-900">Decisión / Bifurcación Jurídica</div><div class="text-indigo-700 text-[11px]">Evaluación con plazos y alternativas procedimentales</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-blue-50 border border-blue-200">
          <div class="w-6 h-6 rounded-md bg-blue-600 text-white flex items-center justify-center font-bold">📄</div>
          <div><div class="font-bold text-blue-900">Acto Administrativo Destacado</div><div class="text-blue-700 text-[11px]">Papeleta, Resolución de Inicio, IFI o Resolución de Sanción</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-emerald-50 border border-emerald-200">
          <div class="w-6 h-6 rounded-md bg-emerald-600 text-white flex items-center justify-center font-bold">✅</div>
          <div><div class="font-bold text-emerald-900">Conclusión Favorable / Archivo</div><div class="text-emerald-700 text-[11px]">Pago pronto, subsanación, eximente, absolución o revocación</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-rose-50 border border-rose-200">
          <div class="w-6 h-6 rounded-md bg-rose-600 text-white flex items-center justify-center font-bold">🛑</div>
          <div><div class="font-bold text-rose-900">Conclusión Sancionadora / Coactiva</div><div class="text-rose-700 text-[11px]">Archivo preliminar, caducidad o embargo coactivo forzoso</div></div>
        </div>
        <div class="flex items-center gap-3 p-2 rounded-lg bg-amber-50 border border-amber-200">
          <div class="w-6 h-6 rounded-md bg-amber-600 text-white flex items-center justify-center font-bold">⚠️</div>
          <div><div class="font-bold text-amber-900">Alerta Crítica / Caducidad / Firmeza</div><div class="text-amber-700 text-[11px]">Puntos ciegos de demora pericial o consentimiento de plazos</div></div>
        </div>
      </div>
      <div class="px-5 py-3 bg-slate-50 border-t border-slate-200 flex justify-end">
        <button onclick="toggleLegendModal()" class="px-4 py-1.5 bg-slate-800 text-white rounded-lg text-xs font-semibold hover:bg-slate-700">Entendido</button>
      </div>
    </div>
  </div>

  <script type="text/plain" id="raw-optimizado">
{optimizado_mmd.strip()}
  </script>

  <script type="text/plain" id="raw-especiales">
{especiales_mmd.strip()}
  </script>

  <script type="text/plain" id="raw-ejecutivo">
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

    let currentView = 'optimizado';
    let panZoomInstance = null;
    let currentlyInspectedElement = null;
    let searchMatches = [];
    let currentMatchIndex = -1;

    const diagramQuickJumps = {{
      optimizado: {json.dumps(jumps_optimizado, ensure_ascii=False)},
      especiales: {json.dumps(jumps_especiales, ensure_ascii=False)},
      ejecutivo: {json.dumps(jumps_ejecutivo, ensure_ascii=False)}
    }};

    const diagramStandaloneLinks = {{
      optimizado: 'diagrama_optimizado.html',
      especiales: 'diagrama_especiales.html',
      ejecutivo: 'diagrama_ejecutivo.html'
    }};

    function updateQuickJumpsBar() {{
      const container = document.getElementById('quick-jumps-bar');
      const jumps = diagramQuickJumps[currentView] || [];
      let html = '<span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1 shrink-0 flex items-center gap-1"><i class="fa-solid fa-location-dot"></i> Saltar:</span>';
      
      jumps.forEach(j => {{
        html += `
        <button onclick="jumpToNode('${{j.target}}')" class="px-2.5 py-1 text-xs font-semibold bg-white text-slate-700 border border-slate-200 rounded-lg hover:bg-slate-50 hover:text-sky-700 hover:border-sky-300 transition-all flex items-center gap-1 shadow-xs whitespace-nowrap">
          <span>${{j.icon}}</span> <span>${{j.label}}</span>
        </button>
        `;
      }});
      container.innerHTML = html;
    }}

    function switchView(viewKey) {{
      currentView = viewKey;
      
      document.querySelectorAll('.tab-btn').forEach(btn => {{
        btn.classList.remove('active');
        btn.classList.add('text-slate-600');
      }});
      
      const activeBtn = document.getElementById('tab-' + viewKey);
      if (activeBtn) {{
        activeBtn.classList.add('active');
        activeBtn.classList.remove('text-slate-600');
      }}

      const standaloneBtn = document.getElementById('btn-open-standalone');
      if (standaloneBtn) {{
        standaloneBtn.href = diagramStandaloneLinks[viewKey];
      }}

      updateQuickJumpsBar();
      closeInspector();

      const rawCode = document.getElementById('raw-' + viewKey).innerText.trim();
      renderDiagram(rawCode);
    }}

    async function renderDiagram(code) {{
      const target = document.getElementById('mermaid-target');
      target.innerHTML = '<div class="text-slate-500 font-semibold flex items-center gap-3"><i class="fa-solid fa-circle-notch fa-spin text-sky-600 text-xl"></i><span>Generando diagrama en alta definición...</span></div>';
      
      if (panZoomInstance) {{
        panZoomInstance.destroy();
        panZoomInstance = null;
      }}

      try {{
        const id = 'mermaid-svg-' + Math.floor(Math.random() * 1000000);
        const {{ svg }} = await mermaid.render(id, code);
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
              init: function() {{}},
              destroy: function() {{}}
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
      
      if (currentView === 'ejecutivo') {{
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
          e.stopPropagation();
          inspectNode(node);
        }});
      }});

      svg.addEventListener('click', () => {{
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
        desc.innerText = fullText.replace(/📌.*/, '').replace(title.innerText, '').trim() || 'Actuación procedimental conforme al RAS y Ley N° 27444.';
      }}

      let clusterEl = nodeEl.closest('.cluster');
      if (clusterEl) {{
        const clusterLabel = clusterEl.querySelector('.cluster-label') || clusterEl.querySelector('text');
        phase.innerText = clusterLabel ? clusterLabel.textContent.trim() : 'Módulo General';
      }} else {{
        phase.innerText = 'Flujo PAS Chiclayo';
      }}

      if (nodeEl.classList.contains('termOk')) {{
        badge.className = 'px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-100 text-emerald-800 border border-emerald-300';
        badge.innerText = 'Conclusión Favorable / Archivo';
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
        status.innerText = `${{searchMatches.length}} resultado(s)`;
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

    function focusSearchMatch(idx) {{
      if (idx < 0 || idx >= searchMatches.length || !panZoomInstance) return;
      const targetNode = searchMatches[idx];
      const bbox = targetNode.getBBox();
      const container = document.getElementById('container');
      const zoom = Math.max(1.0, panZoomInstance.getZoom());
      panZoomInstance.zoom(zoom);
      panZoomInstance.pan({{
        x: (container.clientWidth / 2) - (bbox.x + bbox.width / 2) * zoom,
        y: (container.clientHeight / 2) - (bbox.y + bbox.height / 2) * zoom
      }});
      inspectNode(targetNode);
    }}

    function exportSvg() {{
      const svgEl = document.querySelector('#mermaid-target svg');
      if (!svgEl) return;
      const clone = svgEl.cloneNode(true);
      clone.removeAttribute('style');
      const svgData = new XMLSerializer().serializeToString(clone);
      const blob = new Blob([svgData], {{ type: 'image/svg+xml;charset=utf-8' }});
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `PAS_Chiclayo_${{currentView}}_${{Date.now()}}.svg`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }}

    function exportPng() {{
      const svgEl = document.querySelector('#mermaid-target svg');
      if (!svgEl) return;
      const clone = svgEl.cloneNode(true);
      clone.removeAttribute('style');
      const svgData = new XMLSerializer().serializeToString(clone);
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();
      const svgBlob = new Blob([svgData], {{ type: 'image/svg+xml;charset=utf-8' }});
      const url = URL.createObjectURL(svgBlob);
      
      img.onload = function() {{
        const scale = 2;
        canvas.width = img.width * scale;
        canvas.height = img.height * scale;
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(url);
        
        const a = document.createElement('a');
        a.download = `PAS_Chiclayo_${{currentView}}_${{Date.now()}}.png`;
        a.href = canvas.toDataURL('image/png');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      }};
      img.src = url;
    }}

    function copyCurrentMermaid() {{
      const rawCode = document.getElementById('raw-' + currentView).innerText.trim();
      navigator.clipboard.writeText(rawCode).then(() => {{
        alert('¡Código Mermaid (' + currentView + ') copiado con éxito al portapapeles!');
      }}).catch(err => {{
        console.error('Error al copiar:', err);
      }});
    }}

    function toggleFullscreen() {{
      if (!document.fullscreenElement) {{
        document.documentElement.requestFullscreen();
      }} else if (document.exitFullscreen) {{
        document.exitFullscreen();
      }}
    }}

    function toggleLegendModal() {{
      const modal = document.getElementById('legend-modal');
      modal.classList.toggle('hidden');
    }}

    function toggleRasModal() {{
      const modal = document.getElementById('ras-modal');
      modal.classList.toggle('hidden');
    }}

    let wheelMode = localStorage.getItem('pas_wheel_mode') || 'pan';

    function toggleWheelMode() {{
      wheelMode = (wheelMode === 'pan') ? 'zoom' : 'pan';
      localStorage.setItem('pas_wheel_mode', wheelMode);
      updateWheelModeUI();
    }}

    function updateWheelModeUI() {{
      const btn = document.getElementById('wheel-mode-btn');
      if (!btn) return;
      if (wheelMode === 'pan') {{
        btn.innerHTML = '<i class="fa-solid fa-hand text-sky-600"></i> <span class="hidden sm:inline">2 Dedos: Desplazar</span>';
        btn.className = 'px-2.5 py-1 text-xs font-medium bg-sky-50 text-sky-800 border border-sky-300 rounded-lg hover:bg-sky-100 transition-all flex items-center gap-1.5 shadow-xs';
        btn.title = 'Modo actual: 2 dedos desplazan el plano en panel táctil. Clic para cambiar a Rueda = Zoom.';
      }} else {{
        btn.innerHTML = '<i class="fa-solid fa-magnifying-glass-plus text-amber-600"></i> <span class="hidden sm:inline">Rueda: Zoom</span>';
        btn.className = 'px-2.5 py-1 text-xs font-medium bg-amber-50 text-amber-900 border border-amber-300 rounded-lg hover:bg-amber-100 transition-all flex items-center gap-1.5 shadow-xs';
        btn.title = 'Modo actual: La rueda del ratón hace zoom directo. Clic para cambiar a 2 dedos desplazan.';
      }}
    }}

    function zoomAtScreenPoint(scaleMultiplier, clientX, clientY) {{
      if (!panZoomInstance) return;
      const svgElement = document.querySelector('#mermaid-target svg');
      if (!svgElement) return;

      try {{
        const ctm = svgElement.getScreenCTM();
        if (ctm) {{
          const p = svgElement.createSVGPoint();
          p.x = clientX;
          p.y = clientY;
          const svgPoint = p.matrixTransform(ctm.inverse());
          panZoomInstance.zoomAtPointBy(scaleMultiplier, svgPoint);
          return;
        }}
      }} catch (err) {{}}
      panZoomInstance.zoomBy(scaleMultiplier);
    }}

    function initGestures() {{
      const container = document.getElementById('container');
      if (!container) return;

      container.addEventListener('wheel', function(e) {{
        if (!panZoomInstance) return;
        e.preventDefault();

        if (e.ctrlKey) {{
          let delta = -e.deltaY;
          if (e.deltaMode === 1) delta *= 20;
          const step = Math.max(-80, Math.min(80, delta));
          const zoomFactor = Math.exp(step * 0.0035);
          zoomAtScreenPoint(zoomFactor, e.clientX, e.clientY);
          return;
        }}

        const multiplier = (e.deltaMode === 1) ? 20 : (e.deltaMode === 2 ? 500 : 1);
        const hasHorizontal = Math.abs(e.deltaX) > 0;

        if (hasHorizontal || wheelMode === 'pan') {{
          panZoomInstance.panBy({{
            x: -e.deltaX * multiplier,
            y: -e.deltaY * multiplier
          }});
        }} else {{
          let delta = -e.deltaY;
          if (e.deltaMode === 1) delta *= 20;
          const step = Math.max(-100, Math.min(100, delta));
          const zoomFactor = Math.exp(step * 0.0025);
          zoomAtScreenPoint(zoomFactor, e.clientX, e.clientY);
        }}
      }}, {{ passive: false }});
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      initGestures();
      updateWheelModeUI();
      switchView('optimizado');
    }});
  </script>
</body>
</html>
"""

with open(os.path.join(WORKSPACE_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html_index)
print("✓ Generado: index.html")
print("\n¡Todos los archivos HTML interactivos fueron generados exitosamente!")
