# zave-instagram-media

Imágenes y sistema de producción de contenido de Instagram para **ZAVE** (@zave_ar). Las imágenes de `instagram/` se publican con Vercel en https://zave-instagram-media.vercel.app para que Metricool pueda descargarlas.

## Documentos

| Archivo | Para qué sirve |
|---|---|
| `ZAVE-CONTENIDO.md` | Identidad de marca, tono, productos, criterios de diseño y restricciones |
| `CONTENIDO-HISTORIAL.md` | Registro de ideas, publicaciones, fechas, formatos y estados |
| `PROCEDIMIENTO-CONTENIDO.md` | Flujo reproducible: proponer, generar, revisar, alojar y crear borradores |
| `APROBACION.md` | Mecanismo de aprobación: página privada, reglas de seguridad y estado de la verificación |
| `CALENDARIO-EDITORIAL.md` | Esquema semanal y reglas de rotación |

## Estructura de carpetas

```
instagram/                         ← lo único que se publica en Vercel
  AAAA-MM-DD-<formato>-NN/         ← carpeta de una pieza; la fecha es la de publicación
    NN-<slug>.png
manifiestos/AAAA-MM-DD-<formato>-NN.json   ← datos de la pieza: caption, imágenes, hashes, IDs
referencias/packaging/             ← fotos reales del envase (cargadas por la marca)
plantillas/                        ← plantillas (manifiesto, composición de texto)
```

`manifiestos/`, `referencias/`, `plantillas/` y los `.md` están en `.vercelignore`: **no se sirven públicamente**.

## Sistema de nombres

- **Carpeta:** `AAAA-MM-DD-<formato>-NN`
  - `AAAA-MM-DD`: fecha de publicación prevista.
  - `<formato>`: `carrusel`, `post` o `historia`.
  - `NN`: número correlativo del formato en esa fecha (`01`, `02`, ...).
  - Ejemplos: `2026-10-19-carrusel-01`, `2026-10-21-post-01`, `2026-10-23-historia-02`.
- **Archivo:** `NN-<slug>.png`, con `NN` según el orden de las imágenes (`01`, `02`, ...). El slug va en minúsculas, sin tildes ni espacios, con guiones (`01-portada.png`, `05-producto-zave.png`).
- **Manifiesto:** mismo nombre que la carpeta, con extensión `.json`.
- **Ramas de trabajo:** `contenido/AAAA-Wnn` (una por semana).
- Las URLs son estables e inmutables: https://zave-instagram-media.vercel.app/instagram/<carpeta>/<archivo>.png. **Nunca se reemplaza un archivo ya publicado.** Si hay que corregirlo, se crea otra carpeta con el número siguiente.

## Seguridad

- Sin claves ni tokens en el repo. Los secretos viven solo en el entorno de ejecución.
- Nada se publica automáticamente: borradores con `draft: true` y `autoPublish: false`.
