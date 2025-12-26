"""Strategy 4: Named Entity Recognition using spaCy."""
import json
from typing import List, Set
from ..config import SPACY_MODEL, TECHNICAL_SKILLS_FILE, EnhancedExtractionConfig
from ..utils.text_utils import clean_skill

# Optional spaCy import
try:
    import spacy
    SPACY_AVAILABLE = True
except (ImportError, Exception):
    SPACY_AVAILABLE = False
    spacy = None

class NERExtractor:
    """Extract skills using Named Entity Recognition for products and organizations."""

    def __init__(self, config: EnhancedExtractionConfig = None):
        """Initialize spaCy NER model."""
        self.config = config or EnhancedExtractionConfig()

        # Load spaCy model if available
        self.nlp = None
        if SPACY_AVAILABLE and spacy:
            try:
                self.nlp = spacy.load(SPACY_MODEL, disable=["lemmatizer", "textcat"])
            except (OSError, Exception):
                print(f"Note: spaCy NER disabled (model '{SPACY_MODEL}' not available)")
                self.nlp = None

        # Load technical skills for validation
        with open(TECHNICAL_SKILLS_FILE, 'r', encoding='utf-8') as f:
            skills_data = json.load(f)
        self.tech_skills = set()
        for category, skills in skills_data.items():
            self.tech_skills.update(skill.lower() for skill in skills)

    def extract(self, text: str) -> List[str]:
        """Extract skills using NER."""
        if not text or not self.nlp:
            return []

        found_skills = set()

        try:
            doc = self.nlp(text)

            for ent in doc.ents:
                # Only extract PRODUCT and ORG entities
                if ent.label_ in self.config.NER_LABELS:
                    entity_text = clean_skill(ent.text)

                    # Normalize
                    entity_lower = entity_text.lower()

                    # Validate against technical skills database
                    if entity_lower in self.tech_skills:
                        found_skills.add(entity_lower)
                    # Or if it looks like a technical tool/product name
                    elif len(entity_lower) >= 2 and len(entity_lower) <= 30:
                        # Additional heuristics: likely a technical product
                        if any(char.isupper() for char in ent.text):  # Has capitals (product name)
                            found_skills.add(entity_lower)

            return sorted(found_skills)

        except Exception as e:
            print(f"NER extraction failed: {e}")
            return []

    def extract_batch(self, texts: List[str]) -> List[List[str]]:
        """Batch extraction using spaCy's pipe for efficiency."""
        if not texts or not self.nlp:
            return [[] for _ in texts]

        try:
            found_skills_list = []

            # Use spaCy's pipe for efficient batch processing
            for doc in self.nlp.pipe(texts, disable=["lemmatizer", "textcat"]):
                doc_skills = set()

                for ent in doc.ents:
                    if ent.label_ in self.config.NER_LABELS:
                        entity_text = clean_skill(ent.text)
                        entity_lower = entity_text.lower()

                        if entity_lower in self.tech_skills:
                            doc_skills.add(entity_lower)
                        elif len(entity_lower) >= 2 and len(entity_lower) <= 30:
                            if any(char.isupper() for char in ent.text):
                                doc_skills.add(entity_lower)

                found_skills_list.append(sorted(doc_skills))

            return found_skills_list

        except Exception as e:
            print(f"Batch NER extraction failed: {e}")
            return [[] for _ in texts]
