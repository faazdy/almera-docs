# -*- coding: utf-8 -*-
"""
consolidar - pasa presentaciones YA HECHAS (por otros empleados, con o sin la
skill) a la plantilla institucional, sin cambiar su contenido.

Detalle del modo en `references/07-consolidar-presentaciones.md`.

Que hace, diapositiva por diapositiva:

- Portada / separador / cierre  ->  se rehacen con `Deck.portada` /
  `Deck.separador` (fondo azul, personaje, sellos). TODO su texto pasa a los
  campos del plan (kicker, titulo, subtitulo, meta / titulo, sub): no se pierde.
- Contenido  ->  diapositiva `Deck.contenido(titulo, sub)`: el titulo original
  se lleva a la BANDERA institucional (topbar azul) y el resto de formas se
  COPIAN TAL CUAL (texto, imagenes, tablas, graficas, SmartArt, grupos) y se
  reencuadran en la zona util (2.2 -> 31.7 cm  x  3.8 -> 14.2 cm), escalando
  en bloque solo si no caben. Las lineas "Fuente: ..." van a la linea de fuente.

Lo UNICO que se descarta es mobiliario de la plantilla vieja: numero de
diapositiva, fondos a sangre, formas decorativas sin texto que se salen del
borde y la banda que estaba detras del titulo (todo queda en el informe; con
"conservar_decoracion": true no se quita nada). Pie y fecha de la plantilla
vieja pasan a las notas del orador. Las notas del orador se conservan.

Un separador solo debe anunciar el tema que sigue: si trae ademas una lista de
puntos (vineta/numeral propios, o varias lineas largas), esos puntos se sacan
a una diapositiva de contenido aparte (tipo "puntos") en vez de amontonarlos
en el subtitulo del separador.

Uso (dos pasos; el plan se revisa con el usuario entre uno y otro):

    python consolidar.py inventario a.pptx b.pptx [-o plan.json] \
        [--portada-consolidada] [--titulo-consolidado "..."]
    python consolidar.py generar plan.json [-o consolidado.pptx]

`--portada-consolidada` antepone una portada nueva (en vez de la del primer
archivo) con las direcciones/areas detectadas en el subtitulo (mejor
esfuerzo, queda marcada para confirmar).
"""
import argparse
import copy
import io
import json
import math
import os
import re
import sys

from lxml import etree
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.opc.package import PartFactory, XmlPart
from pptx.opc.packuri import PackURI
from pptx.oxml.ns import qn
from pptx.util import Cm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pptx_kit as K  # noqa: E402

EMU_CM = 360000.0
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_MC = "http://schemas.openxmlformats.org/markup-compatibility/2006"
NS_DSP = "http://schemas.microsoft.com/office/drawing/2008/diagram"
CT_DGM_DATA = "application/vnd.openxmlformats-officedocument.drawingml.diagramData+xml"

SHAPE_TAGS = {qn("p:sp"), qn("p:pic"), qn("p:graphicFrame"), qn("p:grpSp"),
              qn("p:cxnSp"), qn("p:contentPart")}
# relaciones que no se copian (pertenecen a la presentacion de origen)
SKIP_RELS = {RT.SLIDE, RT.SLIDE_LAYOUT, RT.SLIDE_MASTER, RT.NOTES_SLIDE,
             RT.NOTES_MASTER, RT.THEME}

RX_PORTADA = re.compile(r"portada|title slide|diapositiva de t[ií]tulo|^t[ií]tulo$|cover", re.I)
RX_SEPARADOR = re.compile(r"separador|secci[oó]n|section|divis", re.I)
RX_CIERRE = re.compile(r"cierre|closing|contraportada", re.I)
RX_TXT_CIERRE = re.compile(r"^\s*(gracias|muchas gracias|preguntas|fin)\b", re.I)
RX_FUENTE = re.compile(r"^\s*(fuente|fuentes|nota|elaboraci[oó]n)\s*:", re.I)
RX_NUM = re.compile(r"^\d{1,2}\.?$")
RX_DIRECCION = re.compile(r"direcci[oó]n|subdirecci[oó]n|gerencia|vicepresidencia|coordinaci[oó]n"
                          r"|oficina|departamento|\barea\b|talento humano", re.I)
TOPBAR_FILLS = {"003971": False, "2A3B52": True}   # fill del topbar de la skill -> anexo?
TIPOS_MARCO = ("portada", "separador", "cierre")
# tipos que se pueden generar sin "archivo" de origen (formas nuevas, no copiadas)
TIPOS_SIN_ARCHIVO = TIPOS_MARCO + ("puntos",)


# --------------------------------------------------------------------------- #
#  Utilidades XML
# --------------------------------------------------------------------------- #
def _local(el):
    return etree.QName(el).localname


def _order_insert(parent, child, order):
    """Inserta `child` en `parent` respetando el orden de schema `order`."""
    name = _local(child)
    pos = order.index(name) if name in order else len(order)
    for i, c in enumerate(parent):
        cn = _local(c)
        if cn in order and order.index(cn) > pos:
            parent.insert(i, child)
            return child
    parent.append(child)
    return child


# orden de hijos segun el schema de DrawingML (solo lo que se toca aqui)
ORD_PPR = ["lnSpc", "spcBef", "spcAft", "buClrTx", "buClr", "buSzTx", "buSzPct",
           "buSzPts", "buFontTx", "buFont", "buNone", "buAutoNum", "buChar",
           "buBlip", "tabLst", "defRPr", "extLst"]
ORD_RPR = ["ln", "noFill", "solidFill", "gradFill", "blipFill", "pattFill",
           "grpFill", "effectLst", "effectDag", "highlight", "uLnTx", "uLn",
           "uFillTx", "uFill", "latin", "ea", "cs", "sym", "hlinkClick",
           "hlinkMouseOver", "rtl", "extLst"]
ORD_SPPR = ["xfrm", "custGeom", "prstGeom", "noFill", "solidFill", "gradFill",
            "blipFill", "pattFill", "grpFill", "ln", "effectLst", "effectDag",
            "scene3d", "sp3d", "extLst"]
ORD_BODYPR = ["prstTxWarp", "noAutofit", "normAutofit", "spAutoFit", "scene3d",
              "sp3d", "flatTx", "extLst"]
ORD_LST = ["defPPr"] + ["lvl%dpPr" % i for i in range(1, 10)] + ["extLst"]
GROUPS = {}
for _g in (["buClrTx", "buClr"], ["buSzTx", "buSzPct", "buSzPts"],
           ["buFontTx", "buFont"], ["buNone", "buAutoNum", "buChar", "buBlip"],
           ["noFill", "solidFill", "gradFill", "blipFill", "pattFill", "grpFill"],
           ["effectLst", "effectDag"], ["uLnTx", "uLn"], ["uFillTx", "uFill"],
           ["custGeom", "prstGeom"], ["noAutofit", "normAutofit", "spAutoFit"]):
    for _n in _g:
        GROUPS[_n] = tuple(_g)


