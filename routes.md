# Rutas y menú de SABIA

Cómo se conectan las páginas del sitio, el asistente y el menú compartido (`almera/assets/nav.js`, diseño **1c** de Claude Design).

---

## 1. Un solo servidor, dos formas de servir

El sitio es **estático** (HTML/CSS/JS plano) y funciona con cualquier servidor de archivos. El asistente necesita el servidor de `rag/`, porque ahí vive la llave de OpenRouter. Por eso el servidor de `rag/` sirve **las dos cosas en la misma dirección**:

| Ruta | Qué sirve | De dónde sale |
|---|---|---|
| `/` y `/index.html` | Portada de SABIA | `index.html` (raíz del repo) |
| `/styles/…` | Estilos de la portada | `styles/` |
| `/almera/…` | Documentación de Almera, herramientas y `nav.js` | `almera/` |
| `/calidad-ai-agents/…` | Agentes de IA | `calidad-ai-agents/` |
| `/asistente/` | Chat "Pregúntale a SABIA" | `rag/static/index.html` |
| `/asistente/static/…` | CSS/JS del chat | `rag/static/` |
| `/api/modules`, `/api/chat` | API del chat | `rag/app/main.py` |
| `/api/descargas/plantilla`, `/api/descargas/prompt`, `/api/upload` | Botón "Aportar un documento" del chat | `rag/app/main.py` |

```powershell
npm start                    # todo SABIA en http://127.0.0.1:8800/
# o doble clic en iniciar.bat, o: cd rag; .\iniciar.ps1
```

**Modo solo estático** (`npx serve -l 8934 .`, GitHub Pages o abrir el HTML con doble clic): funciona todo **excepto** "Pregúntale a SABIA", que da 404 porque no hay servidor que responda `/asistente/`.

### Qué NO se publica

El servidor monta una **lista cerrada** (`SITE_DIRS` en `rag/app/main.py`), nunca la raíz del repo. Todo lo demás responde 404: `rag/.env` (la llave), `rag/app/`, `.git/`, `docs/`, `README.md`, `sabia.MD`, `.claude/`, y también los intentos de salir de una carpeta con `../` o `%2e%2e`.

> **Si agregas una carpeta de primer nivel al sitio** (por ejemplo `informes/`), súmala a `SITE_DIRS` o dará 404 desde el servidor.

---

## 2. Regla de oro: enlaces relativos, sin puertos

Ningún enlace del sitio ni del chat lleva `http://…:8800` ni otro puerto. Todo es relativo a la página actual:

| Desde | Hacia el chat | Hacia la portada |
|---|---|---|
| `index.html` | `./asistente/` | — |
| `almera/index.html` | `../asistente/` | `../index.html` |
| `rag/static/index.html` (servido en `/asistente/`) | — | `../index.html` |
| `nav.js` | `BASE + "asistente/"` | `BASE + "index.html"` |

Así el mismo código funciona en `127.0.0.1:8800`, en otro puerto o en el servidor del área, sin tocar nada. El único puerto que existe es el del propio servidor (`PORT` en `rag/.env`).

---

## 3. El menú (`almera/assets/nav.js`)

Un solo archivo compartido, sin dependencias ni build. Cada página lo incluye **al final del `<body>`**:

```html
<script src="../../assets/nav.js" data-base="../../../"></script>
```

- `src`: ruta relativa desde la página hasta `almera/assets/nav.js`.
- `data-base`: ruta relativa **desde la página hasta la raíz del repo**. Todos los enlaces del menú se arman como `data-base + ruta` (por ejemplo `../../../almera/index.html`).

| Página | `data-base` |
|---|---|
| `index.html` | `./` |
| `almera/index.html`, `calidad-ai-agents/index.html` | `../` |
| `almera/modulo-proyectos/`, `almera/almera-IA/`, `almera/codigos-estructura-organizacional/`, `calidad-ai-agents/entregables/` | `../../` |
| `almera/modulo-documentos/*/index.html`, `almera/modulo-evaluaciones/*/index.html` | `../../../` |
| Chat (`/asistente/`) | `../` |

**Excepciones a propósito:** `almera/informe-documentos/` y `almera/control-documentos-sgc/` **no** cargan el menú. Son herramientas autocontenidas que se distribuyen por separado (ver `docs/02-informes.md`).

### 3.1 Dónde se monta el botón

`nav.js` busca, en este orden:

1. **Un elemento `[data-sabnav]`**, si la página lo tiene. Es el caso de la portada, `almera/index.html` y el chat:
   ```html
   <div class="header-right">
     <span class="header-meta">SABIA</span>
     <span data-sabnav></span>          <!-- aquí entra el botón -->
   </div>
   ```
   La página tiene que centrar el header en vertical (`align-items:center`), porque el botón mide 44 px.
