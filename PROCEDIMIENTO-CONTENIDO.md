# Procedimiento de producción de contenido ZAVE

Flujo reproducible, de la idea al borrador en Metricool. Lo puede ejecutar una persona o una sesión de Claude Code. Antes de empezar, leer `ZAVE-CONTENIDO.md`.

## Principios

1. **Nunca se publica en Instagram.** Metricool siempre con `draft: true` y `autoPublish: false`. La marca revisa el borrador y publica a mano.
2. **Puertas de aprobación.** Hay tres puntos de parada (P1, P2, P3) donde se espera confirmación humana. Cada ejecución indica en qué modo corre (ver "Modos de ejecución").
3. **Una pieza = un manifiesto.** `manifiestos/<id>.json` es la fuente de verdad de la pieza (caption, imágenes, hashes, ID de Metricool, estado).
4. **Idempotencia.** Ejecutar dos veces el mismo proceso no duplica borradores (ver paso 8).
5. **Lo aprobado es inmutable.** No se modifica ni se reemplaza ningún archivo ya publicado en `instagram/`. Las correcciones van en una carpeta nueva.
6. **Sin secretos en el repo.** Gemini, GitHub y Metricool se usan desde el entorno de ejecución.

## Modos de ejecución

| Modo | Qué hace | Gasto |
|---|---|---|
| `propuesta` (por defecto) | Pasos 0 a 2: consulta el historial y deja el calendario propuesto. Se detiene en P1 | Ninguno |
| `generar` | Pasos 3 a 7 sobre piezas ya aprobadas (P1). Se detiene en P2 | Gemini |
| `borradores` | Pasos 8 y 9 sobre piezas aprobadas (P2) | Ninguno |
| `completo` | Pasos 0 a 9 sin detenerse en P1 ni en P2. **Solo si el dueño de la marca lo activa explícitamente**; igual termina en borrador | Gemini |

Hasta que el dueño apruebe el sistema, ninguna ejecución genera imágenes ni crea borradores.

## Flujo paso a paso

### Paso 0 — Preparación
- Rama de trabajo `contenido/AAAA-Wnn`, creada desde `main` actualizado.
- Leer `ZAVE-CONTENIDO.md`, `CONTENIDO-HISTORIAL.md`, `CALENDARIO-EDITORIAL.md`.
- Confirmar que las herramientas están disponibles (Metricool, GitHub, acceso a Gemini). Si falta alguna, detenerse y avisar.

### Paso 1 — Consultar el historial y evitar repeticiones
- Listar temas, titulares, ingredientes protagonistas y composiciones de las últimas 8 semanas.
- Descartar cualquier idea que repita tema, titular o composición.
- Verificar el balance de pilares y que no haya más de 1 pieza de producto cada 2 de otros pilares.

### Paso 2 — Proponer el calendario editorial (puerta P1)
- Armar la propuesta semanal según `CALENDARIO-EDITORIAL.md` (2 carruseles, 1 publicación, 4 historias).
- Por pieza: fecha y hora, formato, pilar, titular, mensaje por imagen, caption borrador, hashtags, si necesita envase y si hay referencia fiable.
- Guardar la propuesta en `propuestas/AAAA-Wnn.md` y registrar cada pieza en `CONTENIDO-HISTORIAL.md` con estado `Propuesta`. Crear un manifiesto por pieza desde `plantillas/manifiesto.json`.
- **P1: esperar la aprobación del calendario**, pieza por pieza. Las no aprobadas pasan a `Descartada`.

### Paso 3 — Generar las imágenes base con Gemini (Nano Banana Pro)
- Modelo: Nano Banana Pro (Gemini 3 Pro Image). Confirmar el identificador vigente del modelo en la documentación de Google antes de la primera ejecución (hoy `gemini-3-pro-image-preview`).
- Llamada por API REST a `generativelanguage.googleapis.com`. La clave se inyecta desde el entorno; **no se escribe en archivos, logs ni en el repo**.
- Prompt por imagen: describir escena, luz, encuadre y paleta de `ZAVE-CONTENIDO.md`, y **dejar zonas libres para el texto**. Pedir explícitamente *sin texto, sin logotipos, sin marcas de agua*. El texto se compone después (paso 4).
- Las imágenes con envase solo se generan si hay referencia fiable (`referencias/packaging/` o la imagen 05 aprobada). Se pasa la referencia como imagen de entrada y se pide conservar el diseño exacto del envase.
- Si el envase generado difiere del real (logo, textos, colores, proporciones, tapa), se descarta. No se publica un envase inventado.
- Guardar los originales en `trabajo/AAAA-MM-DD-formato-NN/base/` (ignorado por git y por Vercel).
- Registrar prompts y modelo en el manifiesto. Presupuesto: máximo 2 intentos por imagen salvo orden contraria. Se anota la cantidad de imágenes generadas para controlar el costo.

