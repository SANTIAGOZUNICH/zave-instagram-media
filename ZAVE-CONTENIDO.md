# ZAVE — Guía de contenido para Instagram

Documento maestro. Toda sesión (humana o automática) que prepare contenido para @zave_ar **debe leerlo completo antes de proponer o generar nada**.

## 1. Marca

| Dato | Valor |
|---|---|
| Marca | ZAVE |
| Instagram | @zave_ar |
| Web | zave.com.ar |
| Slogan | *Una nueva forma de verte bien.* |
| Producto principal | Crema Facial Hidratante Anti-Age con ácido hialurónico y vitamina C, 50 g, para todo tipo de piel |
| Metricool | Marca "Zave", blogId `7410898`, zona horaria `America/Argentina/Buenos_Aires` |
| Hosting de imágenes | https://zave-instagram-media.vercel.app (Vercel, desde este repo) |

## 2. Tono y voz

- Español argentino natural (voseo: "descubrí", "deslizá", "conocé"), profesional y cálido. Sin jerga forzada ni modismos exagerados.
- Frases cortas, claras, sin sonar a publicidad repetitiva. Mejor una pregunta que una consigna.
- Emojis: máximo 2 o 3 por caption, sobrios (✨ 🧡). Nunca en las imágenes.
- Cierre de marca habitual: *Una nueva forma de verte bien.*
- Hashtags: 5 a 8 al final. Base fija: `#ZAVE #SkincareArgentina #CuidadoFacial`. El resto varía según el tema.
- Prioridad: generar curiosidad, confianza y ganas de conocer el producto. Educar antes que vender.

## 3. Reglas de contenido y restricciones (obligatorias)

1. **No inventar resultados clínicos** ni porcentajes, estudios, "comprobado", "elimina arrugas", "antes y después", ni plazos de resultados.
2. **Claims permitidos**, solo los que figuran en el envase real: *Piel hidratada, luminosa y de aspecto más joven*; *Ácido hialurónico + vitamina C*; *Todo tipo de piel*; *50 g*. Cualquier otro claim requiere aprobación escrita de la marca.
3. No hacer promesas médicas ni dermatológicas. No comparar con otras marcas. No hablar de precios, promociones ni stock salvo pedido explícito.
4. No usar personas reales identificables ni celebridades. Las personas generadas deben verse naturales, diversas en edad y tono de piel, con piel realista (sin retoque plástico).
5. **Packaging:** el envase solo se muestra si hay una referencia visual fiable (ver §6). Si no la hay, **no se inventa**: se usa una composición sin envase (ingredientes, texturas, personas, texto).
6. No repetir la misma foto, encuadre ni composición en dos publicaciones consecutivas (ver `CONTENIDO-HISTORIAL.md`).
7. Nada se publica automáticamente. Todo queda como borrador en Metricool (`draft: true`, `autoPublish: false`).

## 4. Identidad visual

Referencia aprobada: `instagram/2026-10-19-carrusel-01/` (5 imágenes). **No se modifica nunca.**

- **Estilo:** premium, minimalista, moderno, editorial. Mucho aire, una sola idea por imagen.
- **Paleta:**
  - Naranja ZAVE `#E25C12` (acento, medido sobre el carrusel aprobado)
  - Negro cálido `#16110E` (texto principal)
  - Marfil / blanco cálido `#FBF7F2` a `#F3E9DF` (fondos)
  - Durazno suave para sombras y luz cálida
- **Tipografía de los textos:** serif editorial tipo **Playfair Display** (Bold/SemiBold). Titular en negro con **una frase clave en naranja**. Interlineado ajustado, alineado a la izquierda.
- **Texto sobre imagen:** margen mínimo 64 px, hasta 3 o 4 líneas, tamaño de titular aprox. 64 a 72 px en 1080 px de ancho, contraste mínimo 4.5:1 contra el fondo. El texto nunca tapa rostros ni el envase.
- **Fotografía:** realista, luz profesional natural y cálida, profundidad de campo suave, piel con textura natural (poros, imperfecciones leves). Sin aspecto de ilustración 3D ni de stock genérico.
- **Línea facial:** acentos naranjas (naranjas cortados, geles, luz cálida).
- **Cierre de carruseles:** la última imagen conecta con el producto y la marca (como la 05 de la referencia).

### Formatos

| Formato | Medidas | Observaciones |
|---|---|---|
| Carrusel | 1080 × 1350 px (4:5), PNG | 4 a 5 imágenes. Portada que frene el scroll |
| Publicación editorial individual | 1080 × 1350 px (4:5), PNG | Una idea, una frase |
| Historia | 1080 × 1920 px (9:16), PNG | Dejar libres los 250 px superiores y los 340 px inferiores (interfaz de Instagram) |

## 5. Productos

| Producto | Estado | Referencia visual |
|---|---|---|
| Crema Facial Hidratante Anti-Age (ácido hialurónico + vitamina C), 50 g | Activo, principal | Tubo blanco con tapa gris, logotipo ZAVE negro, subrayado y "Z" naranja. Textos del envase: "CREMA FACIAL HIDRATANTE ANTI-AGE", "ÁCIDO HIALURÓNICO + VITAMINA C", "PIEL HIDRATADA, LUMINOSA Y DE ASPECTO MÁS JOVEN", "TODO TIPO DE PIEL", "50 g". Visible en `instagram/2026-10-19-carrusel-01/05-producto-zave.png` |
| Otros productos ZAVE | Sin documentar | **Pendiente:** el dueño de la marca debe indicar qué otros productos existen y aportar fotos. Hasta entonces, no se crea contenido sobre ellos |

## 6. Referencias de packaging

- Carpeta: `referencias/packaging/`. Solo fotos reales del producto (fondo limpio, varios ángulos) cargadas por la marca.
- **Estado actual: vacía.** La única representación del envase disponible es la imagen 05 del carrusel aprobado. Sirve como referencia provisoria para la crema de 50 g, pero conviene que la marca confirme que coincide con el envase real o aporte fotos.
- Regla: si la publicación necesita el envase y no hay referencia fiable para ese producto o ángulo, **no se genera**. Se cambia la idea o se pide la foto al dueño de la marca.
- Al generar con Gemini con el envase, se pasa la foto de referencia como imagen de entrada y luego se compara visualmente (logo, textos, colores, proporciones, tapa). Si hay diferencias, se descarta.

## 7. Calidad mínima antes de enviar a revisión

- Dimensiones exactas, PNG válido, peso menor a 8 MB.
- Texto 100 % legible y sin errores ortográficos (tildes, ¿ ?, ñ).
- Sin deformaciones en manos, dedos, ojos, dientes ni texto generado por la IA dentro de la foto.
- Envase fiel al real o ausente.
- Coherencia con la referencia aprobada (paleta, tipografía, composición).
- Checklist completo en `PROCEDIMIENTO-CONTENIDO.md`.

## 8. Instrucciones para quien ejecute el proceso (persona o IA)

1. Leer este archivo, `CONTENIDO-HISTORIAL.md`, `CALENDARIO-EDITORIAL.md` y `PROCEDIMIENTO-CONTENIDO.md`.
2. Seguir el procedimiento paso a paso, respetando las **puertas de aprobación**.
3. No guardar claves ni tokens en el repo. Usar solo secretos del entorno.
4. Si falta información (referencia de packaging, claim dudoso, dato de producto), **detenerse y preguntar**. No improvisar.
5. Registrar todo en `CONTENIDO-HISTORIAL.md` y en el manifiesto de cada pieza.
