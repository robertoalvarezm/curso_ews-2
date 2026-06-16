# Curso interactivo — Bifurcaciones y Señales de Alerta Temprana (EWS)

Material de curso en **Quarto**, en español (es-MX), sobre bifurcaciones en sistemas 1-D, sus manifestaciones empíricas en biología y las señales de alerta temprana de transiciones críticas. Grupo de Biología Cuantitativa, Facultad de Ciencias Naturales, UAQ.

## Cómo renderizar

```bash
# desde esta carpeta
quarto render      # genera el sitio en _site/
quarto preview     # vista previa con recarga en vivo
```

## Requisitos

- **Quarto ≥ 1.4**
- **R** con `knitr` y `rmarkdown` (el motor de render es `knitr`)
- Un navegador moderno para la lectura interactiva

> **No necesitas Python para renderizar.** Las celdas `{pyodide}` (Python) y `{webr}` (R) se ejecutan **en el navegador** vía WebAssembly (Pyodide y WebR), no durante el render. El sitio resultante es estático y se puede publicar en GitHub Pages, Quarto Pub o Netlify.

## La extensión quarto-live ya está incluida

Está en `_extensions/r-wasm/live/`, así que **no hace falta** ejecutar `quarto add`. Si quisieras actualizarla:

```bash
quarto add r-wasm/quarto-live
```

## Nota de diseño: "sitio" como libro

El proyecto usa `project: type: website` con barra lateral por secciones (en lugar de `type: book`). Es una decisión técnica deliberada: el formato `live-html` de `quarto-live` compone de forma fiable con `website`, garantizando que las celdas ejecutables en el navegador rendericen sin problemas. La experiencia de lectura (barra lateral con las tres partes, navegación entre páginas, búsqueda) es equivalente a la de un libro.

## Interactividad

- **Ejecución en navegador:** celdas `{pyodide}` (Python, primario) y `{webr}` (R, en pestañas).
- **Deslizadores y gráficos reactivos:** celdas `{ojs}` con Observable Plot.
- **Ejercicios plegables:** `callout` con solución colapsable.

## Estructura

- `index.qmd` — presentación
- Parte I: `p1-cap01..03.qmd` (sistemas 1-D, formas normales, potenciales/histéresis)
- Parte II: `p2-cap04.qmd` (bifurcaciones empíricas: Dai, Veraart, Carpenter, lagos)
- Parte III: `p3-cap05..07.qmd` (fundamento EWS, univariadas, multivariadas/ML)
- `taller.qmd` — taller transversal (simulado → real)
- `apA/apB/apC` y `referencias.qmd` — apéndices y bibliografía
- `references.bib`, `styles.css`, `_extensions/`

## Datos reales del taller (Fase B)

Por restricciones de CORS, los datos externos se descargan y analizan **localmente**:

- Termoacústicos + código: <https://github.com/ThomasMBury/deep-early-warnings-pnas>
- Geoquímicos (PANGAEA): <https://doi.pangaea.de/10.1594/PANGAEA.923197>
- Paleoclimáticos (NOAA): <http://www.ncdc.noaa.gov/paleo/data.html>

Herramientas locales sugeridas: `ewstools` (Python), `EWSmethods` (R).

## Licencia

Contenido bajo **CC BY-NC-SA 4.0**. La extensión `quarto-live` conserva su propia licencia (ver `_extensions/r-wasm/live/LICENSE.md`).
