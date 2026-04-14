from flask import Blueprint, request, jsonify

# Define the Blueprint
found_bp = Blueprint('found_items', __name__)

# Example route to get all found items
@found_bp.route('/', methods=['GET'])
def get_found_items():
    return jsonify({"message": "List of found items"}), 200

# Example route to create a found item
@found_bp.route('/', methods=['POST'])
def create_found_item():
    data = request.get_json()
    return jsonify({
        "message": "Found item reported successfully",
        "data": data
    }), 201