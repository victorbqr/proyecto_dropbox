import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from cbas.config import MONITORED_DIR, USUARIO_SO, IP_LOCAL, HOSTNAME
from cbas.hasher import calcular_content_hash_dropbox
from cbas.dropbox_service import subir_archivo
from cbas.database import registrar_evento, obtener_historial

ultimo_hash_conocido = {}

class ManejadorArchivos(FileSystemEventHandler):
    def on_modified(self, event):
        self.procesar(event)

    def on_created(self, event):
        self.procesar(event)

    def procesar(self, event):
        if event.is_directory:
            return
        ruta = Path(event.src_path)
        if ruta.name.startswith(".") or ruta.name.endswith(".tmp"):
            return

        time.sleep(1.0)  # Debounce de estabilización en disco

        try:
            nuevo_hash = calcular_content_hash_dropbox(ruta)
            nombre = ruta.name

            # Prevención de bucles y subidas redundantes
            if ultimo_hash_conocido.get(nombre) == nuevo_hash:
                return

            print(f"[CBAS Agent] Detectado cambio en: {nombre}. Sincronizando con Dropbox...")
            meta = subir_archivo(nombre)
            ultimo_hash_conocido[nombre] = nuevo_hash

            historial = [h for h in obtener_historial() if h["nombre_archivo"] == nombre]
            version_correlativa = f"v{len(historial) + 1}"
            operacion = "CREADO" if len(historial) == 0 else "MODIFICADO"

            registrar_evento(
                nombre_archivo=nombre,
                version_tag=version_correlativa,
                rev=meta.rev,
                content_hash=meta.content_hash,
                tamano=meta.size,
                operacion=operacion,
                usuario=USUARIO_SO,
                ip=IP_LOCAL,
                hostname=HOSTNAME
            )
            print(f"[CBAS Agent] Sincronizado {nombre} -> {version_correlativa} (rev: {meta.rev})")
        except Exception as e:
            print(f"[CBAS Agent] Error al procesar {ruta.name}: {e}")

def iniciar_agente():
    MONITORED_DIR.mkdir(parents=True, exist_ok=True)
    event_handler = ManejadorArchivos()
    observer = Observer()
    observer.schedule(event_handler, path=str(MONITORED_DIR), recursive=False)
    observer.start()
    print(f"[*] Agente Watchdog vigilando: {MONITORED_DIR}")
    return observer