def _grupo(name):
    return GROUPS.get(name, (name,))


def _merge_props(base, over, order):
    """Fusiona dos elementos de propiedades (lvlNpPr / defRPr): atributos de
    `over` pisan los de `base`; hijos por grupo de schema (un buChar pisa un
    buNone, un solidFill pisa un noFill...). Devuelve un elemento nuevo."""
    if base is None:
        return copy.deepcopy(over)
    if over is None:
        return copy.deepcopy(base)
    res = copy.deepcopy(base)
    for k, v in over.attrib.items():
        res.set(k, v)
    for ch in over:
        name = _local(ch)
        nuevo = copy.deepcopy(ch)
        for ex in list(res):
            if _local(ex) in _grupo(name):
                if name == "defRPr":
                    nuevo = _merge_props(ex, ch, ORD_RPR)
                res.remove(ex)
        _order_insert(res, nuevo, order)
    return res


def _merge_lst(styles):
    """Fusiona una cadena de lstStyle/txStyles (de lo general a lo especifico)
    en un unico a:lstStyle con los niveles resueltos."""
    lst = etree.Element(qn("a:lstStyle"))
    for i in range(1, 10):
        tag = "lvl%dpPr" % i
        acc = None
        for st in styles:
            if st is None:
                continue
            e = st.find(qn("a:" + tag))
            if e is not None:
                acc = _merge_props(acc, e, ORD_PPR)
        if acc is not None:
            acc.tag = qn("a:" + tag)
            _order_insert(lst, acc, ORD_LST)
    return lst


def _texto_parrafo(p):
    out = []
    for e in p.iter(qn("a:t"), qn("a:br")):
        out.append(" " if e.tag == qn("a:br") else (e.text or ""))
    return re.sub(r"\s+", " ", "".join(out)).strip()


def _parrafos(el):
    """Parrafos con texto de una forma, en orden."""
    txb = el.find(qn("p:txBody"))
    if txb is None:
        return []
    return [p for p in txb.findall(qn("a:p")) if _texto_parrafo(p)]


def _texto(el):
    return " ".join(t for t in (_texto_parrafo(p) for p in el.iter(qn("a:p"))) if t)


def _xml_blob(root):
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone=True)


# --------------------------------------------------------------------------- #
#  Presentacion de origen y herencia de placeholders
# --------------------------------------------------------------------------- #
class Origen:
    """Una presentacion de origen abierta, con su estilo de texto por defecto."""

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.nombre = os.path.basename(path)
        self.prs = Presentation(path)
        self.W = self.prs.slide_width
        self.H = self.prs.slide_height
        self.default_style = self.prs.part._element.find(qn("p:defaultTextStyle"))

    def slide(self, n):
        return self.prs.slides[n - 1]


def _ph_info(el):
    for tag in ("p:nvSpPr", "p:nvPicPr", "p:nvGraphicFramePr", "p:nvGrpSpPr", "p:nvCxnSpPr"):
        nv = el.find(qn(tag))
        if nv is not None:
            ph = nv.find(qn("p:nvPr") + "/" + qn("p:ph"))
            if ph is None:
                return None
            return {"el": ph, "type": ph.get("type", "obj"), "idx": ph.get("idx", "0")}
    return None


_NORM_PH = {"ctrTitle": "title", "subTitle": "body", "obj": "body"}


def _find_ph(root, typ, idx, by_idx=True):
    cands = []
    for e in root.iter(qn("p:sp"), qn("p:pic"), qn("p:graphicFrame")):
        info = _ph_info(e)
        if info:
            cands.append((e, info))
    if by_idx and idx != "0":
        for e, info in cands:
            if info["idx"] == idx:
                return e
    t = _NORM_PH.get(typ, typ)
    for e, info in cands:
        if _NORM_PH.get(info["type"], info["type"]) == t:
            return e
    return None


def _cadena_ph(slide, el):
    """(master_ph, layout_ph, txStyle del master) del placeholder `el`."""
    info = _ph_info(el)
    if not info:
        return None, None, None
    layout = slide.slide_layout
    master = layout.slide_master
    lay = _find_ph(layout._element, info["type"], info["idx"], by_idx=True)
    mas = _find_ph(master._element, info["type"], info["idx"], by_idx=False)
    tx = master._element.find(qn("p:txStyles"))
    key = {"title": "titleStyle", "ctrTitle": "titleStyle", "dt": "otherStyle",
           "ftr": "otherStyle", "sldNum": "otherStyle"}.get(info["type"], "bodyStyle")
    txs = tx.find(qn("p:" + key)) if tx is not None else None
    return mas, lay, txs


def _lst_de(el):
    txb = el.find(qn("p:txBody")) if el is not None else None
    return txb.find(qn("a:lstStyle")) if txb is not None else None


def _estilo_efectivo(org, slide, el):
    """a:lstStyle resuelto para la forma `el` (placeholder o no)."""
    if _ph_info(el):
        mas, lay, txs = _cadena_ph(slide, el)
        chain = [org.default_style, txs, _lst_de(mas), _lst_de(lay), _lst_de(el)]
    else:
        chain = [org.default_style, _lst_de(el)]
    return _merge_lst(chain)


def _sz_base(lst, lvl, default_style=None):
    for st in (lst, default_style):
        lv = st.find(qn("a:lvl%dpPr" % (lvl + 1))) if st is not None else None
        d = lv.find(qn("a:defRPr")) if lv is not None else None
        if d is not None and d.get("sz"):
            return int(d.get("sz"))
    return 1800


def _nivel(p):
    ppr = p.find(qn("a:pPr"))
    return int(ppr.get("lvl", "0")) if ppr is not None else 0


def _sz_parrafo(p, lst):
    """Tamano mayor de un parrafo (centesimas de pt), resuelto por herencia."""
    base = _sz_base(lst, _nivel(p))
    sizes = []
    for r in p.iter(qn("a:r"), qn("a:fld")):
        rpr = r.find(qn("a:rPr"))
        sizes.append(int(rpr.get("sz")) if rpr is not None and rpr.get("sz") else base)
    return max(sizes) if sizes else base


# --------------------------------------------------------------------------- #
#  Geometria de formas (EMU)
# --------------------------------------------------------------------------- #
def _xfrm(el):
    if el.tag == qn("p:graphicFrame"):
        return el.find(qn("p:xfrm"))
    if el.tag == qn("p:grpSp"):
        g = el.find(qn("p:grpSpPr"))
        return g.find(qn("a:xfrm")) if g is not None else None
    sppr = el.find(qn("p:spPr"))
    return sppr.find(qn("a:xfrm")) if sppr is not None else None


def _tiene_off(xf):
    return xf is not None and xf.find(qn("a:off")) is not None and xf.find(qn("a:ext")) is not None


