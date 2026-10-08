from flask import Flask, jsonify, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = "tareas.db"


def connect_db():
    connection = sqlite3.connect(DATABASE, timeout=5)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = connect_db()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        connection.commit()

    finally:
        connection.close()


@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to the Task Management System",
        "status": "Server is running correctly"
    })


@app.route("/registro", methods=["POST"])
def register():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    password_hash = generate_password_hash(password)

    connection = connect_db()

    try:
        connection.execute(
            """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        connection.commit()

        return jsonify({
            "message": "User registered successfully"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "Username already exists"
        }), 409

    finally:
        connection.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    connection = connect_db()

    try:
        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

    finally:
        connection.close()

    if user is None:
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    if not check_password_hash(user["password_hash"], password):
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "username": username
    }), 200


@app.route("/tareas", methods=["GET"])
def tasks():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Management System</title>
    </head>
    <body>
        <h1>Welcome to the Task Management System!</h1>
        <p>You have logged in successfully.</p>
        <p>This is the task management area.</p>
    </body>
    </html>
    """


if __name__ == "__main__":
    create_tables()
    app.run(debug=True)