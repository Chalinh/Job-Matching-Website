"""Strategy 3: Enhanced KeyBERT with MMR diversity and aggressive filtering."""
from typing import List
from keybert import KeyBERT
from ..config import KEYBERT_MODEL, EnhancedExtractionConfig
from ..utils.text_utils import clean_skill, is_likely_skill
import torch

# Optional spaCy import
try:
    import spacy
    SPACY_AVAILABLE = True
except (ImportError, Exception):
    SPACY_AVAILABLE = False
    spacy = None

class KeyBERTExtractor:
    """Extract skills using enhanced KeyBERT with semantic understanding."""

    def __init__(self, config: EnhancedExtractionConfig = None):
        """Initialize KeyBERT model."""
        self.config = config or EnhancedExtractionConfig()
        
        # Initialize KeyBERT (will use GPU if available via sentence-transformers)
        print(f"  Initializing KeyBERT...")
        
        self.model = KeyBERT(model=KEYBERT_MODEL)

        # Load spaCy for POS tagging (lightweight filtering) if available
        self.nlp = None
        if SPACY_AVAILABLE and spacy:
            try:
                self.nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
            except (OSError, Exception):
                print("Note: spaCy POS filtering disabled (model not found)")
                self.nlp = None

    def _filter_by_pos(self, keyword: str) -> bool:
        """Filter keywords by part-of-speech tags (keep only nouns/proper nouns)."""
        if not self.nlp:
            return True  # Skip filtering if spaCy not available

        doc = self.nlp(keyword)
        # Keep if contains at least one noun or proper noun
        has_noun = any(token.pos_ in ["NOUN", "PROPN"] for token in doc)

        # Reject if starts with adjective or verb
        if doc and doc[0].pos_ in ["ADJ", "VERB", "ADV"]:
            return False

        return has_noun

    def _is_verbose_phrase(self, keyword: str) -> bool:
        """Check if keyword is a verbose/generic phrase."""
        # Remove very long phrases
        if len(keyword) > 40:
            return True

        # Remove if contains too many words
        word_count = len(keyword.split())
        if word_count > 4:
            return True

        # Remove common verbose patterns
        verbose_patterns = [
            'good', 'excellent', 'strong', 'knowledge', 'experience', 'skills',
            'ability', 'able', 'must', 'should', 'required', 'preferred',
            'working', 'work with', 'years experience'
        ]

        keyword_lower = keyword.lower()
        if any(pattern in keyword_lower for pattern in verbose_patterns):
            # But keep if it's a specific technical term
            if word_count <= 2 and not keyword_lower.startswith(('good', 'excellent', 'strong')):
                return False
            return True

        return False

    def extract(self, text: str) -> List[str]:
        """Extract skills using KeyBERT with aggressive filtering."""
        if not text:
            return []

        try:
            # Extract keywords with MMR for diversity
            keywords = self.model.extract_keywords(
                text,
                keyphrase_ngram_range=self.config.KEYBERT_NGRAM_RANGE,
                stop_words='english',
                use_mmr=True,  # Maximum Marginal Relevance for diversity
                diversity=self.config.KEYBERT_DIVERSITY,
                top_n=self.config.KEYBERT_TOP_N
            )

            found_skills = set()

            for keyword, score in keywords:
                # Score threshold
                if score < self.config.KEYBERT_THRESHOLD:
                    continue

                keyword = clean_skill(keyword)

                # Length filter
                if len(keyword) < 2 or len(keyword) > 40:
                    continue

                # Filter verbose phrases
                if self._is_verbose_phrase(keyword):
                    continue

                # POS filtering
                if not self._filter_by_pos(keyword):
                    continue

                # Final check
                if is_likely_skill(keyword):
                    found_skills.add(keyword.lower())

            return sorted(found_skills)

        except Exception as e:
            print(f"KeyBERT extraction failed: {e}")
            return []

    def extract_batch(self, texts: List[str]) -> List[List[str]]:
        """Batch extraction."""
        return [self.extract(text) for text in texts]