def _caja(el, slide=None):
    """(x, y, w, h, rot). Si es placeholder sin posicion propia, la hereda."""
    xf = _xfrm(el)
    if not _tiene_off(xf) and slide is not None and _ph_info(el):
        mas, lay, _ = _cadena_ph(slide, el)
        for src in (lay, mas):
            if src is not None and _tiene_off(_xfrm(src)):
                xf = _xfrm(src)
                break
    if not _tiene_off(xf):
        return None
    off, ext = xf.find(qn("a:off")), xf.find(qn("a:ext"))
    return (int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy")),
            int(xf.get("rot", "0")) / 60000.0)


def _aabb(c):
    """Caja envolvente (alineada a ejes) de una caja posiblemente rotada."""
    x, y, w, h, rot = c
    if not rot or rot % 180 == 0:
        return x, y, w, h
    a = math.radians(rot)
    bw = abs(w * math.cos(a)) + abs(h * math.sin(a))
    bh = abs(w * math.sin(a)) + abs(h * math.cos(a))
    cx, cy = x + w / 2.0, y + h / 2.0
    return cx - bw / 2.0, cy - bh / 2.0, bw, bh


def _set_caja(el, x, y, w, h):
    xf = _xfrm(el)
    if xf is None:
        if el.tag == qn("p:graphicFrame"):
            xf = etree.Element(qn("p:xfrm"))
            el.find(qn("p:nvGraphicFramePr")).addnext(xf)
        else:
            tag = "p:grpSpPr" if el.tag == qn("p:grpSp") else "p:spPr"
            sppr = el.find(qn(tag))
            xf = etree.Element(qn("a:xfrm"))
            sppr.insert(0, xf)
    for t in ("a:off", "a:ext"):
        if xf.find(qn(t)) is None:
            etree.SubElement(xf, qn(t))
    xf.find(qn("a:off")).set("x", str(int(round(x))))
    xf.find(qn("a:off")).set("y", str(int(round(y))))
    xf.find(qn("a:ext")).set("cx", str(int(round(w))))
    xf.find(qn("a:ext")).set("cy", str(int(round(h))))


def _tiene_imagen(el):
    return el.find(".//" + qn("a:blip")) is not None


# --------------------------------------------------------------------------- #
#  Analisis de una diapositiva
# --------------------------------------------------------------------------- #
def _elementos(slide):
    """Formas de primer nivel. mc:AlternateContent se resuelve a su Fallback
    (valido en cualquier version de PowerPoint)."""
    out = []
    for ch in slide.shapes._spTree:
        if ch.tag in SHAPE_TAGS:
            out.append(ch)
        elif ch.tag == "{%s}AlternateContent" % NS_MC:
            fb = ch.find("{%s}Fallback" % NS_MC)
            if fb is None:
                fb = ch.find("{%s}Choice" % NS_MC)
            if fb is not None:
                out.extend(e for e in fb if e.tag in SHAPE_TAGS)
    return out


def _es_bandera_skill(el):
    """None si no es el topbar de pptx_kit; si lo es, True/False = anexo."""
    if el.tag != qn("p:sp") or not _texto(el):
        return None
    geo = el.find(qn("p:spPr") + "/" + qn("a:prstGeom"))
    clr = el.find(qn("p:spPr") + "/" + qn("a:solidFill") + "/" + qn("a:srgbClr"))
    c = _caja(el)
    if geo is None or geo.get("prst") != "roundRect" or clr is None or c is None:
        return None
    val = clr.get("val", "").upper()
    if val in TOPBAR_FILLS and abs(c[1] / EMU_CM - K.TOP_Y) < 0.3:
        return TOPBAR_FILLS[val]
    return None


def _mejor_figura(slide, pics, W, H):
    """Imagen que puede hacer de personaje en portada/separador: la mas grande
    con proporcion de figura (no franjas de logos ni URL) y tamano apreciable."""
    best, area = None, 0
    for el in pics:
        c = _caja(el, slide)
        if not c or not c[3] or not _tiene_imagen(el):
            continue
        a, ratio = c[2] * c[3], c[2] / float(c[3])
        if 0.35 <= ratio <= 2.2 and 0.06 * W * H <= a < 0.85 * W * H and a > area:
            best, area = el, a
    return best


