from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
import numpy as np
from services.db import get_connection

nltk.download("punkt")
nltk.download("stopwords")

stemmer = PorterStemmer()

def preprocess(text):
    tokens = word_tokenize(text.lower())
    tokens = [t for t in tokens if t not in stopwords.words("english") and t.isalpha()]
    tokens = [stemmer.stem(t) for t in tokens]
    return " ".join(tokens)

def compute_text_similarity(desc1, desc2):
    processed = [preprocess(desc1), preprocess(desc2)]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(processed)
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return float(score)

def find_matches(item_id, item_type, threshold=0.65):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    if item_type == "lost":
        cursor.execute("SELECT description FROM lost_items WHERE item_id=%s", (item_id,))
        source = cursor.fetchone()
        cursor.execute("SELECT item_id, description FROM found_items WHERE status='active'")
        candidates = cursor.fetchall()
        source_table = "lost_item_id"
        candidate_table = "found_item_id"
    else:
        cursor.execute("SELECT description FROM found_items WHERE item_id=%s", (item_id,))
        source = cursor.fetchone()
        cursor.execute("SELECT item_id, description FROM lost_items WHERE status='active'")
        candidates = cursor.fetchall()
        source_table = "found_item_id"
        candidate_table = "lost_item_id"

    matches = []
    for candidate in candidates:
        score = compute_text_similarity(source["description"], candidate["description"])
        if score >= threshold:
            cursor.execute(
                f"INSERT INTO matches ({source_table},{candidate_table},nlp_score,combined_score) VALUES (%s,%s,%s,%s)",
                (item_id, candidate["item_id"], score, score)
            )
            conn.commit()
            matches.append({"item_id": candidate["item_id"], "score": score})

    cursor.close()
    conn.close()
    return matches