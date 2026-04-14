from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.db import get_connection
from services.ai_matching import find_matches
from services.notifications import dispatch_notification
import os

lost_bp = Blueprint("lost", __name__)

@lost_bp.route("/report/lost", methods=["POST"])
@jwt_required()
def report_lost():
    user_id = get_jwt_identity()
    data = request.form
    image = request.files.get("image")
    image_path = None

    if image:
        image_path = f"uploads/{user_id}_{image.filename}"
        image.save(image_path)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO lost_items (user_id,category,description,location,date_lost,image_path) VALUES (%s,%s,%s,%s,%s,%s)",
        (user_id, data["category"], data["description"], data["location"], data["date_lost"], image_path)
    )
    conn.commit()
    item_id = cursor.lastrowid
    cursor.close()
    conn.close()

    matches = find_matches(item_id, "lost")
    if matches:
        dispatch_notification(user_id, f"We found {len(matches)} potential match(es) for your lost item!")

    return jsonify({"status": "success", "item_id": item_id}), 201

@lost_bp.route("/items/lost", methods=["GET"])
@jwt_required()
def get_lost_items():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM lost_items WHERE status='active' ORDER BY created_at DESC")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)