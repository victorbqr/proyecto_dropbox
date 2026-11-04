from flask import Flask, jsonify, request, render_template, send_file
from pathlib import Path
import io
from cbas.database import obtener_historial, registrar_evento
from cbas.dropbox_service import restaurar_version_en_carpeta, obtener_cliente_dropbox
from cbas.config import MONITORED_DIR, USUARIO_SO, IP_LOCAL, HOSTNAME
from cbas.agent import ultimo_hash_conocido

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("dashboard.html")

@app.route("/api/archivos", methods=["GET"])
def listar_archivos():
    historial = obtener_historial()
    agrupados = {}
    for item in historial:
        nombre = item["nombre_archivo"]
        if nombre not in agrupados:
            agrupados[nombre] = []
        agrupados[nombre].append(item)
    return jsonify(agrupados)

@app.route("/api/contenido/<nombre_archivo>", methods=["GET"])
def ver_contenido(nombre_archivo):
    ruta = MONITORED_DIR / nombre_archivo
    if not ruta.exists():
        return jsonify({"contenido": "(El archivo no existe localmente)"})
    try:
        # Intentar leer como texto
        with open(ruta, "r", encoding="utf-8", errors="replace") as f:
            contenido = f.read(5000) # Primeros 5000 caracteres
        return jsonify({"contenido": contenido, "tipo": "texto"})
    except Exception as e:
        return jsonify({"contenido": f"Archivo binario o error: {e}", "tipo": "binario"})

@app.route("/api/download/<nombre_archivo>/<rev>", methods=["GET"])
def descargar_rev(nombre_archivo, rev):
    try:
        dbx = obtener_cliente_dropbox()
        ruta_nube = f"/{nombre_archivo}"
        metadata, response = dbx.files_download(ruta_nube, rev=rev)
        return send_file(
            io.BytesIO(response.content),
            as_attachment=True,
            download_name=f"{metadata.name}"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/restore", methods=["POST"])
def restaurar():
    data = request.json
    nombre = data.get("nombre_archivo")
    rev = data.get("rev")
    try:
        resultado = restaurar_version_en_carpeta(nombre, rev)
        ultimo_hash_conocido[nombre] = resultado["content_hash"]

        historial = [h for h in obtener_historial() if h["nombre_archivo"] == nombre]
        version_correlativa = f"v{len(historial) + 1}"

        registrar_evento(
            nombre_archivo=nombre,
            version_tag=version_correlativa,
            rev=resultado["nueva_rev_activa"],
            content_hash=resultado["content_hash"],
            tamano=resultado["tamano_bytes"],
            operacion="RESTAURADO",
            usuario=USUARIO_SO,
            ip=IP_LOCAL,
            hostname=HOSTNAME
        )
        return jsonify({"status": "ok", "version": version_correlativa, "data": resultado})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500