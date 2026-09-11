# -*- coding: utf-8 -*-
"""
Ejemplo trabajado en PPTX: replica el deck HTML `ejemplo-gestion-integral.html`
("Informe de Gestion Integral - 2T 2026") usando `pptx_kit`.

Uso:   python ejemplo-gestion-integral-pptx.py [salida.pptx]
Salida por defecto:  ejemplo-gestion-integral.pptx  (junto a este script)

`pptx_kit.py` esta en assets/ (dos niveles arriba de este archivo).

Datos ficticios. Sirve como referencia de que produce cada helper del kit y
como calibracion de densidad (una idea por diapositiva, sin saturar).
"""
import os
import sys

_ASSETS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, _ASSETS)
from pptx_kit import (Deck, kpi_tiles, vinetas, tarjetas, tabla, grafica_barras,
                      grafica_dona, barras_horizontales, kpi_gigante, fuente, G,
                      barra_apilada, etapas, cita)

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "ejemplo-gestion-integral.pptx")

d = Deck()

# 1 - Portada
d.portada("Informe de gestion", "Gestion Integral", "Segundo trimestre de 2026",
          meta=["Talento Humano - Direccion Administrativa y Financiera",
                "1 de septiembre de 2026 - Comite Directivo"])

# 2 - Resumen ejecutivo (fichas KPI)
s = d.contenido("El trimestre avanza en productividad y cierra con utilidad neta",
                "Cifras clave - abril a junio de 2026 - variacion frente a 1T-2026")
kpi_tiles(s, [
    ("Servidores en teletrabajo", "320", "▲ 40 vs. 1T", "Modalidad hibrida", False),
    ("Productividad areas vinculadas", "+12 %", "Meta +8 %", "Metas de proceso cumplidas", False),
    ("Resultado neto 2T", "$31 MM", "▲ 18 % vs. 1T", "Margen neto 2,1 %", False),
    ("Dias de cartera", "58", "▲ 3 dias - meta <= 45", "Rotacion de CxC", True),
])
fuente(s, "Cifras financieras en miles de millones de pesos (MM). Datos ficticios para efectos de demostracion.")

# 3 - Separador 01
d.separador("01", "Talento humano y teletrabajo", figura="trio-computador")

# 4 - Teletrabajo texto (vinetas)
s = d.contenido("El teletrabajo dejo de ser piloto y ya es politica permanente",
                "Estado del programa - primer semestre de 2026")
vinetas(s, [
    "320 servidores vinculados en modalidad hibrida",
    "Cobertura en las cuatro direcciones misionales",
    "Marco normativo interno aprobado en marzo de 2026",
    "Acompanamiento de Talento Humano y de Seguridad y Salud",
])

# 5 - Solicitudes por mes (barras 1 serie, marzo resaltado)
s = d.contenido("Las solicitudes de ingreso al programa se concentraron en marzo",
                "Solicitudes aprobadas por mes - primer semestre de 2026")
grafica_barras(s, ["Ene", "Feb", "Mar", "Abr", "May", "Jun"],
               [("Solicitudes", (18, 26, 44, 39, 31, 25))], highlight=2)
fuente(s, "183 solicitudes aprobadas en total. Fuente: Talento Humano. Datos ficticios.")

# 6 - Productividad KPI (cifra gigante)
s = d.contenido("La productividad de las areas vinculadas subio 12 %",
                "Cumplimiento de metas de proceso - enero a junio de 2026")
kpi_gigante(s, "+12%",
            "Frente a una meta institucional de +8 %. Medido sobre el promedio de las areas del programa.")

# 7 - Comparacion (2 tarjetas)
s = d.contenido("El cambio se nota en tiempos, en espacio y en costos", "Situacion 2025 frente a 2026")
tarjetas(s, [
    ("Antes - 2025", ["45 minutos promedio de traslado por trayecto",
                      "Dos pisos de sede administrativa en uso",
                      "Picos de ausentismo en temporada de lluvias"], "blanco"),
    ("Despues - 2026", ["Dos dias presenciales a la semana",
                        "Un piso liberado: ahorro de $9 MM al trimestre",
                        "Ausentismo 18 % por debajo del ano anterior"], "inst"),
])

