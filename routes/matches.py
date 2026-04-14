# File: routes/matches.py
from flask import Blueprint, jsonify, request

# Define the Blueprint
matches_bp = Blueprint('matches', __name__)

# Example: Get all matches
@matches_bp.route('/', methods=['GET'])
def get_matches():
    """
    Retrieve all matches between lost and found items.
    """
    # Placeholder response – replace with database logic later
    return jsonify({
        "message": "List of matches",
        "matches": []
    }), 200


# Example: Create a new match
@matches_bp.route('/', methods=['POST'])
def create_match():
    """
    Create a new match between a lost item and a found item.
    """
    data = request.get_json()

    lost_item_id = data.get('lost_item_id')
    found_item_id = data.get('found_item_id')
    similarity_score = data.get('similarity_score', 0)

    # Placeholder response – replace with database logic later
    return jsonify({
        "message": "Match created successfully",
        "match": {
            "lost_item_id": lost_item_id,
            "found_item_id": found_item_id,
            "similarity_score": similarity_score
        }
    }), 201