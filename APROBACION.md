# Mecanismo de aprobación de ZAVE

Cómo una publicación pasa de borrador a programada con publicación automática, solo si el dueño de la marca la aprueba.

## Reglas

1. Nada se publica ni se programa con `autoPublish: true` sin una aprobación explícita de esa publicación, en esa versión.
2. Abrir un correo o un enlace **no** aprueba nada. Los correos no llevan botones de acción.
3. Ningún enlace público autoriza publicaciones. La decisión se toma en una página privada que exige iniciar sesión.
4. Cada aprobación queda registrada: quién, cuándo, qué versión y en qué modo.
5. Si cambia el contenido aprobado (caption, imágenes, fecha, formato), cambia la huella y hace falta una nueva aprobación.
6. No se duplican borradores ni programaciones (ver "Idempotencia").

## Piezas

| Pieza | Qué es |
|---|---|
| Página privada «ZAVE Aprobaciones» | Artifact de claude.ai, legible solo por el dueño. Muestra cada pieza con imágenes, caption, fecha, enlaces y huella. Botones **APROBAR** y **PEDIR CAMBIOS**. Dirección: https://claude.ai/artifact/5fTnRfXadef8nUGBYnAE1N |
| Base de datos de la página | Colecciones `piezas`, `aprobaciones` y `config` (ver abajo). Reglas de acceso: solo `admin` lee y escribe |
| Borrador en Metricool | Creado por el proceso de producción con `draft: true` y `autoPublish: false` |
| Correo | Aviso con enlaces. Sin botones de aprobación |

## Datos

`piezas/{id}`: `titulo`, `formato`, `fechaPublicacion` (ISO UTC), `caption`, `imagenes[]` (`url`, `sha256`, `previewUrl` opcional), `version`, `hash`, `estado`, `esPrueba`, `metricool` (`uuid`, `id`, `plannerUrl`), `metricoolInfo` (JSON completo del post).

Estados: `pendiente` → `aprobacion_enviada` → `programada` → `publicada`; o `cambios_solicitados`; o `error`.

`aprobaciones/{piezaId}__{hash12}`: `decision` (`aprobar` o `cambios`), `comentario`, `byUid`, `byNombre`, `clientAt`, `origen` (`pagina`), `modo` (`DRY_RUN` o `LIVE`), `estadoProceso` (`pendiente`, `procesando`, `procesada`, `simulada`, `error`). El id lleva la huella: una versión nueva genera una aprobación nueva, y una decisión repetida sobre la misma versión no se vuelve a ejecutar.

`config/modo`: `DRY_RUN` o `LIVE`. **Hoy es `DRY_RUN`.** Cambiarlo a `LIVE` requiere orden explícita del dueño.

### Huella

SHA-256 en hexadecimal de `JSON.stringify([caption, imagenes.map(i => i.sha256 || i.url), fechaPublicacion, formato, version])`. La página la recalcula con lo que muestra y **bloquea la aprobación si no coincide con la guardada**.

## Flujo

1. El proceso de producción crea el borrador en Metricool y guarda la pieza en la base (`estado: pendiente`, con `hash`, `metricool.id`, `metricool.uuid` y `metricoolInfo` armado con la **respuesta** de `createScheduledPost`).
2. Llega el aviso por correo con el enlace a la página y al borrador.
3. El dueño abre la página (con su sesión) y elige:
   - **APROBAR**: aparece un panel de confirmación con título, fecha, versión y huella. Al confirmar, la página registra la aprobación y, **solo en modo `LIVE` y con piezas reales**, llama una sola vez a `updateScheduledPost` con `draft: false` y `autoPublish: true`, usando la conexión de Metricool del propio dueño. Guarda el nuevo `id` (el `uuid` no cambia).
   - **PEDIR CAMBIOS**: exige un comentario, no toca Metricool y deja la pieza en `cambios_solicitados`. La versión nueva tendrá otra huella.
4. En modo `DRY_RUN`, aprobar solo registra la decisión y comprueba la conexión con Metricool (`getBrandSettings`, lectura). No escribe nada.
5. Metricool publica a la hora indicada. Después se actualiza el historial.

## Seguridad e idempotencia

- Página privada: solo el dueño la abre. Compartir el enlace no da acceso.
- Una decisión por versión: `acquire` sobre el documento de aprobación y verificación de que no exista antes de escribir.
- Una sola llamada a Metricool por aprobación. Si falla, la página **no reintenta sola**: marca `error` y avisa. Un estado `procesando` que quedó colgado exige revisar Metricool a mano antes de repetir.
- Se exige que la fecha de publicación esté al menos 20 minutos en el futuro.
- Piezas de prueba (`esPrueba: true`) nunca llegan a Metricool, ni en modo `LIVE`.
- **Límite honesto:** Claude escribe en la misma base con los permisos del dueño, así que no existe una barrera técnica que le impida escribir un documento de aprobación. Las defensas son: el campo `origen`, la regla de que Claude **nunca** escribe en `aprobaciones` ni cambia `config/modo`, el registro de auditoría y que la programación la ejecuta la página con la conexión del dueño.

## Cambios después de aprobar

- Cualquier cambio de contenido genera una versión nueva (`version + 1`) y una huella nueva.
- Si la pieza ya estaba programada, se la devuelve a borrador (`draft: true`, `autoPublish: false`) antes de editarla y se vuelve a pedir aprobación. La aprobación anterior queda en el historial y no vale para la versión nueva.

## Correos

- Se envían por las notificaciones por correo de las tareas programadas de Claude Code (llegan a la casilla de la cuenta). Contienen el resumen de la corrida, enlaces a la página de aprobación, al borrador y a las imágenes públicas.
- No contienen claves, tokens ni enlaces que aprueben algo.
- Gmail no está conectado como conector. Si se conecta y permite enviar, puede reemplazar este canal sin cambiar el resto del flujo.

## Estado de la verificación (2026-10-15)

| Punto | Estado |
|---|---|
| Página privada publicada, con base de datos y reglas de acceso | Verificado |
| Una sesión disparada sola puede leer y escribir la base de datos | Verificado (prueba con una tarea de un solo uso) |
| Una tarea programada creada desde una sesión **no** recibe el conector de Metricool | Verificado (por eso la programación la hace la página, no una tarea) |
| Una sesión creada desde otra sesión sí tiene Metricool, ArtifactData y `add_repo` | Verificado (lectura) |
| Una sesión autónoma clona el repositorio y arma la propuesta semanal, pero no puede empujar ramas (403) | Verificado: la propuesta debe viajar en el correo |
| La página llama a Metricool con la conexión del dueño (botón «Probar conexión», lectura) | **Pendiente: requiere un clic y aceptar el permiso** |
| Aprobar en modo `DRY_RUN` sobre la pieza de prueba | **Pendiente: requiere un clic** |
| `updateScheduledPost` convierte un borrador en programado con `autoPublish: true` | **Sin verificar** |
| Metricool publica el carrusel automáticamente en @zave_ar | **Sin verificar** |
| Llegada del correo de notificación a la casilla | **Pendiente de confirmación del dueño** |