# 8 - Separador 02
d.separador("02", "Resultados financieros", figura="hombre-checklist")

# 9 - Estado de resultados (tabla nativa)
s = d.contenido("Estado de resultados resumido del trimestre", "2T-2026 frente a 2T-2025 - MM de pesos")
tabla(s, ["Concepto", "2T-2026", "2T-2025", "Var. %"], [
    ["Ingresos operacionales", "1.482", "1.394", "+6,3 %"],
    ["Costo medico y prestacion", "1.369", "1.312", "+4,3 %"],
    ["Gastos administrativos", "82", "79", "+3,8 %"],
    ["Resultado operacional", "45", "16", "+181 %"],
    ["Gastos financieros netos", "14", "11", "+27 %"],
    ["Resultado neto", "31", "5", "+520 %"],
], total_rows=(3, 5))
fuente(s, "Cifras ficticias, redondeadas. Var. % sobre valores sin redondear.")

# 10 - Ingresos vs egresos (2 series)
s = d.contenido("Los ingresos superaron a los egresos los tres meses del trimestre",
                "Ingresos y egresos operacionales por mes - MM de pesos")
grafica_barras(s, ["Abril", "Mayo", "Junio"],
               [("Ingresos", (486, 495, 501)), ("Egresos", (472, 481, 484))],
               colors=[G[0], G[2]], legend=True)
fuente(s, "Superavit operacional del trimestre: $45 MM. Fuente: estados financieros internos.")

# 11 - Dona
s = d.contenido("El costo medico concentra 9 de cada 10 pesos de gasto",
                "Composicion del egreso operacional - 2T-2026")
grafica_dona(s, [
    ("Costo medico y prestacion de servicios", 92.4),
    ("Gastos administrativos", 5.5),
    ("Gastos financieros", 1.3),
    ("Otros egresos", 0.8),
], centro=("92,4 %", "costo medico"))
fuente(s, "Gasto administrativo dentro del limite regulatorio (8 %). Datos ficticios.")

# 12 - Separador 03
d.separador("03", "Liquidez, cartera y presupuesto", figura="mujer-checklist")

# 13 - Cartera por edades (barras horizontales)
s = d.contenido("El 80 % de la cartera esta al dia o con menos de 60 dias",
                "Cartera por edades - participacion sobre el saldo total ($214 MM)")
barras_horizontales(s, [
    ("0 a 30 dias", 62), ("31 a 60 dias", 18), ("61 a 90 dias", 9),
    ("91 a 180 dias", 7), ("Mas de 180 dias", 4),
])
fuente(s, "Provision constituida sobre cartera > 180 dias: 85 %. Datos ficticios.")

# 14 - Ejecucion presupuestal
s = d.contenido("La ejecucion de ingresos va sobre lo previsto; inversion, rezagada",
                "Ejecucion presupuestal acumulada a junio - % de lo programado para el semestre")
barras_horizontales(s, [
    ("Ingresos", 96), ("Costos en salud", 95),
    ("Gastos administrativos", 91), ("Plan de inversion", 78),
])
fuente(s, "Rezago de inversion por reprogramacion del plan de infraestructura tecnologica. Datos ficticios.")

# 15 - Composicion del plan de inversion (barra apilada 100% - L06)
s = d.contenido("Infraestructura tecnologica concentra el 58 % del plan de inversion",
                "Plan de inversion 2026 - participacion sobre $28.000 MM programados")