def analizar(org, n):
    """Clasifica la diapositiva `n` de `org` y separa titulo, pie, fuente,
    decoracion y contenido. No modifica el origen."""
    slide = org.slide(n)
    W, H = org.W, org.H
    layout_name = slide.slide_layout.name or ""
    r = {"n": n, "layout": layout_name, "titulo": None, "sub": None, "anexo": False,
         "titulo_el": None, "pie": [], "decoracion": [], "fuente": [], "contenido": [],
         "origen_titulo": "ninguno"}

    # 1. placeholders de mobiliario (numero, pie, fecha)
    resto = []
    for el in _elementos(slide):
        info = _ph_info(el)
        if info and info["type"] in ("sldNum", "dt", "ftr"):
            if info["type"] != "sldNum" and _texto(el):
                r["pie"].append(_texto(el))
        else:
            resto.append(el)

    # 2. titulo: placeholder -> bandera de la skill -> texto dominante
    tit = None
    for el in resto:
        info = _ph_info(el)
        if info and info["type"] in ("title", "ctrTitle") and _texto(el):
            tit, r["origen_titulo"] = el, "placeholder"
            break
    if tit is None:
        for el in resto:
            dark = _es_bandera_skill(el)
            if dark is not None:
                tit, r["origen_titulo"], r["anexo"] = el, "bandera de la skill", dark
                break
    textos = [el for el in resto if el.tag == qn("p:sp") and _parrafos(el)]
    medidas = {}
    for el in textos:
        lst = _estilo_efectivo(org, slide, el)
        ps = _parrafos(el)
        medidas[el] = (_sz_parrafo(ps[0], lst), max(_sz_parrafo(p, lst) for p in ps),
                       _texto_parrafo(ps[0]))
    if tit is None and textos:
        cands = [el for el in textos if not RX_FUENTE.match(medidas[el][2])
                 and len(medidas[el][2]) <= 150 and _caja(el, slide)]
        if cands:
            best = max(cands, key=lambda e: (medidas[e][0], -_caja(e, slide)[1]))
            otros = [medidas[e][1] for e in textos if e is not best] or [0]
            y = _caja(best, slide)[1]
            dominante = medidas[best][0] >= 1.2 * max(otros)
            arriba = y < 0.30 * H and medidas[best][0] >= max(otros)
            if dominante or arriba:
                tit, r["origen_titulo"] = best, "heuristica"
    if tit is not None:
        ps = [_texto_parrafo(p) for p in _parrafos(tit)]
        if r["origen_titulo"] == "placeholder":
            r["titulo"] = " ".join(ps)
        else:
            r["titulo"], r["sub"] = ps[0], (" · ".join(ps[1:]) or None)
        r["titulo_el"] = tit
        resto = [e for e in resto if e is not tit]

    # 3. tipo de diapositiva
    ricos = [e for e in resto if e.tag in (qn("p:graphicFrame"), qn("p:grpSp"))]
    textos_resto = [e for e in resto if e.tag == qn("p:sp") and _texto(e)]
    chars = sum(len(_texto(e)) for e in textos_resto) + len(r["titulo"] or "")
    todo = " ".join([r["titulo"] or ""] + [_texto(e) for e in textos_resto]).strip()
    skill = r["origen_titulo"] == "bandera de la skill"
    tipo, por = "contenido", "contenido"
    if not ricos and not skill:
        if RX_PORTADA.search(layout_name):
            tipo, por = "portada", "layout"
        elif RX_SEPARADOR.search(layout_name):
            tipo, por = "separador", "layout"
        elif RX_CIERRE.search(layout_name):
            tipo, por = "cierre", "layout"
        elif RX_TXT_CIERRE.match(todo) and chars < 120:
            tipo, por = "cierre", "texto"
        elif n == 1 and chars < 250:
            tipo, por = "portada", "primera diapositiva"
        elif chars < 60 and len(textos_resto) + (1 if tit is not None else 0) <= 2:
            tipo, por = "separador", "heuristica"
    r["tipo"], r["tipo_por"] = tipo, por

    # 4. decoracion / fuente / contenido
    area_sl = float(W) * H
    ct = _caja(tit, slide) if tit is not None else None
    tcaja = _aabb(ct) if ct else None
    for el in resto:
        c = _caja(el, slide)
        if c is None:
            r["contenido"].append(el)
            continue
        x, y, w, h = _aabb(c)
        txt = _texto(el)
        es_pic = el.tag == qn("p:pic")
        es_forma = el.tag == qn("p:sp") and not txt and not _tiene_imagen(el)
        sangra = x < -0.02 * W or y < -0.02 * H or x + w > 1.02 * W or y + h > 1.02 * H
        fondo = w * h >= 0.85 * area_sl and (es_pic or es_forma)
        detras_titulo = False
        if es_forma and tcaja:
            ix = max(0, min(x + w, tcaja[0] + tcaja[2]) - max(x, tcaja[0]))
            iy = max(0, min(y + h, tcaja[1] + tcaja[3]) - max(y, tcaja[1]))
            # la banda del titulo: lo cubre y es de su tamano (una tarjeta que
            # contiene titulo + texto es mucho mas grande y SI es contenido)
            detras_titulo = (ix * iy >= 0.6 * tcaja[2] * tcaja[3]
                             and w * h <= 3.0 * tcaja[2] * tcaja[3])
        # linea de pie / fuente: por texto ("Fuente: ...") o, si no trae ese
        # prefijo, por geometria (linea angosta y ancha muy abajo, como la que
        # pone `pptx_kit.fuente()` — no toda nota de pie dice "Fuente:").
        es_nota_pie = el.tag == qn("p:sp") and txt and (
            RX_FUENTE.match(txt) or (y > 0.70 * H and h <= 0.06 * H and w >= 0.5 * W))
        if fondo or (es_forma and (sangra or detras_titulo)):
            r["decoracion"].append(el)
        elif es_nota_pie:
            r["fuente"].append(el)
        else:
            r["contenido"].append(el)
    # la pastilla detras de una linea de fuente tambien es decoracion
    for f in r["fuente"]:
        fx, fy, fw, fh = _aabb(_caja(f, slide))
        for el in list(r["contenido"]):
            c = _caja(el, slide)
            if c and el.tag == qn("p:sp") and not _texto(el) and not _tiene_imagen(el):
                x, y, w, h = _aabb(c)
                if x <= fx + fw / 2 <= x + w and y <= fy + fh / 2 <= y + h and w * h < 6 * fw * fh:
                    r["contenido"].remove(el)
                    r["decoracion"].append(el)

    # 5. todas las lineas de texto, en orden de lectura (para portada/separador).
    # cada linea lleva ademas si es un punto de una lista con vineta/numeral
    # propios (buChar/buAutoNum): eso distingue "puntos a tratar" de una
    # simple linea de metadato (area, fecha) para no saturar el separador.
    def _pos(e):
        c = _caja(e, slide)
        return (c[1], c[0]) if c else (0, 0)

    def _es_lista(p):
        ppr = p.find(qn("a:pPr"))
        return ppr is not None and (ppr.find(qn("a:buChar")) is not None
                                    or ppr.find(qn("a:buAutoNum")) is not None)
    lineas = []
    for el in sorted(([tit] if tit is not None else []) + textos_resto, key=_pos):
        lst = _estilo_efectivo(org, slide, el)
        for p in _parrafos(el):
            lineas.append((_texto_parrafo(p), _sz_parrafo(p, lst), _es_lista(p)))
    r["lineas"] = lineas + [(t, 0, False) for t in r["pie"]]
    r["imagenes"] = [e for e in resto if e.tag == qn("p:pic")]
    r["figura"] = _mejor_figura(slide, r["imagenes"], W, H)
    r["ricos_marco"] = ricos
    r["notas"] = ""
    if slide.has_notes_slide and slide.notes_slide.notes_text_frame is not None:
        r["notas"] = slide.notes_slide.notes_text_frame.text
    r["oculta"] = slide._element.get("show") == "0"
    r["animaciones"] = slide._element.find(qn("p:timing")) is not None
    return r


# --------------------------------------------------------------------------- #
#  Inventario -> plan
# --------------------------------------------------------------------------- #
def _direccion_de(a):
    """Mejor intento de sacar el nombre del area/direccion de una portada o
    separador, para sugerir el subtitulo de una portada 'Consolidado de
    presentaciones'. Primero busca una linea que mencione claramente un area
    (por palabra clave: 'Direccion', 'Gerencia'...) en cualquier posicion —
    el kicker de esta misma skill ("INFORME DE GESTION") no es un area y no
    la lleva; si ninguna linea trae esa palabra, cae a la heuristica
    posicional (la linea corta justo antes o despues del titulo)."""
    lineas = [(t, s) for t, s, _ in a["lineas"] if not RX_NUM.match(t)]
    if not lineas:
        return None
    i = [s for _, s in lineas].index(max(s for _, s in lineas))
    textos = [t for t, _ in lineas]
    resto = textos[:i] + textos[i + 1:]
    for t in resto:
        if t and len(t) <= 90 and not RX_FUENTE.match(t) and RX_DIRECCION.search(t):
            return t
    for c in ([textos[i - 1]] if i > 0 else []) + textos[i + 1:i + 2]:
        if c and len(c) <= 60 and not RX_FUENTE.match(c):
            return c
    return None


def _pick_metadato(textos):
    """Elige, de una lista de lineas de metadato (no de puntos a tratar), la
    que mas suene a area/direccion; si ninguna, la primera. Se usa para dejar
    una sola linea corta bajo un separador que viene de una portada ajena."""
    for t in textos:
        if t and len(t) <= 90 and not RX_FUENTE.match(t) and RX_DIRECCION.search(t):
            return t
    return textos[0] if textos else None


