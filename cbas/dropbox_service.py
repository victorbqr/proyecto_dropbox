import dropbox
from dropbox.files import WriteMode
from cbas.config import DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REFRESH_TOKEN, MONITORED_DIR

def obtener_cliente_dropbox():
    return dropbox.Dropbox(
        app_key=DROPBOX_APP_KEY,
        app_secret=DROPBOX_APP_SECRET,
        oauth2_refresh_token=DROPBOX_REFRESH_TOKEN
    )

def subir_archivo(nombre_archivo: str):
    dbx = obtener_cliente_dropbox()
    ruta_local = MONITORED_DIR / nombre_archivo
    ruta_nube = f"/{nombre_archivo}"
    with open(ruta_local, "rb") as f:
        meta = dbx.files_upload(f.read(), ruta_nube, mode=WriteMode.overwrite)
    return meta

def restaurar_version_en_carpeta(nombre_archivo: str, rev_objetivo: str) -> dict:
    dbx = obtener_cliente_dropbox()
    ruta_nube = f"/{nombre_archivo}"
    ruta_local_destino = MONITORED_DIR / nombre_archivo
    
    # 1. Reversión transaccional en Dropbox Version History
    restaurado_meta = dbx.files_restore(ruta_nube, rev_objetivo)
    
    # 2. Descarga del contenido restaurado hacia la carpeta local
    MONITORED_DIR.mkdir(parents=True, exist_ok=True)
    dbx.files_download_to_file(str(ruta_local_destino), ruta_nube)
    return {
        "nombre_archivo": nombre_archivo,
        "rev_solicitada": rev_objetivo,
        "nueva_rev_activa": restaurado_meta.rev,
        "content_hash": restaurado_meta.content_hash,
        "tamano_bytes": restaurado_meta.size,
    }