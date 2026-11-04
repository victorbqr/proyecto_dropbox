import hashlib
from pathlib import Path

DROPBOX_BLOCK_SIZE = 4 * 1024 * 1024  # 4 MB exactos (4,194,304 bytes)

def calcular_content_hash_dropbox(ruta_archivo: str | Path) -> str:
    hashes_bloques = bytearray()
    with open(ruta_archivo, "rb") as archivo:
        while True:
            bloque = archivo.read(DROPBOX_BLOCK_SIZE)
            if not bloque:
                break
            hashes_bloques.extend(hashlib.sha256(bloque).digest())
    if not hashes_bloques:
        return hashlib.sha256(b"").hexdigest()
    return hashlib.sha256(hashes_bloques).hexdigest()