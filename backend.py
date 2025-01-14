from flask import Flask, request, jsonify
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Configura aquí los detalles de conexión a tu base de datos
DB_HOST = "127.0.0.1"
DB_NAME = "flask"
DB_USER = "usu"
DB_PASS = "admin"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/')
def index():
    return "API para gestionar personas"

@app.route('/personas', methods=['GET'])
def get_personas():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM personas"
    cur.execute(s)
    lista_personas = cur.fetchall()
    cur.close()
    return jsonify(lista_personas)

@app.route('/persona', methods=['POST'])
def add_persona():
    new_persona = request.get_json()
    nombre = new_persona['nombre']
    apellido = new_persona['apellido']
    edad = new_persona['edad']
    sexo = new_persona['sexo']
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("INSERT INTO personas (nombre, apellido, edad, sexo) VALUES (%s, %s, %s, %s) RETURNING *", (nombre, apellido, edad, sexo))
    new_persona_id = cur.fetchone()
    conn.commit()
    cur.close()
    return jsonify(new_persona_id)

@app.route('/persona/<id>', methods=['DELETE'])
def delete_persona(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("DELETE FROM personas WHERE id = %s RETURNING *", (id,))
    deleted_persona = cur.fetchone()
    conn.commit()
    cur.close()
    return jsonify(deleted_persona)

if __name__ == '__main__':
    app.run(debug=True)
