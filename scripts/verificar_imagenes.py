#!/usr/bin/env python3
"""Verifica las imágenes de una pieza (solo lectura, sin gastos ni secretos).

Uso:
  python3 -I scripts/verificar_imagenes.py manifiestos/AAAA-MM-DD-formato-NN.json [--local-only]

Comprueba, por cada imagen del manifiesto:
  - archivo local: PNG válido (firma, IHDR primero, IEND último, CRC), dimensiones esperadas,
    peso menor a 8 MB, SHA-256 igual al del manifiesto (si está cargado);
  - URL pública (sin cookies ni cabeceras de autenticación): HTTP 200, sin redirecciones,
    Content-Type image/png, Content-Length coincidente y mismo SHA-256 que el archivo local.
Sale con código 0 solo si todo es correcto.
"""
import hashlib, json, struct, sys, urllib.request, zlib
from pathlib import Path

MAX_BYTES = 8 * 1024 * 1024
FORMATOS = {"carrusel": (1080, 1350), "post": (1080, 1350), "historia": (1080, 1920)}


class SinRedireccion(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def png_valido(datos):
    if datos[:8] != b"\x89PNG\r\n\x1a\n":
        return None, "firma PNG inválida"
    i, tipos = 8, []
    while i < len(datos):
        if i + 12 > len(datos):
            return None, "archivo truncado"
        largo, = struct.unpack(">I", datos[i:i + 4])
        tipo, cuerpo = datos[i + 4:i + 8], datos[i + 8:i + 8 + largo]
        crc, = struct.unpack(">I", datos[i + 8 + largo:i + 12 + largo])
        if zlib.crc32(tipo + cuerpo) & 0xFFFFFFFF != crc:
            return None, f"CRC inválido en {tipo!r}"
        tipos.append(tipo)
        i += 12 + largo
    if tipos[0] != b"IHDR" or tipos[-1] != b"IEND":
        return None, "faltan IHDR o IEND"
    return struct.unpack(">II", datos[16:24]), None


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    ruta = Path(sys.argv[1])
    solo_local = "--local-only" in sys.argv
    m = json.loads(ruta.read_text(encoding="utf-8"))
    raiz = ruta.resolve().parent.parent
    esperado = FORMATOS[m["formato"]]
    abre = urllib.request.build_opener(SinRedireccion)
    errores = []
    for img in sorted(m["imagenes"], key=lambda x: x["orden"]):
        etiqueta = f'{img["orden"]:02d} {img["archivo"]}'
        local = raiz / "instagram" / m["id"] / img["archivo"]
        if not local.exists():
            errores.append(f"{etiqueta}: no existe {local}")
            continue
        datos = local.read_bytes()
        sha = hashlib.sha256(datos).hexdigest()
        dim, err = png_valido(datos)
        if err:
            errores.append(f"{etiqueta}: {err}")
        elif dim != esperado:
            errores.append(f"{etiqueta}: dimensiones {dim}, se esperaba {esperado}")
        if len(datos) > MAX_BYTES:
            errores.append(f"{etiqueta}: pesa más de 8 MB")
        if img.get("sha256") and img["sha256"] != sha:
            errores.append(f"{etiqueta}: SHA-256 distinto al del manifiesto")
        estado = f"local OK {dim} {len(datos)} B" if not err else "local ERROR"
        if not solo_local:
            try:
                r = abre.open(urllib.request.Request(img["url"], headers={"User-Agent": "zave-verificador"}), timeout=60)
                cuerpo = r.read()
                ct = r.headers.get("Content-Type", "")
                if r.status != 200:
                    errores.append(f"{etiqueta}: HTTP {r.status}")
                if ct.split(";")[0].strip() != "image/png":
                    errores.append(f"{etiqueta}: Content-Type {ct!r}")
                cl = r.headers.get("Content-Length")
                if cl and int(cl) != len(cuerpo):
                    errores.append(f"{etiqueta}: Content-Length {cl} != {len(cuerpo)} bytes recibidos")
                if hashlib.sha256(cuerpo).hexdigest() != sha:
                    errores.append(f"{etiqueta}: la URL sirve un archivo distinto al del repo")
                estado += f" | URL HTTP {r.status} {ct}"
            except Exception as e:
                errores.append(f"{etiqueta}: error de red o redirección ({e})")
                estado += " | URL ERROR"
        print(etiqueta, estado)
    if errores:
        print("\nFALLÓ:")
        print("\n".join(" - " + e for e in errores))
        sys.exit(1)
    print(f"\nOK: {len(m['imagenes'])} imágenes verificadas")


if __name__ == "__main__":
    main()
