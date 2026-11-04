from cbas.database import init_db
from cbas.agent import iniciar_agente
from cbas.backend import app
import time

if __name__ == "__main__":
    init_db()
    observer = iniciar_agente()
    print("=" * 65)
    print("  CLOUD BACKUP & AUDIT SYSTEM (CBAS) - DROPBOX PLATFORM")
    print("  Servidor Web en http://127.0.0.1:5050")
    print("=" * 65)
    try:
        app.run(host="0.0.0.0", port=5050, debug=False, use_reloader=False)
    finally:
        observer.stop()
        observer.join()