def _entrada_plan(org, a, es_primera_portada):
    """Devuelve una lista de 1 o 2 entradas de plan: 2 cuando un separador
    trae 'puntos a tratar' (lista con vineta propia, o varias lineas largas)
    que se separan a una diapositiva de contenido aparte para dejarlo limpio
    — ver SKILL.md -> 'Consolidar presentaciones existentes'."""
    ent = {"archivo": org.path, "n": a["n"], "tipo": a["tipo"]}
    avisos, extra = [], None
    if a["tipo"] in TIPOS_MARCO:
        reclasificada = a["tipo"] == "portada" and not es_primera_portada
        if reclasificada:
            ent["tipo"] = "separador"
            avisos.append("portada de una presentacion que no es la primera -> separador")
        lineas = [(t, s, b) for t, s, b in a["lineas"] if not RX_NUM.match(t)]
        textos = [t for t, _, _ in lineas]
        i = [s for _, s, _ in lineas].index(max(s for _, s, _ in lineas)) if lineas else 0
        titulo = textos[i] if textos else ""
        resto = lineas[:i] + lineas[i + 1:]
        if ent["tipo"] == "portada":
            antes = [t for t, _, _ in lineas[:i]]
            despues = [t for t, _, _ in lineas[i + 1:]]
            ent.update({"kicker": " · ".join(antes), "titulo": titulo,
                        "subtitulo": despues[0] if despues else "", "meta": despues[1:]})
        elif reclasificada:
            # viene de una portada (kicker/subtitulo/meta), no es una lista de
            # puntos a tratar: se deja una sola linea corta (la que mas suene
            # a area/fecha) y el resto -> notas del orador, no una diapositiva
            # de viñetas (se veria raro repitiendo metadatos de portada).
            textos_resto = [t for t, _, _ in resto]
            sub = _pick_metadato(textos_resto)
            ent.update({"titulo": titulo, "sub": sub, "num": None})
            resto_extra = [t for t in textos_resto if t != sub]
            if resto_extra:
                ent["_nota_extra"] = resto_extra
                avisos.append("metadatos de la portada original (%s) van a notas del orador"
                              % "; ".join(resto_extra))
        else:
            textos_resto = [t for t, _, _ in resto]
            # "puntos a tratar": la lista trae vineta/numeral propios, o son
            # varias lineas, o el texto combinado es largo -> no caben como
            # una sola linea de metadato bajo el separador sin saturarlo.
            saturado = (any(b for _, _, b in resto) or len(textos_resto) > 2
                       or sum(len(t) for t in textos_resto) > 100)
            if ent["tipo"] == "separador" and saturado and textos_resto:
                ent.update({"titulo": titulo, "sub": None})
                extra = {"archivo": None, "tipo": "puntos", "titulo": titulo,
                         "puntos": textos_resto,
                         "_avisos": ["diapositiva generada con los puntos que traia el "
                                     "separador original, para no saturarlo: revisar "
                                     "titulo y contenido"]}
            else:
                ent.update({"titulo": titulo, "sub": " · ".join(textos_resto) or None})
            if ent["tipo"] == "separador":
                ent["num"] = None
        ent["figura"] = "original" if a["figura"] is not None else None
        otras = len(a["imagenes"]) - (1 if a["figura"] is not None else 0)
        if otras:
            avisos.append("%d imagen(es) de marca de la plantilla vieja (logos, franjas, "
                          "iconos) no se pasan%s" % (otras, "; el personaje original si"
                                                     if a["figura"] is not None else ""))
        if a["tipo_por"] in ("heuristica", "primera diapositiva", "texto"):
            avisos.append("tipo '%s' deducido por %s: confirmar" % (a["tipo"], a["tipo_por"]))
    else:
        ent.update({"titulo": a["titulo"], "sub": a["sub"], "anexo": a["anexo"]})
        if not a["titulo"]:
            avisos.append("sin titulo detectable: proponer uno (si no, 'titulo anterior (cont.)')")
        elif a["origen_titulo"] == "heuristica":
            avisos.append("titulo deducido (texto dominante): confirmar")
        if a["titulo"] and len(a["titulo"]) > 90:
            avisos.append("titulo largo (%d car.)" % len(a["titulo"]))
        if a["decoracion"]:
            avisos.append("%d forma(s) decorativa(s) de la plantilla vieja no se pasan"
                          % len(a["decoracion"]))
        if not a["contenido"] and not a["fuente"]:
            avisos.append("solo tiene titulo: ¿separador?")
    if a["pie"]:
        avisos.append("pie/fecha de la plantilla vieja -> notas del orador")
    if a["animaciones"]:
        avisos.append("tiene animaciones: no se conservan")
    if a["oculta"]:
        avisos.append("diapositiva oculta: se mantiene oculta")
    if avisos:
        ent["_avisos"] = avisos
    return [ent] if extra is None else [ent, extra]


def inventario(paths, portada_consolidada=False,
              titulo_consolidado="Consolidado de presentaciones"):
    """`portada_consolidada=True` antepone una portada nueva con ese titulo y,
    en el subtitulo, las direcciones/areas detectadas en cada archivo (mejor
    esfuerzo: confirmar en el plan). Cuando se usa, la portada propia de cada
    archivo de origen pasa a separador (incluida la del primero)."""
    plan = {"salida": "consolidado.pptx", "normalizar_fuentes": True,
            "conservar_decoracion": False, "trazabilidad_en_notas": False,
            "diapositivas": []}
    primera, direcciones = True, []
    for path in paths:
        org = Origen(path)
        for n in range(1, len(org.prs.slides) + 1):
            a = analizar(org, n)
            if n == 1:
                d = _direccion_de(a)
                if d and d not in direcciones:
                    direcciones.append(d)
            es_primera = primera and not portada_consolidada
            plan["diapositivas"].extend(_entrada_plan(org, a, es_primera_portada=es_primera))
            primera = False
    if portada_consolidada:
        cover = {"archivo": None, "tipo": "portada", "kicker": "",
                 "titulo": titulo_consolidado, "subtitulo": " · ".join(direcciones),
                 "meta": [],
                 "_avisos": ["direcciones detectadas automaticamente en la portada de cada "
                            "archivo: confirmar o completar"] if direcciones else
                           ["no se detectaron direcciones/areas en los archivos de origen: "
                            "completar el subtitulo a mano si aplica"]}
        plan["diapositivas"].insert(0, cover)
    return plan


def _resumen(plan):
    filas = ["| # | Origen | Tipo | Titulo (bandera) | Avisos |", "|---|---|---|---|---|"]
    for i, e in enumerate(plan["diapositivas"], 1):
        tit = e.get("titulo") or "—"
        if e.get("sub"):
            tit += "  ·  _%s_" % e["sub"]
        orig = "%s #%s" % (os.path.basename(e["archivo"]), e["n"]) if e.get("archivo") else "nueva"
        filas.append("| %d | %s | %s | %s | %s |" % (
            i, orig, e["tipo"], tit.replace("|", "/"), "; ".join(e.get("_avisos", []))))
    return "\n".join(filas)


