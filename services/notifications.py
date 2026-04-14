import firebase_admin
from firebase_admin import credentials, messaging
import os

cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_credentials.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

def dispatch_notification(user_id, message_body):
    from services.db import get_connection
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT fcm_token FROM users WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user or not user["fcm_token"]:
        return None

    message = messaging.Message(
        notification=messaging.Notification(
            title="Lost Item Match Found!",
            body=message_body
        ),
        token=user["fcm_token"]
    )
    response = messaging.send(message)
    return response