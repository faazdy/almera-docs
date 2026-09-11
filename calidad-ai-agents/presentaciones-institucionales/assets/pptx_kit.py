# -*- coding: utf-8 -*-
"""
pptx_kit - utilidades para generar presentaciones institucionales en PPTX
partiendo de `assets/plantilla.pptx`.

Reglas de la plantilla (detalle en `references/05-mapa-de-layouts.md`):

- La base SIEMPRE es `plantilla.pptx` (tema "Capital 2025 octubre" + fuente
  Arial). No se crea un `Presentation()` vacio y no se usa `referencia.pptx`
  (tema Office generico).
- Los placeholders de `plantilla.pptx` tienen todos `idx=0` y son inservibles
  para posicionar: al instanciar una diapositiva se apilan en la misma
  coordenada. Por eso el contenido se COMPONE con formas colocadas por
  coordenadas. Cada layout solo aporta el "mobiliario": fondo claro
  institucional, franja de sellos inferior, logo, chip de numero de pagina y
  el texto vertical "Vigilado Supersalud".
- Zona de contenido util:  x  2.2 -> 31.7 cm   |   y  3.8 -> 14.2 cm
  (los ~4.2 cm inferiores los ocupa la franja de sellos del layout).
- Titulos en Arial Bold. Si la maquina tiene "Roboto Slab" instalada, cambiar
  F_TIT abajo a "Roboto Slab" (es la fuente de titulos de la presentacion de
  referencia; PowerPoint la sustituye por Arial si no esta).

Uso tipico:

    from pptx_kit import (Deck, kpi_tiles, vinetas, tarjetas, tabla,
                          grafica_barras, grafica_dona, barras_horizontales,
                          kpi_gigante, fuente,
                          barra_apilada, etapas, imagen, cita)
    # Deck.texto_pleno(...) para diapositivas de solo texto (L12-L14)

    d = Deck()                                   # abre plantilla.pptx (adelgazada)
    d.portada("Informe de gestion", "Gestion Integral",
              "Segundo trimestre de 2026",
              meta=["Talento Humano", "1 de septiembre de 2026 - Comite Directivo"],
              figura="trio-computador")          # personaje de marca/personajes/
    d.separador("01", "Talento humano y teletrabajo", figura="hombre-checklist")

    s = d.contenido("El teletrabajo ya es politica permanente",
                    "Estado del programa - primer semestre de 2026")
    vinetas(s, ["320 servidores vinculados", "Cobertura en las 4 direcciones"])

    s = d.contenido("Solicitudes concentradas en marzo")
    grafica_barras(s, ["Ene","Feb","Mar","Abr"], [("Solicitudes",(18,26,44,39))],
                   highlight=2)
    fuente(s, "Fuente: Talento Humano. Datos ficticios.")

    d.guardar("gestion-integral.pptx")
"""
import os
from pptx import Presentation
from pptx.util import Cm, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.oxml.ns import qn

# --------------------------------------------------------------------------- #
#  Paleta (assets/paleta.md) y tipografias
# --------------------------------------------------------------------------- #
PRIMARIO   = RGBColor(0x00, 0x4C, 0x97)   # titulos, barras de seccion, encabezado de tabla
AZUL_ENCAB = RGBColor(0x00, 0x39, 0x71)   # topbar, subtitulos, cifras KPI
ACENTO     = RGBColor(0x00, 0x85, 0xCF)   # UN dato resaltado por diapositiva
TEXTO      = RGBColor(0x00, 0x00, 0x00)
FONDO_INST = RGBColor(0xD6, 0xF0, 0xF5)   # bandas / tarjetas "despues"
BLANCO     = RGBColor(0xFF, 0xFF, 0xFF)
GRIS_BORDE = RGBColor(0xCD, 0xDA, 0xE6)
GRIS_TX    = RGBColor(0x5B, 0x6B, 0x7A)
CLARO      = RGBColor(0xF8, 0xF8, 0xF8)
TOPBAR_DARK = RGBColor(0x2A, 0x3B, 0x52)  # topbar de anexos
AZUL_CLARO_TX = RGBColor(0xCF, 0xE0, 0xF2)

# colores de grafica, en orden (assets/paleta.md)
G = [RGBColor(0x00, 0x4C, 0x97), RGBColor(0x00, 0x85, 0xCF), RGBColor(0x5A, 0xB5, 0xE6),
     RGBColor(0x33, 0xB4, 0xCF), RGBColor(0xB9, 0xE5, 0xE5), RGBColor(0x9D, 0xCD, 0xEA)]

# rampa azul decreciente para barra apilada 100% y barra de avance (L06, L08)
RAMP = [G[0], G[1], G[2], G[3], G[5]]

F_TIT = "Arial"   # titulos  (poner "Roboto Slab" si esta instalada)
F_TXT = "Arial"   # cuerpo

