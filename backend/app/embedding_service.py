# app/embedding_service.py
from sentence_transformers import SentenceTransformer
import numpy as np

# Load model 1 lần (sau đó cache lại, không load lại nữa)
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    """Trả về vector embedding cho text"""
    if not text:
        return None
    return model.encode(text, convert_to_numpy=True).tolist()

def cosine_similarity(vec1, vec2):
    """Tính cosine similarity"""
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return float(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
