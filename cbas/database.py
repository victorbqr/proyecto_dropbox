import sqlite3
from datetime import datetime, timezone
from cbas.config import DB_PATH

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS versiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_archivo TEXT NOT NULL,
            version_tag TEXT NOT NULL,
            rev TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            tamano_bytes INTEGER,
            operacion TEXT NOT NULL,
            usuario TEXT,
            ip_origen TEXT,
            hostname TEXT,
            fecha_utc TEXT
        )
    """)
    conn.commit()
    conn.close()

def registrar_evento(nombre_archivo, version_tag, rev, content_hash, tamano, operacion, usuario, ip, hostname):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    fecha_utc = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    cursor.execute("""
        INSERT INTO versiones (nombre_archivo, version_tag, rev, content_hash, tamano_bytes, operacion, usuario, ip_origen, hostname, fecha_utc)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (nombre_archivo, version_tag, rev, content_hash, tamano, operacion, usuario, ip, hostname, fecha_utc))
    conn.commit()
    conn.close()

def obtener_historial():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM versiones ORDER BY id DESC")
    filas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return filas