### Paso 4 — Componer los textos legibles
- Los textos **nunca los dibuja la IA**: se componen con HTML/CSS renderizado en Chromium (Playwright) o con Pillow, sobre la imagen base.
- Tipografía Playfair Display (SemiBold/Bold), titular negro `#16110E` con la frase clave en naranja `#E25C12`, alineado a la izquierda, margen mínimo 64 px, hasta 4 líneas.
- Verificar contraste mínimo 4.5:1 entre texto y fondo. Si no alcanza, mover el bloque de texto o aplicar un degradado suave marfil detrás.
- Exportar PNG: 1080 × 1350 (carrusel, post) o 1080 × 1920 (historia). Nombrar `NN-<slug>.png` según `README.md`.

### Paso 5 — Verificar resolución, dimensiones y calidad visual
- Automático: `python3 -I scripts/verificar_imagenes.py manifiestos/<id>.json --local-only` (firma PNG, CRC, dimensiones, peso, hash).
- Visual, imagen por imagen (checklist):
  - [ ] Texto legible, sin cortes ni errores ortográficos (tildes, ¿ ?, ñ).
  - [ ] Texto fuera de rostros y del envase; margen seguro respetado (historias: 250 px arriba, 340 px abajo).
  - [ ] Manos, dedos, ojos y dientes sin deformaciones; piel natural.
  - [ ] Envase fiel al real, o ausente.
  - [ ] Sin logotipos ni textos espurios generados por la IA.
  - [ ] Coherente con la paleta y el estilo de la referencia aprobada.
  - [ ] No repite una composición reciente.
- Cualquier fallo: regenerar esa imagen (respetando el máximo de intentos) o detenerse y avisar.

### Paso 6 — Revisión humana (puerta P2)
- Presentar las imágenes finales y el caption al dueño de la marca (en la sesión y/o en un PR).
- **P2: esperar la aprobación explícita** antes de alojar y crear borradores. Se registran los cambios pedidos.
- Completar `sha256` de cada imagen en el manifiesto y pasar la pieza a `Aprobada`.

### Paso 7 — Subir a GitHub y alojar en Vercel
- Copiar las imágenes aprobadas a `instagram/<id>/`. Nunca sobrescribir archivos existentes: si la carpeta ya existe en `main`, usar el siguiente número.
- Commit en `contenido/AAAA-Wnn` y push (con reintentos con espera creciente si falla la red).
- Alojar: el sitio de Vercel se despliega desde `main`. Opciones: abrir un PR y que el dueño lo fusione, o fusionar con su autorización. **No se fusiona ni se empuja a `main` sin autorización.**
- Esperar el despliegue de Vercel y verificar con `python3 -I scripts/verificar_imagenes.py manifiestos/<id>.json`, que comprueba, sin cookies ni tokens:
  - [ ] HTTP 200 en todas las URLs, sin redirecciones ni pantalla de autenticación.
  - [ ] `Content-Type: image/png`.
  - [ ] `Content-Length` coincide con los bytes descargados.
  - [ ] El archivo servido tiene el mismo SHA-256 que el del repo.
- Si algo falla, **no se crean borradores**. Se avisa el problema.

### Paso 8 — Crear el borrador en Metricool (con idempotencia)
Metricool: marca Zave, `blogId 7410898`, solo `instagram` (@zave_ar).

**Importante (observado el 2026-10-14, no confirmado en la documentación de Metricool):** `getScheduledPosts` parece **no devolver los borradores**. La consulta del 19/10/2026 devolvió una lista vacía mientras el borrador `396049475` existía; luego, ya publicada, la misma publicación apareció con otro `id` (`396085138`) y el mismo `uuid`. El `id` cambia cuando Metricool modifica la publicación; el `uuid` no: **la clave estable es el uuid**. Por eso la idempotencia se apoya en el manifiesto del repo, no en Metricool.

