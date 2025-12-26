"""Normalization module for cleaning and standardizing skills."""
from typing import List
from ..utils.text_utils import clean_skill, normalize_text

class Normalizer:
    """Normalize skills: lowercase, trim, clean special characters."""

    def normalize(self, skills: List[str]) -> List[str]:
        """Normalize a list of skills."""
        normalized = set()

        for skill in skills:
            # Clean and normalize
            cleaned = clean_skill(skill)
            normalized_skill = normalize_text(cleaned)

            # Skip empty or too short
            if not normalized_skill or len(normalized_skill) < 2:
                continue

            normalized.add(normalized_skill)

        return sorted(normalized)

    def normalize_single(self, skill: str) -> str:
        """Normalize a single skill."""
        return normalize_text(clean_skill(skill))
