from flask import Flask, jsonify, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = "tareas.db"


def conectar_db():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_tablas():
    conexion = conectar_db()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


@app.route("/")
def inicio():
    return jsonify({
        "mensaje": "Bienvenido al SGT: Sistema de Gestión de Tareas",
        "estado": "Servidor funcionando correctamente"
    })


@app.route("/registro", methods=["POST"])
def registro():
    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({
            "error": "El usuario y la contraseña son obligatorios"
        }), 400

    password_hash = generate_password_hash(contraseña)

    try:
        conexion = conectar_db()

        conexion.execute(
            """
            INSERT INTO usuarios (usuario, password_hash)
            VALUES (?, ?)
            """,
            (usuario, password_hash)
        )

        conexion.commit()
        conexion.close()

        return jsonify({
            "mensaje": "Usuario registrado correctamente"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "El usuario ya existe"
        }), 409


@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({
            "error": "El usuario y la contraseña son obligatorios"
        }), 400

    conexion = conectar_db()

    usuario_db = conexion.execute(
        "SELECT * FROM usuarios WHERE usuario = ?",
        (usuario,)
    ).fetchone()

    conexion.close()

    if usuario_db is None:
        return jsonify({
            "error": "Usuario o contraseña incorrectos"
        }), 401

    if not check_password_hash(usuario_db["password_hash"], contraseña):
        return jsonify({
            "error": "Usuario o contraseña incorrectos"
        }), 401

    return jsonify({
        "mensaje": "Inicio de sesión exitoso",
        "usuario": usuario
    }), 200


if __name__ == "__main__":
    crear_tablas()
    app.run(debug=True)