Secuencia obligatoria:
1. Leer el manifiesto. Si `metricool.postId` ya tiene valor o `estado` es `Borrador Metricool`, **no crear nada**: ir al paso 9 para verificar el existente.
2. Si `estado` es `Creando borrador` (un intento anterior se cortó antes de guardar el resultado), **detenerse y avisar**. El borrador pudo haberse creado. Se comprueba a mano en el planner de Metricool antes de reintentar.
3. Marcar `estado = "Creando borrador"` en el manifiesto y empujarlo al repo **antes** de llamar a Metricool.
4. Llamar a `createScheduledPost` **una sola vez** con:
   - `blogId: 7410898`, `date` en formato ISO con offset `-03:00`.
   - `info`: `draft: true`, `autoPublish: false`, `providers: [{"network":"instagram"}]`, `media` con las URLs públicas en orden, `text` con el caption exacto, `publicationDate: {dateTime, timezone: "America/Argentina/Buenos_Aires"}`, `instagramData: {"type":"POST"}`, `descendants: []`, `firstCommentText: ""`, `shortener: false`.
   - Historias: `instagramData.type = "STORY"` y sin `text`.
5. Guardar de inmediato `postId`, `uuid`, `plannerUrl` y `estado = "Borrador Metricool"` en el manifiesto. Hacer commit y push.
6. **Un error de Metricool no se reintenta a ciegas**: se informa el error textual y se espera instrucción.

### Paso 9 — Verificar el borrador
La respuesta de creación incluye las imágenes que Metricool guardó. Comprobar:
- [ ] `draft: true` y `autoPublish: false` (también en `instagramData`).
- [ ] Único proveedor: `instagram`, estado `PENDING`.
- [ ] Cantidad de imágenes igual a la del manifiesto, en el mismo orden.
- [ ] Cada URL de `static.metricool.com` devuelve 200 y `image/png`, y su **SHA-256 coincide con el de la imagen del repo** en la misma posición (comprobado con el borrador de referencia: los 5 hashes coinciden).
- [ ] Texto del caption idéntico al aprobado.
- [ ] Fecha y zona horaria correctas.
- Marcar `metricool.verificado = true`, actualizar `CONTENIDO-HISTORIAL.md` y entregar el informe: ID, estado, imágenes y orden, fecha, autoPublish desactivado, advertencias.

## Informe final de cada ejecución

ID de Metricool, estado, cantidad y orden de imágenes, fecha registrada, confirmación de `autoPublish: false`, advertencias o errores, cantidad de imágenes generadas con Gemini y costo estimado.

## Ejecución programada

Estado al 2026-10-15. **La automatización de extremo a extremo todavía no está comprobada.** Solo está verificado lo que se indica en `APROBACION.md`.

| Etapa | Cómo se ejecuta | Estado |
|---|---|---|
| Planificación semanal | Tarea programada de Claude Code, domingos 18:00 (hora de Buenos Aires), sesión nueva, con notificación por correo. Deja `propuestas/AAAA-Wnn.md` en la rama `contenido/AAAA-Wnn` | Ver `CONTENIDO-HISTORIAL.md` y la sesión de configuración |
| Aprobación del calendario y del presupuesto | El dueño, antes de cualquier gasto | Sin automatizar |
| Generación (Gemini), alojamiento y creación del borrador | Sesión de Claude Code con conector de Metricool. Una tarea creada desde una sesión **no** recibe conectores, así que hace falta una sesión persistente creada con ellos, o crear la tarea desde la interfaz de claude.ai | Pendiente de decisión y de aprobación de gasto |
| Aprobación de cada pieza | Página privada (`APROBACION.md`) | Publicada, pendiente de prueba con clic |
| Programación con `autoPublish: true` | La página, con la conexión de Metricool del dueño, solo en modo `LIVE` | Desactivada (`DRY_RUN`) |

Restricciones comprobadas del entorno:
- Una tarea programada creada desde una sesión no puede recibir conectores («connectors no está disponible para esta organización»).
- Las tareas ligadas a una sesión existente no admiten notificaciones por correo.
- El correo de una tarea de sesión nueva es un resumen del resultado final de la corrida.