# --------------------------------------------------------------------------- #
#  Copia de formas entre presentaciones
# --------------------------------------------------------------------------- #
class Copiador:
    """Copia formas de una diapositiva de origen a una de destino junto con
    sus partes relacionadas (imagenes, graficas + Excel, SmartArt, medios,
    enlaces externos)."""

    def __init__(self, dst_prs):
        self.pkg = dst_prs.part.package
        self.cache = {}
        self.usados = set()

    def _partname(self, src_name):
        m = re.match(r"^(.*?)(\d*)(\.\w+)$", src_name)
        tmpl = m.group(1) + "%d" + m.group(3)
        existentes = {str(p.partname) for p in self.pkg.iter_parts()} | self.usados
        n = 1
        while tmpl % n in existentes:
            n += 1
        self.usados.add(tmpl % n)
        return PackURI(tmpl % n)

    def _imagen(self, src_part):
        try:
            return self.pkg.get_or_add_image_part(io.BytesIO(src_part.blob))
        except Exception:
            return None   # SVG u otro formato que PIL no lee -> copia generica

    def copiar_parte(self, src):
        key = (id(src.package), str(src.partname))
        if key in self.cache:
            return self.cache[key]
        new = PartFactory(self._partname(str(src.partname)), src.content_type,
                          self.pkg, src.blob)
        self.cache[key] = new
        rmap = {}
        for rId, rel in list(src.rels.items()):
            nuevo = self._relacion(new, rel)
            if nuevo:
                rmap[rId] = nuevo
        if isinstance(new, XmlPart):
            self._reescribir(new._element, rmap, quitar=False)
        elif new.content_type.endswith("xml") and rmap:
            try:
                root = etree.fromstring(new.blob)
                self._reescribir(root, rmap, quitar=False)
                new._blob = _xml_blob(root)
            except Exception:
                pass
        return new

    def _relacion(self, dst_part, rel):
        """Replica `rel` en `dst_part`; devuelve el rId nuevo o None."""
        if rel.is_external:
            return dst_part.relate_to(rel.target_ref, rel.reltype, is_external=True)
        if rel.reltype in SKIP_RELS:
            return None
        tgt = rel.target_part
        if rel.reltype == RT.IMAGE:
            img = self._imagen(tgt)
            if img is not None:
                return dst_part.relate_to(img, RT.IMAGE)
        return dst_part.relate_to(self.copiar_parte(tgt), rel.reltype)

    @staticmethod
    def _reescribir(root, rmap, quitar=True):
        for e in list(root.iter()):
            for k, v in list(e.attrib.items()):
                if not k.startswith("{%s}" % NS_R):
                    continue
                if v in rmap:
                    e.set(k, rmap[v])
                elif quitar:
                    if _local(e) in ("hlinkClick", "hlinkHover", "hlinkMouseOver"):
                        if e.getparent() is not None:
                            e.getparent().remove(e)
                        break
                    del e.attrib[k]

    def copiar_forma(self, el, src_slide, dst_slide, avisos):
        """Copia de `el` con sus relaciones ya apuntando a `dst_slide`."""
        new = copy.deepcopy(el)
        src_part, dst_part = src_slide.part, dst_slide.part
        rids = {v for e in new.iter() for k, v in e.attrib.items()
                if k.startswith("{%s}" % NS_R)}
        rmap = {}
        for rId in rids:
            if rId not in src_part.rels:
                continue
            rel = src_part.rels[rId]
            if not rel.is_external and rel.reltype in SKIP_RELS:
                avisos.append("hipervinculo a otra diapositiva quitado (el texto se conserva)")
                continue
            nuevo = self._relacion(dst_part, rel)
            if nuevo:
                rmap[rId] = nuevo
        self._reescribir(new, rmap)
        # SmartArt: la parte "drawing" cuelga de la diapositiva y se referencia
        # por relId dentro de la parte de datos
        for e in new.iter():
            if _local(e) != "relIds" or not e.get(qn("r:dm")):
                continue
            data = dst_part.related_part(e.get(qn("r:dm")))
            if data.content_type == CT_DGM_DATA:
                self._smartart_drawing(data, src_part, dst_part)
        return new

    def _smartart_drawing(self, data, src_slide_part, dst_slide_part):
        es_xml = isinstance(data, XmlPart)
        root = data._element if es_xml else etree.fromstring(data.blob)
        for ext in list(root.iter("{%s}dataModelExt" % NS_DSP)):
            rid = ext.get("relId")
            if rid and rid in src_slide_part.rels:
                nuevo = self._relacion(dst_slide_part, src_slide_part.rels[rid])
                if nuevo:
                    ext.set("relId", nuevo)
                    continue
            ext.getparent().remove(ext)   # PowerPoint lo redibuja desde los datos
        if not es_xml:
            data._blob = _xml_blob(root)


# --------------------------------------------------------------------------- #
#  Normalizacion de una forma copiada
# --------------------------------------------------------------------------- #
def _materializar_ph(new, org, src_slide, src_el):
    """Convierte un placeholder copiado en forma normal: posicion, relleno y
    estilo de cuadro heredados pasan a ser explicitos (su layout no existe en
    la plantilla institucional)."""
    info = _ph_info(new)
    if not info:
        return
    c = _caja(src_el, src_slide)
    if c:
        _set_caja(new, *c[:4])
    mas, lay, _ = _cadena_ph(src_slide, src_el)
    sppr = new.find(qn("p:spPr"))
    txb = new.find(qn("p:txBody"))
    bp = txb.find(qn("a:bodyPr")) if txb is not None else None
    for src in (lay, mas):
        if src is None:
            continue
        ssp = src.find(qn("p:spPr"))
        if sppr is not None and ssp is not None:
            for ch in ssp:
                if _local(ch) == "xfrm":
                    continue
                if not any(_local(x) in _grupo(_local(ch)) for x in sppr):
                    _order_insert(sppr, copy.deepcopy(ch), ORD_SPPR)
        stx = src.find(qn("p:txBody"))
        sbp = stx.find(qn("a:bodyPr")) if stx is not None else None
        if bp is not None and sbp is not None:
            for k, v in sbp.attrib.items():
                if k not in bp.attrib:
                    bp.set(k, v)
            for ch in sbp:
                if not any(_local(x) in _grupo(_local(ch)) for x in bp):
                    _order_insert(bp, copy.deepcopy(ch), ORD_BODYPR)
    info["el"].getparent().remove(info["el"])


