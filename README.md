# Lost & Found Backend

This is the Flask backend for the Lost & Found Management System. It provides RESTful APIs for managing lost and found items, user authentication, claims, and AI-based matching.

## 🚀 Features
- JWT-based authentication
- MySQL database integration
- Firebase Cloud Messaging (FCM) for notifications
- AI-based item matching using NLP
- RESTful API design
- Deployment-ready with Render

## 🛠️ Tech Stack
- Flask
- MySQL (AWS RDS)
- Firebase Admin SDK
- Scikit-learn & NLTK
- Gunicorn
- Render (Deployment)

## 📦 Installation

```bash
git clone https://github.com/chai12tanya12/lost-found-backend.git
cd lost-found-backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
