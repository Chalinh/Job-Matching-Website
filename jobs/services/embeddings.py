from sentence_transformers import SentenceTransformer
import numpy as np
from functools import lru_cache


class EmbeddingService:
    """Lazy-loaded sentence embedding service"""

    def __init__(self):
        self.model = None

    def _load_model(self):
        """Lazy load embedding model"""
        if self.model is None:
            print("Loading sentence transformer model...")
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            print("Model loaded!")

    @lru_cache(maxsize=1000)
    def embed(self, text):
        """Embed a single text (cached)"""
        self._load_model()
        return self.model.encode(text, convert_to_numpy=True)

    def embed_batch(self, texts):
        """Embed multiple texts"""
        self._load_model()
        return self.model.encode(texts, convert_to_numpy=True)

    def cosine_similarity(self, vec1, vec2):
        """Compute cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
