from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.db import get_connection
import hashlib

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    campus_id = data.get("campus_id")
    password = data.get("password")
    pw_hash = hashlib.sha256(password.encode()).hexdigest()

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE campus_id=%s AND password_hash=%s", (campus_id, pw_hash))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user["user_id"]))
    return jsonify({"token": token, "user_id": user["user_id"], "name": user["name"]})

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    pw_hash = hashlib.sha256(data["password"].encode()).hexdigest()
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (campus_id, name, email, password_hash) VALUES (%s,%s,%s,%s)",
            (data["campus_id"], data["name"], data["email"], pw_hash)
        )
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()
        conn.close()
    return jsonify({"message": "Registered successfully"}), 201