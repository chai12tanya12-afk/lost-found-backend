# File: routes/claims.py
from flask import Blueprint, jsonify, request

# Define the Blueprint
claims_bp = Blueprint('claims', __name__)

# Example: Get all claims
@claims_bp.route('/', methods=['GET'])
def get_claims():
    """
    Retrieve all claims made by users.
    """
    # Placeholder response – replace with database logic later
    return jsonify({
        "message": "List of claims",
        "claims": []
    }), 200


# Example: Submit a new claim
@claims_bp.route('/', methods=['POST'])
def create_claim():
    """
    Submit a claim for a found item.
    """
    data = request.get_json()

    claim = {
        "user_id": data.get('user_id'),
        "found_item_id": data.get('found_item_id'),
        "description": data.get('description'),
        "status": "pending"
    }

    # Placeholder response – replace with database logic later
    return jsonify({
        "message": "Claim submitted successfully",
        "claim": claim
    }), 201


# Example: Update claim status (approve/reject)
@claims_bp.route('/<int:claim_id>', methods=['PUT'])
def update_claim_status(claim_id):
    """
    Update the status of a claim.
    """
    data = request.get_json()
    status = data.get('status')

    if status not in ['approved', 'rejected', 'pending']:
        return jsonify({"error": "Invalid status"}), 400

    # Placeholder response – replace with database logic later
    return jsonify({
        "message": f"Claim {status} successfully",
        "claim_id": claim_id,
        "status": status
    }), 200