def _explicitar_texto(new, org, src_slide, src_el):
    """Estilo de texto resuelto dentro de la forma + tamano explicito en cada
    corrida: asi no depende de la plantilla de origen y se puede escalar."""
    txb = new.find(qn("p:txBody"))
    if txb is not None:
        lst = _estilo_efectivo(org, src_slide, src_el)
        old = txb.find(qn("a:lstStyle"))
        if old is not None:
            txb.replace(old, lst)
        else:
            txb.find(qn("a:bodyPr")).addnext(lst)
    for body in list(new.iter(qn("p:txBody"), qn("a:txBody"))):
        lst = body.find(qn("a:lstStyle"))
        for p in body.findall(qn("a:p")):
            base = str(_sz_base(lst, _nivel(p), org.default_style))
            for r in p:
                n = _local(r)
                if n not in ("r", "fld", "endParaRPr"):
                    continue
                rpr = r if n == "endParaRPr" else r.find(qn("a:rPr"))
                if rpr is None:
                    rpr = etree.Element(qn("a:rPr"))
                    r.insert(0, rpr)
                if not rpr.get("sz"):
                    rpr.set("sz", base)


def _normalizar_fuentes(new):
    for e in new.iter(qn("a:latin")):
        tf = e.get("typeface", "")
        if tf and not tf.startswith("+"):
            e.set("typeface", K.F_TXT)


def _escalar_texto(new, s):
    """Escala tamanos de letra, sangrias, espaciados fijos, margenes internos y
    medidas de tabla. Devuelve el tamano minimo resultante en pt."""
    minimo = None

    def esc(e, k):
        if e.get(k) and e.get(k).lstrip("-").isdigit():
            e.set(k, str(int(round(int(e.get(k)) * s))))
    for e in new.iter():
        if not isinstance(e.tag, str):
            continue
        n = _local(e)
        if n in ("rPr", "defRPr", "endParaRPr") and e.get("sz"):
            v = max(100, int(round(int(e.get("sz")) * s)))
            e.set("sz", str(v))
            if n == "rPr":
                minimo = v if minimo is None else min(minimo, v)
        elif n == "spcPts":
            esc(e, "val")
        elif n == "pPr" or (n.startswith("lvl") and n.endswith("pPr")):
            esc(e, "marL")
            esc(e, "indent")
        elif n == "bodyPr":
            for k in ("lIns", "tIns", "rIns", "bIns"):
                esc(e, k)
        elif n == "tcPr":
            for k in ("marL", "marR", "marT", "marB"):
                esc(e, k)
        elif n == "tr":
            esc(e, "h")
        elif n == "gridCol":
            esc(e, "w")
    return (minimo / 100.0) if minimo else None


def _renumerar(dst_slide, nuevos):
    """Ids de forma unicos en la diapositiva destino (y conectores al dia)."""
    tree = dst_slide.shapes._spTree
    ids = [int(e.get("id")) for e in tree.iter(qn("p:cNvPr")) if e.get("id", "").isdigit()]
    nxt = max(ids + [1]) + 1
    idmap = {}
    for el in nuevos:
        for c in el.iter(qn("p:cNvPr")):
            idmap[c.get("id")] = str(nxt)
            c.set("id", str(nxt))
            nxt += 1
    for el in nuevos:
        for c in list(el.iter(qn("a:stCxn"), qn("a:endCxn"))):
            if c.get("id") in idmap:
                c.set("id", idmap[c.get("id")])
            else:
                c.getparent().remove(c)


def _insertar(dst_slide, el):
    tree = dst_slide.shapes._spTree
    ext = tree.find(qn("p:extLst"))
    if ext is not None:
        ext.addprevious(el)
    else:
        tree.append(el)


# --------------------------------------------------------------------------- #
#  Generacion
# --------------------------------------------------------------------------- #
def _figura_original(org, n, dst_slide, portada):
    """Pone la imagen mas grande de la portada/separador de origen donde va el
    personaje institucional (misma geometria que pptx_kit._add_personaje)."""
    slide = org.slide(n)
    pics = [e for e in _elementos(slide) if e.tag == qn("p:pic")]
    best = _mejor_figura(slide, pics, org.W, org.H)
    blip = best.find(".//" + qn("a:blip")) if best is not None else None
    rid = blip.get(qn("r:embed")) if blip is not None else None
    if not rid:
        return False
    c = _caja(best, slide)
    ratio = c[2] / float(c[3]) if c[3] else 1.0
    left, alto, base = (2.6, 14.0, 15.3) if portada else (2.8, 12.8, 14.4)
    ancho = alto * ratio
    tope = 16.4 - left               # no invadir el texto de la mitad derecha
    if ancho > tope:
        ancho, alto = tope, tope / ratio
    try:
        blob = slide.part.related_part(rid).blob
        dst_slide.shapes.add_picture(io.BytesIO(blob), Cm(left), Cm(base - alto),
                                     Cm(ancho), Cm(alto))
    except Exception:
        return False
    return True


def _reencuadrar(nuevos, fuentes, org, con_sub):
    """Ubica el bloque de contenido en la zona util, bajo la bandera. Escala en
    bloque solo si no cabe; si cabe (con un margen de tolerancia para excesos
    de diseno menores, p. ej. una caja de texto centrada mas ancha que el
    margen para centrar su texto), no se toca nada: ni posicion ni tamano.
    Devuelve la escala aplicada."""
    top = K.CANVAS_Y + (0.35 if con_sub else 0.0)
    bottom = K.CANVAS_BOTTOM - (0.35 if fuentes else 0.0)
    ax, ay, aw, ah = K.MX * EMU_CM, top * EMU_CM, K.CONTENT_W * EMU_CM, (bottom - top) * EMU_CM
    tol = 0.5 * EMU_CM
    cajas = [(el, _caja(el)) for el in nuevos]
    cajas = [(el, c) for el, c in cajas if c]
    vis = []
    for el, c in cajas:
        b = _aabb(c)
        if b[0] + b[2] > 0 and b[1] + b[3] > 0 and b[0] < org.W and b[1] < org.H:
            vis.append(b)
    escala = 1.0
    if vis:
        bx = min(b[0] for b in vis)
        by = min(b[1] for b in vis)
        bw = max(b[0] + b[2] for b in vis) - bx
        bh = max(b[1] + b[3] for b in vis) - by
        cabe = (bx >= ax - tol and by >= ay - tol
                and bx + bw <= ax + aw + tol and by + bh <= ay + ah + tol)
        if not cabe:
            escala = min(1.0, aw / bw if bw else 1.0, ah / bh if bh else 1.0)
            nbx = min(max(bx, ax), ax + aw - bw * escala)
            nby = min(max(by, ay), ay + ah - bh * escala)
            for el, (x, y, w, h, _) in cajas:
                ncx = nbx + (x + w / 2.0 - bx) * escala
                ncy = nby + (y + h / 2.0 - by) * escala
                _set_caja(el, ncx - w * escala / 2.0, ncy - h * escala / 2.0,
                          w * escala, h * escala)
    for f in fuentes:
        c = _caja(f)
        h = min(c[3], 0.9 * EMU_CM) if c else 0.6 * EMU_CM
        _set_caja(f, ax, (K.CANVAS_BOTTOM - 0.25) * EMU_CM, aw, h)
    return escala