# --------------------------------------------------------------------------- #
#  Geometria (diapositiva 33.87 x 19.05 cm, 16:9)
# --------------------------------------------------------------------------- #
W        = 33.87
H        = 19.05
MX       = 2.2                       # margen izq/der
TOP_Y    = 0.75                      # y del topbar
TOPBAR_H = 2.5
CANVAS_Y = TOP_Y + TOPBAR_H + 0.55   # ~3.80 : donde empieza el contenido
CANVAS_BOTTOM = 14.2                 # la franja de sellos empieza en ~14.83
CANVAS_H = CANVAS_BOTTOM - CANVAS_Y  # ~10.4
CONTENT_W = W - 2 * MX              # ~29.5

# layouts de plantilla.pptx que usa la skill (ver 05-mapa-de-layouts.md).
# La plantilla viene "adelgazada": solo estos 6 layouts, sin las diapositivas de
# ejemplo y SIN los renders de personaje (esos se colocan en generacion desde
# assets/marca/personajes/).
LAYOUT_PORTADA   = "Portada"
LAYOUT_CONTENIDO = "Contenido Tabla 4"   # fondo claro + sellos + logo, zona superior limpia
SEPARADORES = ["Separador1", "Separador2", "1_Separador1", "2_Separador1"]

# personajes disponibles en assets/marca/personajes/ (sin extension)
PERSONAJES = ["trio-computador", "hombre-checklist", "mujer-checklist",
              "trio-sello", "duo-laptop-ok"]
# rotacion por defecto para separadores sin `figura=` explicita
_SEP_FIGURAS = ["hombre-checklist", "mujer-checklist", "trio-sello", "trio-computador"]

_ASSETS_DIR = os.path.dirname(os.path.abspath(__file__))
_PLANTILLA  = os.path.join(_ASSETS_DIR, "plantilla.pptx")
_MARCA      = os.path.join(_ASSETS_DIR, "marca")


def _add_personaje(slide, nombre, portada=False):
    """Coloca un render de personaje de marca/personajes/ a la izquierda de la
    diapositiva (portadas y separadores). `nombre` sin extension; None = nada."""
    if not nombre:
        return
    path = os.path.join(_MARCA, "personajes", nombre + ".png")
    if not os.path.exists(path):
        return
    if portada:
        left, alto, base = 2.6, 14.0, 15.3     # base = borde inferior de la figura
    else:
        left, alto, base = 2.8, 12.8, 14.4     # mas chico: los trios no invaden el texto
    slide.shapes.add_picture(path, Cm(left), Cm(base - alto), height=Cm(alto))


# --------------------------------------------------------------------------- #
#  Primitivas de bajo nivel  (normalmente no se llaman directo)
# --------------------------------------------------------------------------- #
def _set_runs(tf, lines, align=PP_ALIGN.LEFT):
    """lines: lista de parrafos. Cada parrafo es una lista de runs
    `(texto, size_pt, bold, color, font)` o un unico run como tupla."""
    for i, para in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        runs = [para] if isinstance(para, tuple) else para
        for (text, size, bold, color, font) in runs:
            r = p.add_run()
            r.text = text
            r.font.size = Pt(size)
            r.font.bold = bold
            r.font.name = font
            r.font.color.rgb = color


def textbox(slide, x, y, w, h, lines, align=PP_ALIGN.LEFT,
            anchor=MSO_ANCHOR.TOP, wrap=True, line_spacing=None):
    """Caja de texto por coordenadas (cm). `lines` con el formato de _set_runs."""
    tb = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Cm(0)
    tf.margin_top = tf.margin_bottom = Cm(0)
    _set_runs(tf, lines, align)
    if line_spacing:
        for p in tf.paragraphs:
            p.line_spacing = line_spacing
    return tb


def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0, rounded=False):
    """Rectangulo (o rectangulo redondeado) por coordenadas (cm)."""
    shp = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE,
        Cm(x), Cm(y), Cm(w), Cm(h))
    if rounded:
        try:
            shp.adjustments[0] = 0.06
        except Exception:
            pass
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = fill
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_w)
    shp.shadow.inherit = False
    return shp


def _clip_shape(pic, prst="roundRect"):
    """Recorta una imagen a una forma (`roundRect` o `ellipse`) insertando un
    prstGeom en su spPr, justo despues de xfrm para respetar el orden del schema."""
    spPr = pic._element.spPr
    for tag in ("a:prstGeom", "a:custGeom"):
        e = spPr.find(qn(tag))
        if e is not None:
            spPr.remove(e)
    g = spPr.makeelement(qn("a:prstGeom"), {"prst": prst})
    g.append(spPr.makeelement(qn("a:avLst"), {}))
    xfrm = spPr.find(qn("a:xfrm"))
    if xfrm is not None:
        xfrm.addnext(g)
    else:
        spPr.insert(0, g)
    return pic


