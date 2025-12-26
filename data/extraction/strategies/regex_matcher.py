"""Strategy 1: Regex-based pattern matching for known technical skills."""
import json
import re
from typing import List, Set
from pathlib import Path
from ..config import TECHNICAL_SKILLS_FILE

class RegexMatcher:
    """Extract skills using regex pattern matching against known skills database."""

    def __init__(self):
        """Initialize with technical skills database."""
        self.skills_db: Set[str] = set()
        self.patterns: List[re.Pattern] = []
        self._load_skills_database()

    def _load_skills_database(self):
        """Load and compile regex patterns for all technical skills."""
        with open(TECHNICAL_SKILLS_FILE, 'r', encoding='utf-8') as f:
            skills_data = json.load(f)

        # Flatten all categories into a single set
        for category, skills in skills_data.items():
            self.skills_db.update(skill.lower() for skill in skills)

        # Create regex patterns with word boundaries
        # Sort by length (longest first) to match longer phrases before shorter ones
        sorted_skills = sorted(self.skills_db, key=len, reverse=True)

        for skill in sorted_skills:
            # Escape special regex characters
            escaped = re.escape(skill)
            # Create pattern with word boundaries
            # Use \b for simple words, custom boundaries for complex terms
            if re.match(r'^[a-zA-Z0-9]+$', skill):
                # Simple alphanumeric skill
                pattern = rf'\b{escaped}\b'
            else:
                # Complex skill with special chars (e.g., "c++", "ms office")
                pattern = rf'(?:^|[\s,;(])({escaped})(?:[\s,;)]|$)'

            self.patterns.append((skill, re.compile(pattern, re.IGNORECASE)))

    def extract(self, text: str) -> List[str]:
        """Extract skills from text using regex matching."""
        if not text:
            return []

        text_lower = text.lower()
        found_skills = set()

        # Match against all patterns
        for skill, pattern in self.patterns:
            if pattern.search(text_lower):
                found_skills.add(skill)

        return sorted(found_skills)

    def extract_batch(self, texts: List[str]) -> List[List[str]]:
        """Batch extraction (same as sequential for regex)."""
        return [self.extract(text) for text in texts]