def generar(plan, salida=None):
    salida = salida or plan.get("salida") or "consolidado.pptx"
    norm = plan.get("normalizar_fuentes", True)
    deco = plan.get("conservar_decoracion", False)
    traza = plan.get("trazabilidad_en_notas", False)

    d = K.Deck()
    cp = Copiador(d.prs)
    origenes = {}
    informe = []
    sep_n = 0
    ultimo_titulo = None

    for i, e in enumerate(plan["diapositivas"], 1):
        tipo = e.get("tipo", "contenido")
        org = a = None
        avisos, notas = [], []
        if e.get("archivo"):
            path = os.path.abspath(e["archivo"])
            if path not in origenes:
                origenes[path] = Origen(path)
            org = origenes[path]
            etiqueta = "%s #%d" % (org.nombre, e["n"])
        else:
            etiqueta = "nueva"
            if tipo not in TIPOS_SIN_ARCHIVO:
                raise ValueError("diapositiva %d: sin 'archivo' solo puede ser %s"
                                 % (i, "/".join(TIPOS_SIN_ARCHIVO)))
        if tipo == "omitir":
            informe.append({"i": i, "origen": etiqueta, "tipo": tipo,
                            "avisos": ["omitida por decision del usuario"]})
            continue
        if org is not None:
            a = analizar(org, e["n"])
            src_slide = org.slide(e["n"])
            notas.append(a["notas"])
            if a["pie"]:
                notas.append("Pie original: " + " · ".join(a["pie"]))
            if traza:
                notas.append("[Origen: %s · diapositiva %d]" % (org.nombre, e["n"]))
        if e.get("_nota_extra"):
            notas.append("Datos de la portada original: " + " · ".join(e["_nota_extra"]))

        if tipo in TIPOS_MARCO:
            fig = e.get("figura")
            original = fig == "original" and org is not None
            if tipo == "portada":
                s = d.portada(e.get("kicker") or "", e.get("titulo") or "",
                              e.get("subtitulo") or "", meta=e.get("meta") or [],
                              figura=None if original else (fig or "trio-computador"))
            else:
                if tipo == "separador":
                    sep_n += 1
                    num = e.get("num") or "%02d" % sep_n
                else:
                    num = ""
                s = d.separador(num, e.get("titulo") or "", sub=e.get("sub"),
                                figura="" if original else fig)
            if original and not _figura_original(org, e["n"], s, tipo == "portada"):
                avisos.append("no se pudo reutilizar la imagen original; va sin personaje")
            if a is not None and a["ricos_marco"]:
                avisos.append("tenia tablas/graficas/grupos: revisar si es contenido")
            ultimo_titulo = e.get("titulo") or ultimo_titulo
        elif tipo == "puntos":
            # diapositiva sintetica: puntos que traia un separador saturado,
            # separados aqui para dejarlo limpio (ver _entrada_plan). Se arma
            # con el helper normal de vinetas, no se copian formas.
            titulo = e.get("titulo") or ultimo_titulo or "Puntos a tratar"
            s = d.contenido(titulo, None)
            K.vinetas(s, [str(p) for p in (e.get("puntos") or [])])
            ultimo_titulo = titulo
        else:
            titulo = e.get("titulo")
            if not titulo:
                titulo = ("%s (cont.)" % ultimo_titulo) if ultimo_titulo \
                    else os.path.splitext(org.nombre)[0]
                avisos.append("sin titulo: se uso '%s'" % titulo)
            sub = e.get("sub")
            s = d.contenido(titulo, sub, dark=bool(e.get("anexo")))
            ultimo_titulo = titulo

            def _copiar(lista):
                out = []
                for el in lista:
                    new = cp.copiar_forma(el, src_slide, s, avisos)
                    _materializar_ph(new, org, src_slide, el)
                    _explicitar_texto(new, org, src_slide, el)
                    if norm:
                        _normalizar_fuentes(new)
                    out.append(new)
                return out
            nuevos = _copiar(a["contenido"] + (a["decoracion"] if deco else []))
            fuentes = _copiar(a["fuente"])
            escala = _reencuadrar(nuevos, fuentes, org, bool(sub))
            if escala < 0.999:
                mins = [m for m in (_escalar_texto(el, escala) for el in nuevos) if m]
                avisos.append("contenido reducido al %d %% para caber bajo la bandera"
                              % round(escala * 100))
                if mins and min(mins) < 9:
                    avisos.append("texto minimo %.1f pt: considerar recomponer o partir"
                                  % min(mins))
            _renumerar(s, nuevos + fuentes)
            for el in nuevos + fuentes:
                _insertar(s, el)
            if a["decoracion"] and not deco:
                avisos.append("%d forma(s) decorativa(s) no se pasaron" % len(a["decoracion"]))

        if a is not None:
            if a["animaciones"]:
                avisos.append("animaciones no conservadas")
            if a["oculta"]:
                s._element.set("show", "0")
        notas = [t for t in notas if t and t.strip()]
        if notas:
            s.notes_slide.notes_text_frame.text = "\n\n".join(notas)
        informe.append({"i": i, "origen": etiqueta, "tipo": tipo,
                        "titulo": e.get("titulo"), "avisos": sorted(set(avisos))})

    d.guardar(salida)
    return salida, informe


def _informe_md(informe):
    filas = ["| # | Origen | Tipo | Avisos |", "|---|---|---|---|"]
    for r in informe:
        filas.append("| %d | %s | %s | %s |" % (r["i"], r["origen"], r["tipo"],
                                                "; ".join(r["avisos"]) or "—"))
    return "\n".join(filas)


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description="Consolida presentaciones en la plantilla institucional.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("inventario", help="analiza las presentaciones y escribe el plan JSON")
    a1.add_argument("archivos", nargs="+")
    a1.add_argument("-o", "--plan", default="plan-consolidacion.json")
    a1.add_argument("--portada-consolidada", action="store_true", help=(
        "antepone una portada nueva (en vez de usar la portada del primer archivo) con las "
        "direcciones/areas detectadas en el subtitulo, mejor esfuerzo: revisar en el plan"))
    a1.add_argument("--titulo-consolidado", default="Consolidado de presentaciones",
                    help="titulo de esa portada nueva (con --portada-consolidada)")
    a2 = sub.add_parser("generar", help="genera el PPTX consolidado a partir del plan")
    a2.add_argument("plan")
    a2.add_argument("-o", "--salida")
    args = ap.parse_args(argv)

    if args.cmd == "inventario":
        plan = inventario(args.archivos, portada_consolidada=args.portada_consolidada,
                          titulo_consolidado=args.titulo_consolidado)
        with open(args.plan, "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        print(_resumen(plan))
        print("\nPlan escrito en %s" % args.plan)
    else:
        with open(args.plan, encoding="utf-8") as f:
            plan = json.load(f)
        salida, informe = generar(plan, args.salida)
        print(_informe_md(informe))
        print("\nConsolidado escrito en %s" % salida)


if __name__ == "__main__":
    main()