def _numeral(slide, x, y, d, texto, fill=FONDO_INST, fg=AZUL_ENCAB, size=13):
    """Circulo con un numero (etapas L08, vinetas numeradas L13)."""
    c = slide.shapes.add_shape(MSO_SHAPE.OVAL, Cm(x), Cm(y), Cm(d), Cm(d))
    c.fill.solid()
    c.fill.fore_color.rgb = fill
    c.line.fill.background()
    c.shadow.inherit = False
    tf = c.text_frame
    tf.word_wrap = False
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = Cm(0)
    tf.margin_top = tf.margin_bottom = Cm(0)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = str(texto)
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.name = F_TIT
    r.font.color.rgb = fg
    return c


# --------------------------------------------------------------------------- #
#  Deck
# --------------------------------------------------------------------------- #
class Deck:
    """Abre `plantilla.pptx`, borra sus diapositivas de ejemplo y ofrece
    fabricas de diapositiva. `contenido()` devuelve la diapositiva cruda de
    python-pptx para seguir componiendo con los helpers del modulo."""

    def __init__(self, plantilla=None):
        self.prs = Presentation(plantilla or _PLANTILLA)
        self._delete_all_slides()
        self._layouts = {l.name: l for l in self.prs.slide_masters[0].slide_layouts}
        self._sep_i = 0

    # -- infra --------------------------------------------------------------
    def _delete_all_slides(self):
        lst = self.prs.slides._sldIdLst
        for sid in list(lst):
            self.prs.part.drop_rel(sid.get(qn("r:id")))
            lst.remove(sid)

    def _new(self, layout_name):
        slide = self.prs.slides.add_slide(self._layouts[layout_name])
        # quitar placeholders heredados (vacios y mal posicionados por idx=0)
        for ph in list(slide.placeholders):
            ph._element.getparent().remove(ph._element)
        return slide

    def guardar(self, path):
        self.prs.save(path)
        return path

    # -- fabricas de diapositiva -----------------------------------------
    def portada(self, kicker, titulo, subtitulo, meta=(), figura="trio-computador"):
        s = self._new(LAYOUT_PORTADA)
        _add_personaje(s, figura, portada=True)
        lines = [[(kicker.upper(), 12, True, G[4], F_TXT)],
                 [(titulo, 40, True, CLARO, F_TIT)],
                 [(subtitulo, 18, True, CLARO, F_TXT)]]
        for m in meta:
            lines.append([(m, 12, False, AZUL_CLARO_TX, F_TXT)])
        textbox(s, 17.0, 4.6, 14.5, 9.0, lines,
                align=PP_ALIGN.RIGHT, line_spacing=1.15)
        return s

    def separador(self, num, titulo, figura=None, layout=None):
        i = self._sep_i
        self._sep_i += 1
        if layout is None:
            layout = SEPARADORES[i % len(SEPARADORES)]
        if figura is None:
            figura = _SEP_FIGURAS[i % len(_SEP_FIGURAS)]
        s = self._new(layout)
        _add_personaje(s, figura, portada=False)
        x0, w = 16.8, 14.9           # mitad derecha, libre de la figura
        textbox(s, x0, 4.6, w, 1.0,
                [[(num, 18, True, AZUL_CLARO_TX, F_TIT)]], align=PP_ALIGN.RIGHT)
        textbox(s, x0, 5.7, w, 3.9,
                [[(titulo.upper(), 26, True, BLANCO, F_TIT)]],
                align=PP_ALIGN.RIGHT, line_spacing=1.08)
        rect(s, x0 + w - 10.5, 10.1, 10.5, 0.12, fill=RGBColor(0xBF, 0xD9, 0xEC))
        return s
        return s

    def contenido(self, titulo, sub=None, dark=False):
        """Diapositiva de contenido: agrega el topbar azul y devuelve la
        diapositiva para componerle el cuerpo con los helpers del modulo."""
        s = self._new(LAYOUT_CONTENIDO)
        bg = TOPBAR_DARK if dark else AZUL_ENCAB
        h = TOPBAR_H + (0.35 if sub else 0)
        box = rect(s, MX, TOP_Y, CONTENT_W - 3.0, h, fill=bg, rounded=True)
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Cm(0.7)
        tf.margin_top = tf.margin_bottom = Cm(0.2)
        lines = [[(titulo, 17, True, BLANCO, F_TIT)]]
        if sub:
            lines.append([(sub, 10.5, False, AZUL_CLARO_TX, F_TXT)])
        _set_runs(tf, lines)
        return s

    def texto_pleno(self, titulo, encabezado=None, cuerpo=(), figura=None,
                    numerada=False, mensaje=None, apoyos=()):
        """Diapositiva de SOLO texto con personaje institucional
        (L12 `plain-text`, L13 `plain-bullets`, L14 `plain-statement`).

        - `cuerpo`: hasta 5 lineas / puntos.
        - `numerada=True`  -> cada punto con numeral (L13).
        - `mensaje` (+ `apoyos`) -> mensaje central + viñetas de apoyo (L14).
        - `figura`: personaje de `marca/personajes/` (sin extension); None rota.

        Desde "Layouts Gerenciales v2": L12-L14 usan **el mismo marco estandar**
        que el resto (topbar redondeado dentro del margen + logo). No hay banda a
        sangre. Lo unico propio es la zona de contenido: tarjeta de texto +
        personaje al 34 %."""
        s = self._new(LAYOUT_CONTENIDO)
        if figura is None:
            figura = _SEP_FIGURAS[self._sep_i % len(_SEP_FIGURAS)]
            self._sep_i += 1
        _add_personaje(s, figura, portada=False)

        box = rect(s, MX, TOP_Y, CONTENT_W - 3.0, TOPBAR_H, fill=AZUL_ENCAB,
                   rounded=True)
        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Cm(0.7)
        tf.margin_top = tf.margin_bottom = Cm(0.2)
        _set_runs(tf, [[(str(titulo), 17, True, BLANCO, F_TIT)]])

        cx = 16.8                     # misma referencia que Deck.separador
        cw = W - cx - MX
        cy = CANVAS_Y + 0.2
        chh = CANVAS_H - 0.6
        card = rect(s, cx, cy, cw, chh, fill=BLANCO, line=GRIS_BORDE, rounded=True)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE if mensaje else MSO_ANCHOR.TOP
        tf.margin_left = tf.margin_right = Cm(0.7)
        tf.margin_top = tf.margin_bottom = Cm(0.6)
        lines = []
        if encabezado:
            lines.append([(str(encabezado).upper(), 15, True, PRIMARIO, F_TIT)])
        if mensaje:
            lines.append([(str(mensaje), 15, False, TEXTO, F_TIT)])
            for a in apoyos:
                lines.append([("•  ", 11, False, ACENTO, F_TXT),
                              (str(a), 11, False, TEXTO, F_TXT)])
        elif numerada:
            for i, pt in enumerate(cuerpo, 1):
                lines.append([("%d.  " % i, 13, True, ACENTO, F_TIT),
                              (str(pt), 13, False, TEXTO, F_TXT)])
        else:
            for ln in cuerpo:
                lines.append([(str(ln), 13, False, TEXTO, F_TXT)])
        _set_runs(tf, lines)
        for p in tf.paragraphs:
            p.space_before = Pt(6)
            p.line_spacing = 1.18
        return s


