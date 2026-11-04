import os
import socket
import getpass
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DROPBOX_APP_KEY = os.getenv("DROPBOX_APP_KEY")
DROPBOX_APP_SECRET = os.getenv("DROPBOX_APP_SECRET")
DROPBOX_REFRESH_TOKEN = os.getenv("DROPBOX_REFRESH_TOKEN")

# Ko'ãva ha'e umi oñekotevẽva ha omohenda DB_PATH:
MONITORED_DIR = BASE_DIR / "directorio_pyme"
DB_PATH = BASE_DIR / "cbas_auditoria.db"

def obtener_ip_local():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

HOSTNAME = socket.gethostname()
USUARIO_SO = getpass.getuser()
IP_LOCAL = obtener_ip_local()