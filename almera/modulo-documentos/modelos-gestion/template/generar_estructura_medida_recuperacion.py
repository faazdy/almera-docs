"""Genera el XLSX de carga de nodos para "Medida de recuperación" a partir de task.txt.

Usa como molde la exportación de la plataforma (igual que generar_xlsx_prueba.py):
solo se reescriben sheet1.xml (Nodos_Modelo) y sharedStrings.xml.

Estructura resultante:
  N      Carpeta                 (Módulo / Items)
  N.MM   Documento de la carpeta (Item / Items), versión en Descripción
"""
import re
import sys
import zipfile
from collections import Counter
from xml.sax.saxutils import escape

BASE = r"C:\Users\leonardo.rengifor\Downloads\parametrizacion\modelos-de-gestion"
SRC = BASE + r"\Medida de recuperacion20260923_042506.xlsx"
TASK = BASE + r"\task.txt"
OUT = BASE + r"\Estructura Medida de recuperacion - carga.xlsx"

CLASIF_CARPETA = ("Módulo", "Items")
CLASIF_DOCUMENTO = ("Item", "Items")
ENCABEZADOS = ["Código", "Nombre", "Clasificación", "Clasificación Hijos", "Descripción", "Padre"]

RE_CARPETA = re.compile(r"^(?P<nombre>[^├└│].*?) \((?P<total>\d+)\)\s*$")
RE_DOCUMENTO = re.compile(r"^[├└]── (?P<nombre>.+?)(?: \(V (?P<version>[\d.]+)\))?\s*$")


def leer_arbol():
    texto = open(TASK, encoding="utf-8").read()
    texto = texto.split("ARBOL DOCUMENTOS", 1)[1]
    carpetas = []
    for linea in texto.splitlines():
        if not linea.strip():
            continue
        m = RE_DOCUMENTO.match(linea)
        if m:
            carpetas[-1]["docs"].append((m["nombre"].strip(), m["version"]))
            continue
        m = RE_CARPETA.match(linea)
        if m:
            carpetas.append({"nombre": m["nombre"].strip(), "total": int(m["total"]), "docs": []})
            continue
        sys.exit(f"Línea no reconocida: {linea!r}")
    return carpetas


def construir_nodos(carpetas):
    # (codigo, nombre, clasificacion, clasificacion hijos, descripcion, padre)
    nodos = []
    for i, c in enumerate(carpetas, start=1):
        if len(c["docs"]) != c["total"]:
            sys.exit(f'{c["nombre"]}: dice {c["total"]} documentos y se leyeron {len(c["docs"])}')
        nodos.append((str(i), c["nombre"], *CLASIF_CARPETA, "", ""))
        for j, (nombre, version) in enumerate(c["docs"], start=1):
            desc = f"Versión {version}" if version else ""
            # Dos dígitos: evita que "2.1" y "2.10" choquen si se leen como número
            # y mantiene el orden correcto si se ordenan como texto.
            nodos.append((f"{i}.{j:02d}", nombre, *CLASIF_DOCUMENTO, desc, str(i)))
    return nodos


def escribir_xlsx(nodos):
    with zipfile.ZipFile(SRC) as z:
        originales = {n: z.read(n) for n in z.namelist()}
        orden = z.namelist()

    sst_xml = originales["xl/sharedStrings.xml"].decode("utf-8")
    strings = [re.sub(r"<[^>]+>", "", s) for s in re.findall(r"<si>(.*?)</si>", sst_xml)]
    strings = [s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">") for s in strings]
    indice = {s: k for k, s in enumerate(strings)}

    def idx(texto):
        if texto not in indice:
            indice[texto] = len(strings)
            strings.append(texto)
        return indice[texto]

    cols = "ABCDEF"
    filas = ['<row r="1" spans="1:6">' + "".join(
        f'<c r="{cols[i]}1" s="1" t="s"><v>{idx(h)}</v></c>' for i, h in enumerate(ENCABEZADOS)) + "</row>"]
    for r, nodo in enumerate(nodos, start=2):
        celdas = []
        for i, v in enumerate(nodo):
            s = 3 if i < 2 else 2  # mismos estilos que el export
            ref = f"{cols[i]}{r}"
            celdas.append(f'<c r="{ref}" s="{s}" t="s"><v>{idx(v)}</v></c>' if v else f'<c r="{ref}" s="{s}"/>')
        filas.append(f'<row r="{r}" spans="1:6">{"".join(celdas)}</row>')

    hoja = originales["xl/worksheets/sheet1.xml"].decode("utf-8")
    hoja = re.sub(r"<sheetData>.*</sheetData>", "<sheetData>" + "".join(filas) + "</sheetData>", hoja)
    hoja = hoja.replace('<dimension ref="A1:E6"/>', f'<dimension ref="A1:F{len(nodos) + 1}"/>')
    hoja = re.sub(r'activeCell="\w+" sqref="\w+"', 'activeCell="A2" sqref="A2"', hoja)
    hoja = hoja.replace("</cols>", '<col min="6" max="6" width="12" customWidth="true" style="0"/></cols>')

    sst = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
           '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
           f'uniqueCount="{len(strings)}">'
           + "".join(f"<si><t>{escape(s)}</t></si>" for s in strings) + "</sst>")

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as out:
        for n in orden:
            if n == "xl/worksheets/sheet1.xml":
                out.writestr(n, hoja.encode("utf-8"))
            elif n == "xl/sharedStrings.xml":
                out.writestr(n, sst.encode("utf-8"))
            else:
                out.writestr(n, originales[n])


if __name__ == "__main__":
    carpetas = leer_arbol()
    nodos = construir_nodos(carpetas)
    escribir_xlsx(nodos)

    print(f"OK {OUT}")
    for i, c in enumerate(carpetas, start=1):
        print(f"  {i}  {c['nombre']}  ({len(c['docs'])} docs)")
    print(f"  Total filas: {len(nodos)}")

    for c in carpetas:
        for nombre, n in Counter(d[0] for d in c["docs"]).items():
            if n > 1:
                print(f"  AVISO repetido x{n} en '{c['nombre']}': {nombre}")
    sin_version = [n[1] for n in nodos if n[5] and not n[4]]
    if sin_version:
        print(f"  AVISO documentos sin versión: {sin_version}")
    largos = sorted((n for n in nodos), key=lambda n: -len(n[1]))[:3]
    for n in largos:
        print(f"  Nombre más largo ({len(n[1])} car.): {n[0]} {n[1]}")
