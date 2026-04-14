from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# ✅ JWT Configuration
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")

# ✅ Database Configuration (AWS RDS MySQL)
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize extensions
from services.db import db
db.init_app(app)

jwt = JWTManager(app)

# ✅ Root route
@app.route('/')
def home():
    return jsonify({
        "message": "Lost & Found Backend is running!",
        "status": "success"
    }), 200

# ✅ Health check route
@app.route('/api/health')
def health():
    return jsonify({"status": "OK"}), 200

# Import and register route blueprints
from routes.auth import auth_bp
from routes.lost_items import lost_bp
from routes.found_items import found_bp
from routes.matches import matches_bp
from routes.claims import claims_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(lost_bp, url_prefix='/api/lost-items')
app.register_blueprint(found_bp, url_prefix='/api/found-items')
app.register_blueprint(matches_bp, url_prefix='/api/matches')
app.register_blueprint(claims_bp, url_prefix='/api/claims')

# Optional: Create tables automatically (useful for development)
with app.app_context():
    db.create_all()

# Run the app locally
if __name__ == "__main__":
    app.run(debug=True)