# --------------------------------------------------------------------------- #
#  Helpers de cuerpo  (operan sobre una diapositiva de `Deck.contenido`)
# --------------------------------------------------------------------------- #
def fuente(slide, txt):
    """Linea de fuente / nota al pie, al borde inferior de la zona util."""
    textbox(slide, MX, 13.95, CONTENT_W, 0.7,
            [[(txt, 8.5, False, PRIMARIO, F_TXT)]])


def vinetas(slide, items, size=18, y=None, h=None):
    """Lista de vinetas simples."""
    y = CANVAS_Y + 0.6 if y is None else y
    h = CANVAS_H - 1.0 if h is None else h
    textbox(slide, MX + 0.3, y, CONTENT_W - 0.6, h,
            [[("•  ", size, False, PRIMARIO, F_TXT), (it, size, False, TEXTO, F_TXT)]
             for it in items],
            line_spacing=1.15)


def kpi_tiles(slide, data, y=None, h=3.6):
    """Fila de fichas KPI. `data`: lista de tuplas
    `(rotulo, cifra, delta|None, pie|None, alerta_bool)` (2 a 4 fichas)."""
    y = CANVAS_Y + 0.3 if y is None else y
    n = len(data)
    gap = 0.6
    tw = (CONTENT_W - (n - 1) * gap) / n
    for i, item in enumerate(data):
        lbl, num = item[0], item[1]
        delta = item[2] if len(item) > 2 else None
        foot = item[3] if len(item) > 3 else None
        alert = item[4] if len(item) > 4 else False
        card = rect(slide, MX + i * (tw + gap), y, tw, h,
                    fill=BLANCO, line=GRIS_BORDE, rounded=True)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = tf.margin_right = Cm(0.35)
        tf.margin_top = tf.margin_bottom = Cm(0.3)
        lines = [[(str(lbl).upper(), 8, True, PRIMARIO, F_TXT)],
                 [(str(num), 22, True, AZUL_ENCAB, F_TIT)]]
        if delta:
            lines.append([(delta, 9, True, ACENTO if alert else PRIMARIO, F_TXT)])
        if foot:
            lines.append([(foot, 7.5, False, GRIS_TX, F_TXT)])
        _set_runs(tf, lines)


def _card_lista(slide, x, y, w, h, titulo, items, fill=BLANCO):
    c = rect(slide, x, y, w, h, fill=fill,
             line=GRIS_BORDE if fill == BLANCO else None, rounded=True)
    tf = c.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = Cm(0.6)
    tf.margin_top = tf.margin_bottom = Cm(0.55)
    lines = []
    if titulo:
        lines.append([(titulo, 13, True, AZUL_ENCAB, F_TIT)])
    for it in items:
        lines.append([("-  ", 11, False, ACENTO, F_TXT), (it, 11, False, TEXTO, F_TXT)])
    _set_runs(tf, lines)
    for p in tf.paragraphs[(1 if titulo else 0):]:
        p.space_before = Pt(7)
        p.line_spacing = 1.15
    return c


