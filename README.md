# Lecturas

Mapa interactivo de lo que voy leyendo: un carril por tipo de lectura, una estación por libro, y dos formas de ordenar el tiempo (cuándo lo leí y cuándo se escribió).

## Cómo está organizado

| Carpeta | Qué hay |
|---|---|
| `libros/` | Un archivo Markdown por libro: datos arriba, reseña y contexto debajo |
| `datos/carriles.yml` | Los carriles del mapa y los hilos de ideas |
| `datos/esquemas.yml` | Los esquemas de los ensayos, por libro |
| `web/plantilla.html` | La página del mapa |
| `scripts/construir.py` | Junta todo y genera la web |

Cada cambio en la rama `main` vuelve a construir y publicar la web.

## Añadir un libro

Crea `libros/nombre-del-libro.md` (minúsculas, sin tildes, con guiones):

```markdown
---
titulo: La montaña mágica
autor: Thomas Mann
estado: leido          # leido o pendiente
leido: 2027-03         # año o año-mes
escrito: 1924          # negativo para antes de Cristo
nota: 4                # de 1 a 5, opcional
carril: literatura     # uno de datos/carriles.yml
ideas: [culpa, dios]   # hilos de datos/carriles.yml, opcional
lengua: alemán
paginas: 936
isbn: '9788435009126'  # para la portada
conexiones:            # opcional
- libro: asi-hablo-zaratustra
  texto: Por qué se relacionan.
---

## Reseña

Lo que me ha parecido.

## Contexto

Nota breve sobre el libro.
```

Otros campos opcionales: `serie`, `releido: true` y `escrito_etiqueta` (por ejemplo `s. VIII a. C.`).

## Probarlo en el ordenador

```
pip install pyyaml
python scripts/construir.py
```

La web queda en `_site/index.html`.

## Créditos

Las reseñas y las notas son mías. Las notas de contexto y los esquemas los ha escrito Claude, una IA. Las portadas vienen de [Open Library](https://openlibrary.org).
