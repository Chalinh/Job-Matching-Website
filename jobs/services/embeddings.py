import numpy as np

class EmbeddingService:
    """Lazy-loaded sentence embedding service"""

    _instance = None
    _model = None

    def __new__(cls):
        """Singleton pattern to ensure only one model instance"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _load_model(self):
        """Lazy load embedding model only when needed"""
        if EmbeddingService._model is None:
            print("Loading sentence transformer model...")
            try:
                from sentence_transformers import SentenceTransformer
                # Use a smaller, more memory-efficient model
                EmbeddingService._model = SentenceTransformer(
                    'sentence-transformers/all-MiniLM-L6-v2',
                    device='cpu'  # Force CPU to avoid GPU memory issues
                )
                print("Model loaded successfully!")
            except MemoryError:
                print("ERROR: Not enough memory to load embedding model. Semantic matching disabled.")
                EmbeddingService._model = False  # Mark as failed
                raise
            except Exception as e:
                print(f"Error loading model: {e}. Semantic matching disabled.")
                EmbeddingService._model = False
                raise

    def embed(self, text):
        """Embed a single text"""
        self._load_model()
        return EmbeddingService._model.encode(text, convert_to_numpy=True)

    def embed_batch(self, texts):
        """Embed multiple texts"""
        self._load_model()
        return EmbeddingService._model.encode(texts, convert_to_numpy=True)

    def cosine_similarity(self, vec1, vec2):
        """Compute cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