def tarjetas(slide, cols, y=None, h=None):
    """1..3 tarjetas en fila. `cols`: lista de `(titulo, [items], fondo)`
    donde fondo es 'blanco' o 'inst'."""
    y = CANVAS_Y if y is None else y
    h = CANVAS_H - 3.0 if h is None else h
    n = len(cols)
    gap = 1.2
    cw = (CONTENT_W - (n - 1) * gap) / n
    for i, (titulo, items, fondo) in enumerate(cols):
        fill = FONDO_INST if fondo == "inst" else BLANCO
        _card_lista(slide, MX + i * (cw + gap), y, cw, h, titulo, items, fill=fill)


def caja_texto(slide, titulo, items, y=None, h=None):
    """Una sola tarjeta ancha (p. ej. anexo de supuestos)."""
    y = CANVAS_Y if y is None else y
    h = CANVAS_H - 0.4 if h is None else h
    _card_lista(slide, MX, y, CONTENT_W, h, titulo, items)


def kpi_gigante(slide, numero, caption):
    """Una cifra grande en color de acento + una linea que la explica."""
    textbox(slide, MX + 1.0, CANVAS_Y + 1.2, 12, 4.5,
            [[(str(numero), 72, True, ACENTO, F_TIT)]], anchor=MSO_ANCHOR.MIDDLE)
    textbox(slide, MX + 1.0, CANVAS_Y + 5.8, CONTENT_W - 8, 3.0,
            [[(caption, 16, False, TEXTO, F_TXT)]], line_spacing=1.25)


