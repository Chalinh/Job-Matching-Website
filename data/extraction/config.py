"""Enhanced configuration for v3 extraction engine with improved accuracy."""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
RESOURCES_DIR = BASE_DIR / "resources"

# Resource files
TECHNICAL_SKILLS_FILE = RESOURCES_DIR / "technical_skills.json"
MAJOR_TAXONOMY_FILE = RESOURCES_DIR / "major_taxonomy.json"
BLACKLIST_FILE = RESOURCES_DIR / "blacklist.json"
SYNONYMS_FILE = RESOURCES_DIR / "skill_synonyms.json"

# Model configurations
KEYBERT_MODEL = "paraphrase-MiniLM-L6-v2"
SPACY_MODEL = "en_core_web_sm"
LLM_MODEL = "google/flan-t5-base"

# V3 Enhanced Extraction Parameters
class EnhancedExtractionConfig:
    # KeyBERT parameters - more relaxed for better recall
    KEYBERT_TOP_N = 25  # Increased from 20
    KEYBERT_THRESHOLD = 0.38  # Slightly reduced from 0.40 for better recall
    KEYBERT_NGRAM_RANGE = (1, 3)  # Allow 3-word phrases for compound skills
    KEYBERT_DIVERSITY = 0.75  # Higher diversity

    # Section parser parameters
    SECTION_MIN_LENGTH = 2  # Back to 2 for technical acronyms
    SECTION_MAX_LENGTH = 60  # Increased from 50

    # NER parameters
    NER_LABELS = ["PRODUCT", "ORG", "GPE"]  # Added GPE for location-based tech

    # Post-processing parameters
    MIN_SKILL_LENGTH = 2
    MAX_SKILL_LENGTH = 60  # Increased from 50

    # Enhanced education regex patterns with more variations
    EDUCATION_LEVEL_PATTERNS = {
        "high school": r"(?:high\s+school|secondary\s+school|diploma(?!\s+in)|form\s+\d+|grade\s+12)",
        "associate": r"(?:associate'?s?\s+degree|a\.s\.|associate\s+in)",
        "bachelor's degree": r"(?:bachelor'?s?\s+(?:degree|diploma)?|ba\b|b\.s\b|b\.sc\b|bs\s+degree|bachelor\s+(?:in|of)|beng|bsc|undergraduate\s+degree)",
        "master's degree": r"(?:master'?s?\s+(?:degree|diploma)?|msc|m\.s\b|m\.sc\b|graduate\s+degree|ma\b|master\s+(?:in|of)|postgraduate\s+degree|mba|meng)",
        "phd": r"(?:ph\.?d\.?|doctorate|doctoral|doctor\s+of\s+philosophy)"
    }

    # Enhanced major extraction with multiple strategies
    MAJOR_EXTRACTION_PATTERNS = [
        # Direct patterns
        r"(?:degree|diploma|bachelor'?s?|master'?s?|phd)\s+(?:in|of)\s+([a-z][a-z\s&/,-]{2,50})(?:\s+or|\s+and|,|\.|$|related)",
        r"(?:ba|bs|bsc|beng|ma|ms|msc|mba|meng)\s+(?:in|of)?\s*([a-z][a-z\s&/,-]{2,50})(?:\s+or|\s+and|,|\.|$|related)",
        r"major[\s:]+([a-z][a-z\s&/,-]{2,50})(?:\s+or|\s+and|,|\.|$|related)",
        r"field\s+of\s+(?:study[\s:]+)?([a-z][a-z\s&/,-]{2,50})(?:\s+or|\s+and|,|\.|$|related)",
        r"study[\s:]+([a-z][a-z\s&/,-]{2,50})(?:\s+or|\s+and|,|\.|$|related)",
        r"graduated\s+(?:in|with|from)\s+([a-z][a-z\s&/,-]{2,50})(?:\s+or|\s+and|,|\.|$|related)",
        # Compound patterns for multiple majors
        r"([a-z][a-z\s&/,-]{2,40})\s+or\s+related\s+field",
    ]

    # Soft skills to recognize (not in technical_skills.json)
    SOFT_SKILLS = [
        "communication", "leadership", "teamwork", "problem solving",
        "time management", "critical thinking", "creativity",
        "adaptability", "work ethic", "interpersonal skills",
        "presentation skills", "analytical skills", "organizational skills"
    ]

    # Cache settings
    CACHE_SIZE = 1500  # Increased from 1000
    BATCH_SIZE = 50
