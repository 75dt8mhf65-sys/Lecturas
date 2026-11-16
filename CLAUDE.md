# Mapa de lecturas

Web estática con las lecturas del dueño del repositorio. Idioma del proyecto: español.

## Tarea habitual: añadir o actualizar un libro

1. Crea o edita `libros/<slug>.md` con el formato descrito en `README.md`. El slug va en minúsculas, sin tildes y con guiones.
2. La sección `## Reseña` es la voz del usuario: usa sus palabras, arreglando solo puntuación y erratas. No añadas opiniones que no haya dado ni estrellas que no haya dicho.
3. La sección `## Contexto` la escribe Claude: dos o tres frases con datos comprobables sobre el libro. Si no conoces bien el libro, déjala vacía antes que inventar.
4. Para ensayo, filosofía o divulgación, añade un esquema en `datos/esquemas.yml` con la clave del slug. Tipos de bloque: `chain` (pasos encadenados), `notes` (ideas sueltas) y `pairs` (tabla de dos columnas).
5. Propón `ideas` (hilos) y `conexiones` con otros libros del repositorio. Una conexión debe apoyarse en un hecho o en algo que el usuario haya dicho en una reseña.
6. Ejecuta `python scripts/construir.py`: valida carriles, hilos y conexiones, y falla con un mensaje claro si algo no cuadra.

## Reglas

- La web es pública. No pongas nombres de terceros ni detalles personales que el usuario no haya querido publicar.
- Un carril o un hilo nuevo se añade en `datos/carriles.yml`. Un carril nuevo necesita además su color `--l-<id>` en `web/plantilla.html`, en los tres bloques de tema (claro, oscuro por sistema y oscuro por `data-theme`).
- No edites `_site/`: se genera.