barra_apilada(s, [
    ("Infraestructura tecnologica", 58, "$16.240 MM", "Data center + red"),
    ("Dotacion asistencial", 22, "$6.160 MM", None),
    ("Obra fisica", 13, "$3.640 MM", None),
    ("Otros frentes", 7, "$1.960 MM", None),
], total=("Total plan de inversion", "$28.000 MM"))
fuente(s, "Cifras ficticias en millones de pesos (MM). Fuente: tablero presupuestal.")

# 16 - Ruta del plan de saneamiento de cartera (etapas - L08)
s = d.contenido("El plan de saneamiento de cartera > 90 dias va en la etapa 2 de 5",
                "Cronograma de recuperacion - horizonte a diciembre de 2026")
etapas(s, [
    ("Jun 2026", "Depuracion", "Conciliacion de saldos con 8 EPS", "Cartera", True),
    ("Ago 2026", "Acuerdos", "Firma de acuerdos de pago con deudores clave", "Cartera + Juridica", True),
    ("Oct 2026", "Cobro coactivo", "Traslado de cartera sin acuerdo", "Juridica", False),
    ("Nov 2026", "Provision", "Ajuste de la provision segun recuperacion real", "Contabilidad", False),
    ("Dic 2026", "Cierre", "Informe final al Comite", "Financiera", False),
], hito="La firma de acuerdos de agosto define cuanta cartera pasa a cobro coactivo")
fuente(s, "Saldo objetivo: $41 MM de cartera > 90 dias. Datos ficticios.")

# 17 - Separador 04
d.separador("04", "Conclusiones y decisiones", figura="trio-sello")

# 18 - Voceria de la direccion (cita - L11)
s = d.contenido("La direccion respalda las tres decisiones que se llevan al Comite",
                "Cierre de la presentacion de gestion - 2T-2026")
cita(s,
     "El trimestre confirma que el modelo hibrido es sostenible: cumplimos metas de "
     "productividad, cerramos con utilidad y liberamos costo fijo.",
     "Ana Maria Rojas", "Directora Administrativa y Financiera",
     chips=[("Utilidad neta 2T", "$31 MM"), ("Ahorro por sede", "$9 MM/trim")])
fuente(s, "Vocera: Direccion Administrativa y Financiera. Datos ficticios.")

# 19 - Cierre (2 tarjetas)
s = d.contenido("Conclusiones y decisiones solicitadas", "Para el Comite Directivo")
tarjetas(s, [
    ("Conclusiones", ["El teletrabajo cumple sus metas de productividad y ahorro.",
                      "Segundo trimestre consecutivo con utilidad neta.",
                      "Siniestralidad a la baja, pero aun sobre el 92 %.",
                      "Cartera > 90 dias y rezago de inversion: los focos."], "blanco"),
    ("Decisiones solicitadas", ["Aprobar la ampliacion del teletrabajo a areas de apoyo.",
                                "Aprobar el plan de saneamiento de cartera > 90 dias.",
                                "Autorizar la reprogramacion del plan de inversion.",
                                "Ratificar la meta de siniestralidad de 91 % para el 3T."], "inst"),
])

# 20 - Anexo
s = d.contenido("Anexo - Supuestos y fuentes", "Base de las cifras presentadas", dark=True)
from pptx_kit import caja_texto
caja_texto(s, "", [
    "Todas las cifras son ficticias y se usan solo para demostrar la plantilla.",
    "Productividad = % de metas de proceso cumplidas, promedio de areas vinculadas al teletrabajo.",
    "Valores financieros en miles de millones de pesos (MM), salvo indicacion distinta.",
    "Siniestralidad = costo medico y prestacion / ingresos operacionales.",
    "Dias de cartera = saldo de CxC / ingresos x 90.",
    "Ejecucion presupuestal contra el programado del semestre, corte 30 de junio de 2026.",
    "Fuentes: Talento Humano, estados financieros internos y tablero presupuestal.",
])

path = d.guardar(OUT)
print("OK ->", path, "|", round(os.path.getsize(path) / 1e6, 1), "MB |",
      len(d.prs.slides._sldIdLst), "slides")
