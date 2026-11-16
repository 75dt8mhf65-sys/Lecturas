"""Construye el mapa de lecturas.

Lee un archivo Markdown por libro (libros/*.md), los carriles e hilos
(datos/carriles.yml) y los esquemas (datos/esquemas.yml), y genera la web
en _site/index.html a partir de web/plantilla.html.

Uso:  python scripts/construir.py
"""
import json
import pathlib
import re
import sys

import yaml

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ESTADOS = {"leido", "pendiente"}


def leer_libro(ruta):
    texto = ruta.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", texto, re.S)
    if not m:
        raise ValueError("falta la cabecera entre líneas '---'")
    datos = yaml.safe_load(m.group(1)) or {}
    secciones = {}
    actual = None
    for linea in m.group(2).splitlines():
        t = re.match(r"^##\s+(.*)$", linea)
        if t:
            actual = t.group(1).strip().lower()
            secciones[actual] = []
        elif actual:
            secciones[actual].append(linea)
    secciones = {k: "\n".join(v).strip() for k, v in secciones.items()}
    return datos, secciones


def etiqueta_anio(anio):
    if anio is None:
        return None
    return f"{-anio} a. C." if anio < 0 else str(anio)


def main():
    conf = yaml.safe_load((RAIZ / "datos" / "carriles.yml").read_text(encoding="utf-8"))
    esquemas = yaml.safe_load((RAIZ / "datos" / "esquemas.yml").read_text(encoding="utf-8")) or {}
    carriles = {c["id"] for c in conf["carriles"]}
    hilos = {h["id"] for h in conf["hilos"]}

    rutas = sorted((RAIZ / "libros").glob("*.md"))
    ids = {r.stem for r in rutas}
    libros, errores = [], []

    for ruta in rutas:
        try:
            d, s = leer_libro(ruta)
        except Exception as e:  # cabecera mal escrita
            errores.append(f"{ruta.name}: {e}")
            continue

        def mal(msg):
            errores.append(f"{ruta.name}: {msg}")

        for campo in ("titulo", "autor", "carril"):
            if not d.get(campo):
                mal(f"falta '{campo}'")
        estado = d.get("estado", "leido")
        if estado not in ESTADOS:
            mal(f"estado '{estado}' no válido (leido o pendiente)")
        if d.get("carril") and d["carril"] not in carriles:
            mal(f"carril '{d['carril']}' no existe en datos/carriles.yml")
        for h in d.get("ideas") or []:
            if h not in hilos:
                mal(f"hilo '{h}' no existe en datos/carriles.yml")
        leido = str(d["leido"]) if d.get("leido") else None
        if estado == "leido":
            if not leido:
                mal("falta 'leido' (año o año-mes)")
            elif re.fullmatch(r"\d{4}", leido):
                leido += "-06"  # solo el año: se coloca a mitad de año
            elif not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", leido):
                mal(f"'leido: {leido}' debe ser AAAA o AAAA-MM")
        nota = d.get("nota") or 0
        if nota not in (0, 1, 2, 3, 4, 5):
            mal("'nota' debe ir de 1 a 5")
        conexiones = []
        for c in d.get("conexiones") or []:
            if c.get("libro") not in ids:
                mal(f"la conexión apunta a '{c.get('libro')}', que no existe en libros/")
            conexiones.append({"to": c.get("libro"), "text": c.get("texto", "")})

        anio = d.get("escrito")
        libros.append({
            "id": ruta.stem,
            "title": d.get("titulo"),
            "series": d.get("serie"),
            "author": d.get("autor"),
            "year": anio,
            "year_label": str(d["escrito_etiqueta"]) if d.get("escrito_etiqueta") else etiqueta_anio(anio),
            "status": estado,
            "read": leido if estado == "leido" else None,
            "rating": nota,
            "review": s.get("reseña") or None,
            "reread": bool(d.get("releido")),
            "lane": d.get("carril"),
            "ideas": d.get("ideas") or [],
            "lang": d.get("lengua"),
            "context": s.get("contexto") or None,
            "diagram": ruta.stem if ruta.stem in esquemas else None,
            "links": conexiones,
            "isbn": str(d["isbn"]) if d.get("isbn") else None,
            "pages": d.get("paginas"),
        })

    if errores:
        print("No se ha construido la web. Hay que corregir:\n  - " + "\n  - ".join(errores))
        sys.exit(1)

    datos = {"lanes": conf["carriles"], "ideas": conf["hilos"], "diagrams": esquemas, "books": libros}
    plantilla = (RAIZ / "web" / "plantilla.html").read_text(encoding="utf-8")
    js = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    salida = RAIZ / "_site"
    salida.mkdir(exist_ok=True)
    (salida / "index.html").write_text(plantilla.replace("/*DATA*/", js, 1), encoding="utf-8")
    leidos = sum(1 for b in libros if b["status"] == "leido")
    print(f"Web construida: {len(libros)} libros ({leidos} leídos, {len(libros) - leidos} por leer)")


if __name__ == "__main__":
    main()