2. **El header de la página** (`header.m-header` o `header.site-header`), si no hay `[data-sabnav]`. `nav.js` agrupa el último elemento del header (el enlace "Todos los módulos" o la nav) con el botón dentro de un `.sabnav-right`, y centra el header. Así funcionan las 12 páginas de módulo y de agentes **sin editar su HTML**. En celular (≤ 640 px), ese enlace de texto se oculta porque el menú ya lo incluye.
3. **Fijo arriba a la derecha** (`.sabnav-fixed`, con fondo y sombra), si la página no tiene header.

### 3.2 El contenido del menú

Está en dos listas al inicio de `nav.js`:

```js
var HOME = [            // columna 01 · Inicio (letra grande)
  { label: 'SABIA', desc: 'Centro de recursos', href: 'index.html' },
  { label: 'Pregúntale a SABIA', desc: 'Asistente de Almera', href: 'asistente/' }
];
var GROUPS = [          // columnas 02–04 (listas con líneas finas)
  { num: '02', title: 'Almera · Documentación', wide: true, items: [ … ] },   // wide = 2 columnas
  { num: '03', title: 'Agentes de IA · Calidad', items: [ … ] },
  { num: '04', title: 'Herramientas · Informes', items: [ … ] }
];
```

Los `href` son **relativos a la raíz del repo**, sin `./` al inicio.

**La página actual** se detecta comparando la ruta del enlace con la de la página (tratando `x/index.html` y `x/` como iguales). Se marca con `aria-current="page"` y con el punto naranja en lugar de la flecha.

### 3.3 Cómo se arma el menú abierto (diseño 1c)

- **Cerrado:** círculo de 44 px, borde de 1 px `rgba(23,22,20,.16)` y dos líneas de 1 px.
- **Abierto:** capa `position:fixed` a pantalla completa, fondo `#17161a`, en 3 columnas (`1fr 2fr 1fr`). Pasa a 2 columnas por debajo de 980 px y a 1 por debajo de 640 px.
- **El header no se mueve al abrir:** la capa tiene su propio botón de cerrar, su eyebrow y la etiqueta "SABIA". Al abrir, `nav.js` **mide** dónde está el botón de la página y copia esa posición, y también copia el texto del eyebrow de la página. Por eso parece que solo cambia el fondo y las líneas giran a una X. Si el botón quedó fuera de pantalla por el scroll, usa la esquina superior derecha.
- **Mientras está abierto:** se bloquea el scroll de la página (`html.sabnav-lock`).
- **Teclado y lectores de pantalla:** `Escape` cierra. El foco pasa al botón de cerrar al abrir y vuelve al botón original al cerrar. Usa `role="dialog"`, `aria-modal` y `aria-expanded`.
- **Animaciones:** se desactivan si el sistema tiene activado "reducir movimiento".

> **Ojo con el atributo:** el `<style>` que inyecta `nav.js` se marca con `data-sabnav-style`, **no** con `data-sabnav`. Si llevara `data-sabnav`, `querySelector('[data-sabnav]')` lo encontraría primero y el botón terminaría dentro del `<style>`, invisible. Ya pasó una vez.

---

## 4. Agregar una página nueva

1. Crea la página y enlaza sus estilos con rutas relativas.
2. Al final del `<body>`, agrega `<script src="…/almera/assets/nav.js" data-base="…/"></script>` con las rutas de la tabla de la sección 3.
3. Si su header es `.m-header` o `.site-header`, no hay que hacer nada más: el botón se monta solo. Si quieres controlar dónde va, pon un `<span data-sabnav></span>` en el header y céntralo en vertical.
4. Agrégala a `GROUPS` (o `HOME`) en `nav.js` para que aparezca en el menú.
5. Si está en una carpeta de primer nivel nueva, súmala a `SITE_DIRS` en `rag/app/main.py`.
6. Pruébala en los dos modos: `npx serve -l 8934 .` y `rag\iniciar.ps1`.

---

## 5. Problemas comunes

| Síntoma | Causa probable |
|---|---|
| "Pregúntale a SABIA" da 404 | El sitio se está sirviendo sin el servidor de `rag/`. Usa `rag\iniciar.ps1`. |
| Una página nueva da 404 solo con el servidor de `rag/` | Su carpeta de primer nivel no está en `SITE_DIRS`. |
| El menú no aparece en una página | Falta el `<script>` de `nav.js` o el `src` relativo está mal (revisa la consola del navegador). |
| Los enlaces del menú llevan a rutas rotas | El `data-base` no corresponde a la profundidad de la página. |
| La página actual no se marca en el menú | El `href` en `nav.js` no coincide con la ruta real de la página. |
| El botón se encima con otros elementos del header | El header no está centrado en vertical, o tiene demasiados elementos para el ancho del celular. |
| Con `npx serve`, `almera/index.html` carga sin estilos | `serve` redirige `/almera/index.html` a `/almera` sin barra final, y eso rompe las rutas relativas. Entra por `/almera/`. |