def tabla(slide, headers, rows, total_rows=(), y=None, h=8.6):
    """Tabla nativa con el estilo de la plantilla (encabezado azul, filas
    alternas, filas de total en fondo institucional). `total_rows`: indices
    (base 0) de filas de `rows` a resaltar como total."""
    y = CANVAS_Y if y is None else y
    nr, nc = len(rows) + 1, len(headers)
    gf = slide.shapes.add_table(nr, nc, Cm(MX), Cm(y), Cm(CONTENT_W), Cm(h))
    t = gf.table
    t.first_row = True
    t.horz_banding = False
    for j, htxt in enumerate(headers):
        cell = t.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = PRIMARIO
        cell.margin_left = cell.margin_right = Cm(0.25)
        p = cell.text_frame.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.RIGHT
        r = p.add_run()
        r.text = str(htxt)
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.name = F_TXT
        r.font.color.rgb = BLANCO
    for i, row in enumerate(rows, start=1):
        is_total = (i - 1) in total_rows
        for j, val in enumerate(row):
            cell = t.cell(i, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = (FONDO_INST if is_total
                                        else BLANCO if i % 2
                                        else RGBColor(0xFB, 0xFD, 0xFE))
            cell.margin_left = cell.margin_right = Cm(0.25)
            cell.margin_top = cell.margin_bottom = Cm(0.1)
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.RIGHT
            r = p.add_run()
            r.text = str(val)
            r.font.size = Pt(11)
            r.font.bold = is_total
            r.font.name = F_TXT
            r.font.color.rgb = TEXTO
    return t


def _style_chart(chart, colors, legend=False, data_labels=True):
    chart.has_title = False
    if legend:
        chart.has_legend = True
        chart.legend.position = XL_LEGEND_POSITION.BOTTOM
        chart.legend.include_in_layout = False
        chart.legend.font.size = Pt(9)
        chart.legend.font.name = F_TXT
    else:
        chart.has_legend = False
    for plot in chart.plots:
        plot.has_data_labels = data_labels
        if data_labels:
            plot.data_labels.font.size = Pt(9)
            plot.data_labels.font.name = F_TXT
            plot.data_labels.font.bold = True
            plot.data_labels.font.color.rgb = PRIMARIO
        for s_idx, series in enumerate(plot.series):
            series.format.fill.solid()
            series.format.fill.fore_color.rgb = colors[s_idx % len(colors)]
            series.format.line.fill.background()
    try:
        chart.value_axis.visible = False
        chart.value_axis.has_major_gridlines = False
    except Exception:
        pass
    for ax in (getattr(chart, "category_axis", None),):
        if ax is not None:
            try:
                ax.tick_labels.font.size = Pt(9)
                ax.tick_labels.font.name = F_TXT
            except Exception:
                pass


def grafica_barras(slide, cats, series, colors=None, horizontal=False,
                   legend=False, highlight=None, y=None, h=None):
    """Grafica de barras nativa.
    - `series`: lista de `(nombre, (v1, v2, ...))`.
    - serie unica + `highlight=i`: resalta la barra i en color de acento y el
      resto en gris azulado.
    - varias series: pasa `legend=True`; usa colores de paleta por serie."""
    y = CANVAS_Y + 0.1 if y is None else y
    h = CANVAS_H - 1.2 if h is None else h
    if colors is None:
        colors = [PRIMARIO] if len(series) == 1 else G
    cd = CategoryChartData()
    cd.categories = cats
    for name, vals in series:
        cd.add_series(name, vals)
    ctype = XL_CHART_TYPE.BAR_CLUSTERED if horizontal else XL_CHART_TYPE.COLUMN_CLUSTERED
    chart = slide.shapes.add_chart(ctype, Cm(MX), Cm(y), Cm(CONTENT_W), Cm(h), cd).chart
    _style_chart(chart, colors, legend=legend)
    if highlight is not None and len(series) == 1:
        for i, pt in enumerate(chart.plots[0].series[0].points):
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = ACENTO if i == highlight else G[4]
    try:
        chart.plots[0].gap_width = 60 if len(series) == 1 else 90
    except Exception:
        pass
    return chart


def grafica_dona(slide, pares, colors=None, centro=None, y=None, h=None):
    """Dona nativa. `pares`: lista de `(categoria, valor)`. Los porcentajes van
    en la leyenda (no como etiquetas sobre la dona, que se amontonan en las
    porciones chicas). `centro=(cifra, rotulo)` dibuja un texto en el agujero."""
    y = CANVAS_Y if y is None else y
    h = CANVAS_H - 1.0 if h is None else h
    if colors is None:
        colors = [G[0], G[1], G[3], G[5], G[2], G[4]]
    cd = CategoryChartData()
    cd.categories = ["%s  -  %s %%" % (c, ("%.1f" % v).replace(".", ",")) for c, v in pares]
    cd.add_series("comp", [v for _, v in pares])
    chart = slide.shapes.add_chart(
        XL_CHART_TYPE.DOUGHNUT, Cm(MX), Cm(y), Cm(CONTENT_W), Cm(h), cd).chart
    chart.has_title = False
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.RIGHT
    chart.legend.include_in_layout = False
    chart.legend.font.size = Pt(11)
    chart.legend.font.name = F_TXT
    plot = chart.plots[0]
    plot.has_data_labels = False
    for i, pt in enumerate(plot.series[0].points):
        pt.format.fill.solid()
        pt.format.fill.fore_color.rgb = colors[i % len(colors)]
    if centro:
        legend_zone = 9.5
        cxc = MX + (CONTENT_W - legend_zone) / 2
        cyc = y + h / 2
        bw = 5.0
        textbox(slide, cxc - bw / 2, cyc - 1.1, bw, 2.2,
                [[(centro[0], 20, True, AZUL_ENCAB, F_TIT)],
                 [(centro[1], 10, False, GRIS_TX, F_TXT)]],
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return chart


def barras_horizontales(slide, rows, accent_last=True, y=None, h=None):
    """Barras horizontales dibujadas a mano (pista + relleno + rotulo + %).
    `rows`: lista de `(rotulo, porcentaje)`. Con `accent_last` la ultima fila
    va en color de acento."""
    y = CANVAS_Y + 0.4 if y is None else y
    h = CANVAS_H - 1.2 if h is None else h
    x = MX + 0.3
    w = CONTENT_W - 0.6
    n = len(rows)
    row_h = h / n
    lab_w, pct_w = 5.2, 2.0
    track_x = x + lab_w
    track_w = w - lab_w - pct_w
    bar_h = min(0.95, row_h * 0.5)
    for i, (label, pct) in enumerate(rows):
        cy = y + i * row_h
        mid = cy + (row_h - bar_h) / 2
        is_acc = accent_last and i == n - 1
        textbox(slide, x, cy, lab_w - 0.2, row_h,
                [[(label, 12, False, TEXTO, F_TXT)]], anchor=MSO_ANCHOR.MIDDLE)
        rect(slide, track_x, mid, track_w, bar_h,
             fill=RGBColor(0xD7, 0xE4, 0xEF), rounded=True)
        rect(slide, track_x, mid, max(0.15, track_w * pct / 100.0), bar_h,
             fill=ACENTO if is_acc else PRIMARIO, rounded=True)
        textbox(slide, track_x + track_w + 0.15, cy, pct_w, row_h,
                [[("%g %%" % pct, 12, True, PRIMARIO, F_TXT)]],
                align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)


def _pct(v):
    """Formatea un porcentaje: sin decimal si es entero, con uno si no."""
    return ("%g" % round(v, 1)).replace(".", ",")


def barra_apilada(slide, segmentos, total=None, y=None, h=None):
    """Distribucion del 100% en una barra apilada (L06 `share-100`).
    Preferida sobre la dona para partes de un total conocido.

    `segmentos`: lista de 2 a 4 tuplas `(nombre, pct, valor|None, nota|None)`.
    `total`: `(label, valor)` opcional; se rotula arriba a la derecha.
    Debajo, una tarjeta por segmento con borde superior de su color."""
    y = CANVAS_Y + 1.0 if y is None else y
    h = CANVAS_H - 1.6 if h is None else h
    x = MX
    w = CONTENT_W
    bar_h = 1.8
    gap = 0.12
    tot_pct = sum(s[1] for s in segmentos) or 100.0

    if total:
        textbox(slide, x, y - 0.95, w, 0.85,
                [[(str(total[0]).upper() + "   ", 9, True, GRIS_TX, F_TXT),
                  (str(total[1]), 13, True, AZUL_ENCAB, F_TIT)]],
                align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)

    inner_w = w - (len(segmentos) - 1) * gap
    cxp = x
    for i, seg in enumerate(segmentos):
        pct = seg[1]
        sw = max(0.3, inner_w * pct / tot_pct)
        rect(slide, cxp, y, sw, bar_h, fill=RAMP[i % len(RAMP)], rounded=True)
        if pct >= 10:
            textbox(slide, cxp, y, sw, bar_h,
                    [[(_pct(pct) + " %", 11, True, BLANCO, F_TXT)]],
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        cxp += sw + gap

    cy = y + bar_h + 0.9
    ch = min(4.8, (y + h) - cy)
    n = len(segmentos)
    cgap = 0.6
    cw = (w - (n - 1) * cgap) / n
    for i, seg in enumerate(segmentos):
        nombre, pct = seg[0], seg[1]
        valor = seg[2] if len(seg) > 2 else None
        nota = seg[3] if len(seg) > 3 else None
        bx = x + i * (cw + cgap)
        rect(slide, bx, cy, cw, 0.16, fill=RAMP[i % len(RAMP)])
        card = rect(slide, bx, cy + 0.16, cw, ch - 0.16,
                    fill=BLANCO, line=GRIS_BORDE, rounded=True)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = tf.margin_right = Cm(0.35)
        tf.margin_top = tf.margin_bottom = Cm(0.3)
        lines = [[(str(nombre).upper(), 8, True, PRIMARIO, F_TXT)],
                 [(_pct(pct) + " %", 18, True, AZUL_ENCAB, F_TIT)]]
        if valor:
            lines.append([(str(valor), 10, True, GRIS_TX, F_TXT)])
        if nota:
            lines.append([(str(nota), 8, False, GRIS_TX, F_TXT)])
        _set_runs(tf, lines)


def etapas(slide, pasos, hito=None, y=None, h=None):
    """Proceso por etapas con avance y responsable (L08 `stages`).

    `pasos`: lista de 2 a 5 tuplas
    `(fecha, nombre, desc|"", responsable|"", cumplida_bool)`.
    Barra de avance segmentada arriba (un tramo por etapa); las pendientes van
    atenuadas. `hito`: texto de hito critico, en franja azul al pie."""
    y = CANVAS_Y + 0.2 if y is None else y
    h = CANVAS_H - 1.0 if h is None else h
    x = MX
    w = CONTENT_W
    n = len(pasos)

    seg_gap = 0.15
    seg_w = (w - (n - 1) * seg_gap) / n
    for i, p in enumerate(pasos):
        done = p[4] if len(p) > 4 else False
        rect(slide, x + i * (seg_w + seg_gap), y, seg_w, 0.5,
             fill=ACENTO if done else GRIS_BORDE, rounded=True)

    cy = y + 1.15
    reserve = 1.5 if hito else 0.0
    ch = (y + h) - cy - reserve
    cgap = 0.55
    cw = (w - (n - 1) * cgap) / n
    for i, p in enumerate(pasos):
        fecha, nombre = p[0], p[1]
        desc = p[2] if len(p) > 2 else ""
        resp = p[3] if len(p) > 3 else ""
        done = p[4] if len(p) > 4 else False
        bx = x + i * (cw + cgap)
        card = rect(slide, bx, cy, cw, ch,
                    fill=BLANCO if done else CLARO, line=GRIS_BORDE, rounded=True)
        tf = card.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_left = tf.margin_right = Cm(0.4)
        tf.margin_top = Cm(0.95)
        tf.margin_bottom = Cm(0.3)
        tint = TEXTO if done else GRIS_TX
        lines = [[(str(fecha).upper(), 8, True, PRIMARIO if done else GRIS_TX, F_TXT)],
                 [(str(nombre), 12, True, AZUL_ENCAB if done else GRIS_TX, F_TIT)]]
        if desc:
            lines.append([(str(desc), 9, False, tint, F_TXT)])
        _set_runs(tf, lines)
        for pp in tf.paragraphs[1:]:
            pp.space_before = Pt(4)
            pp.line_spacing = 1.12
        _numeral(slide, bx + 0.4, cy - 0.45, 0.9, "%02d" % (i + 1),
                 fill=ACENTO if done else GRIS_BORDE,
                 fg=BLANCO if done else GRIS_TX, size=11)
        if resp:
            textbox(slide, bx + 0.4, cy + ch - 1.15, cw - 0.8, 1.0,
                    [[("RESPONSABLE", 6.5, True, GRIS_TX, F_TXT)],
                     [(str(resp), 9, True, tint, F_TXT)]], line_spacing=1.1)

    if hito:
        hy = y + h - 1.15
        bar = rect(slide, x, hy, w, 1.15, fill=AZUL_ENCAB, rounded=True)
        tf = bar.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = Cm(0.6)
        tf.margin_top = tf.margin_bottom = Cm(0.1)
        _set_runs(tf, [[("HITO CRITICO    ", 8, True, AZUL_CLARO_TX, F_TXT),
                        (str(hito), 11, True, BLANCO, F_TXT)]])


def imagen(slide, ruta=None, x=None, y=None, w=None, h=None, credito=None):
    """Imagen de CONTENIDO (no personaje) para L10 `text-image`.

    Por defecto ocupa la columna derecha (~38% de la zona util). Si `ruta` no
    existe, dibuja un marcador punteado con la leyenda [imagen]. `credito` va
    como nota al pie de la imagen (toda imagen lleva credito)."""
    if w is None:
        w = CONTENT_W * 0.38
    if x is None:
        x = MX + CONTENT_W - w
    y = CANVAS_Y + 0.2 if y is None else y
    if h is None:
        h = min(CANVAS_H - 1.6, w * 3.0 / 4.0)

    if ruta and os.path.exists(ruta):
        pic = slide.shapes.add_picture(ruta, Cm(x), Cm(y), Cm(w), Cm(h))
        _clip_shape(pic, "roundRect")
    else:
        ph = rect(slide, x, y, w, h, fill=RGBColor(0xEE, 0xF4, 0xFA),
                  line=RGBColor(0xB9, 0xCF, 0xE3), line_w=1.0, rounded=True)
        try:
            from pptx.enum.line import MSO_LINE_DASH_STYLE
            ph.line.dash_style = MSO_LINE_DASH_STYLE.DASH
        except Exception:
            pass
        textbox(slide, x, y, w, h,
                [[("[ imagen ]", 10, True, GRIS_TX, F_TXT)]],
                align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if credito:
        textbox(slide, x, y + h + 0.12, w, 0.6,
                [[(str(credito), 7.5, False, GRIS_TX, F_TXT)]],
                align=PP_ALIGN.RIGHT)
    return (x, y, w, h)


def cita(slide, mensaje, nombre, cargo, avatar=None, chips=(), y=None, h=None):
    """Mensaje con voceria identificable (L11 `quote-avatar`).

    Avatar circular a la izquierda con nombre y cargo debajo; el mensaje grande
    (sin cifras nuevas) a la derecha; hasta 2 `chips` `(label, valor)`.
    Si `avatar` no existe, se dibuja un circulo con las iniciales."""
    y = CANVAS_Y + 0.5 if y is None else y
    h = CANVAS_H - 1.4 if h is None else h
    x = MX
    av_d = 4.6
    av_x = x + 0.6
    av_y = y + (h - av_d) / 2 - 1.0

    if avatar and os.path.exists(avatar):
        pic = slide.shapes.add_picture(avatar, Cm(av_x), Cm(av_y), Cm(av_d), Cm(av_d))
        _clip_shape(pic, "ellipse")
    else:
        o = slide.shapes.add_shape(MSO_SHAPE.OVAL, Cm(av_x), Cm(av_y),
                                   Cm(av_d), Cm(av_d))
        o.fill.solid()
        o.fill.fore_color.rgb = FONDO_INST
        o.line.color.rgb = GRIS_BORDE
        o.line.width = Pt(1)
        o.shadow.inherit = False
        ini = "".join(p[0] for p in str(nombre).split()[:2]).upper()
        tf = o.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        pp = tf.paragraphs[0]
        pp.alignment = PP_ALIGN.CENTER
        r = pp.add_run()
        r.text = ini
        r.font.size = Pt(20)
        r.font.bold = True
        r.font.name = F_TIT
        r.font.color.rgb = AZUL_ENCAB

    textbox(slide, av_x - 1.0, av_y + av_d + 0.25, av_d + 2.0, 2.0,
            [[(str(nombre), 11, True, AZUL_ENCAB, F_TIT)],
             [(str(cargo), 9, False, GRIS_TX, F_TXT)]],
            align=PP_ALIGN.CENTER, line_spacing=1.15)

    tx = av_x + av_d + 1.4
    tw = x + CONTENT_W - tx
    has_chips = bool(chips)
    textbox(slide, tx, y, tw, h - (2.0 if has_chips else 0.0),
            [[("“" + str(mensaje) + "”", 18, False, TEXTO, F_TIT)]],
            anchor=MSO_ANCHOR.MIDDLE, line_spacing=1.25)

    if has_chips:
        cw = 6.2
        cg = 0.5
        cyy = y + h - 1.6
        for i, ch in enumerate(list(chips)[:2]):
            lbl, val = ch
            bx = tx + i * (cw + cg)
            box = rect(slide, bx, cyy, cw, 1.5,
                       fill=RGBColor(0xEE, 0xF4, 0xFA), rounded=True)
            tf = box.text_frame
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf.margin_left = tf.margin_right = Cm(0.45)
            tf.margin_top = tf.margin_bottom = Cm(0.1)
            _set_runs(tf, [[(str(lbl).upper() + "   ", 7.5, True, GRIS_TX, F_TXT),
                            (str(val), 12, True, AZUL_ENCAB, F_TIT)]])
