# app.py
# Este archivo debe estar en la raíz de tu carpeta de proyecto (ej. proyecto-encuesta/app.py)

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlitecloud
import os

# --- Configuración Inicial ---
app = Flask(__name__, static_folder='public')
CORS(app) # Permite que el front-end (HTML) se comunique con este servidor

# --- Conexión a SQLite Cloud ---
# Esta es tu cadena de conexión personal.
CONNECTION_STRING = "sqlitecloud://czbxplhynk.g3.sqlite.cloud:8860/chinook.sqlite?apikey=pZSAdQavtt15i3Cjf5VYOqyraww2ScrsXtptm9KiQR8"

# --- Función para Inicializar la Base de Datos ---
def init_db():
    """Crea la tabla 'respuestas' en la nube si no existe."""
    try:
        with sqlitecloud.connect(CONNECTION_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS respuestas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    q1_juegas TEXT,
                    q2_frecuencia TEXT,
                    q3_usas_ingles TEXT,
                    q4_ayuda_clases TEXT,
                    q5_usar_en_clases TEXT,
                    q5_razon TEXT,
                    q6_mejora_rendimiento TEXT,
                    q6_manera TEXT,
                    q7_motiva_aprender TEXT,
                    q8_participas_foros TEXT,
                    q9_aplicas_vocabulario TEXT,
                    q10_mejora_pronunciacion TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            print("Conexión a SQLite Cloud exitosa. Tabla 'respuestas' lista.")
    except Exception as e:
        print(f"ERROR: No se pudo inicializar la base de datos en SQLite Cloud: {e}")

# --- Ruta para guardar los datos de la encuesta ---
@app.route('/submit', methods=['POST'])
def submit_survey():
    """Recibe los datos del formulario en formato JSON y los guarda en la base de datos."""
    try:
        data = request.get_json()
        with sqlitecloud.connect(CONNECTION_STRING) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO respuestas (
                    q1_juegas, q2_frecuencia, q3_usas_ingles, q4_ayuda_clases,
                    q5_usar_en_clases, q5_razon, q6_mejora_rendimiento, q6_manera,
                    q7_motiva_aprender, q8_participas_foros, q9_aplicas_vocabulario,
                    q10_mejora_pronunciacion
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('q1'), data.get('q2'), data.get('q3'), data.get('q4'),
                data.get('q5_choice'), data.get('q5_reason'), data.get('q6_choice'), data.get('q6_reason'),
                data.get('q7'), data.get('q8'), data.get('q9'), data.get('q10')
            ))
            conn.commit()
        print(f"Nueva respuesta recibida y guardada.")
        return jsonify({"status": "success", "message": "Encuesta guardada correctamente en la nube."}), 200
    except Exception as e:
        print(f"ERROR: No se pudo guardar la encuesta en la nube: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Punto de Entrada Principal ---
if __name__ == '__main__':
    init_db()
    # El servidor se ejecuta en el puerto 5000 y es accesible desde la red local.
    app.run(host='0.0.0.0', port=5000, debug=True)
