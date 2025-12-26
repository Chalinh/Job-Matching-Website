"""Validation module to filter out non-skill phrases."""
import json
from typing import List, Set
from ..config import BLACKLIST_FILE, EnhancedExtractionConfig

class Validator:
    """Validate skills against blacklist and other criteria."""

    def __init__(self, config: EnhancedExtractionConfig = None):
        """Initialize validator with blacklist."""
        self.config = config or EnhancedExtractionConfig()
        self.blacklist: Set[str] = set()
        self._load_blacklist()

    def _load_blacklist(self):
        """Load blacklisted phrases."""
        try:
            with open(BLACKLIST_FILE, 'r', encoding='utf-8') as f:
                blacklist_data = json.load(f)

            # Flatten all categories
            for category, phrases in blacklist_data.items():
                self.blacklist.update(phrase.lower() for phrase in phrases)

        except FileNotFoundError:
            print(f"Warning: Blacklist file not found at {BLACKLIST_FILE}")

    def validate(self, skills: List[str]) -> List[str]:
        """Filter skills through validation criteria."""
        validated = []

        for skill in skills:
            if self._is_valid_skill(skill):
                validated.append(skill)

        return validated

    def _is_valid_skill(self, skill: str) -> bool:
        """Check if a skill passes all validation criteria."""
        skill_lower = skill.lower().strip()

        # Check length
        if len(skill_lower) < self.config.MIN_SKILL_LENGTH:
            return False
        if len(skill_lower) > self.config.MAX_SKILL_LENGTH:
            return False

        # Check against blacklist (exact match)
        if skill_lower in self.blacklist:
            return False

        # Check if any blacklisted phrase is in the skill
        for blacklisted in self.blacklist:
            if blacklisted in skill_lower and len(blacklisted) > 5:
                return False

        # Reject if it's just a number or contains mostly numbers
        if skill_lower.isdigit():
            return False

        # Reject if contains email pattern
        if '@' in skill_lower or '.com' in skill_lower or '.net' in skill_lower:
            return False

        # Reject if starts with "and " or "or "
        if skill_lower.startswith(('and ', 'or ', 'the ', 'a ', 'an ')):
            return False

        # Reject if ends with common sentence endings
        if skill_lower.endswith(('.', '!', '?', ',')):
            return False

        # Reject if contains "no." (address numbers)
        if 'no.' in skill_lower or 'no ' in skill_lower:
            return False

        # Reject if contains location indicators (Cambodian location words)
        location_words = ['khan', 'sangkat', 'phum', 'boeng', 'chbar', 'ampov',
                         'chhuk', 'nirouth', 'chamkar', 'daun', 'penh', 'phnom',
                         'location', 'academy', 'aupp', 'liger']
        if any(loc_word in skill_lower for loc_word in location_words):
            return False

        # Reject job roles/titles (not skills)
        job_role_indicators = ['supervisor', 'manager', 'director', 'coordinator',
                               'educator', 'officer', 'assistant', 'executive']
        if any(skill_lower.endswith(role) for role in job_role_indicators):
            return False

        # Count words (needed for subsequent checks)
        word_count = len(skill_lower.split())

        # Reject if it's a pure adjective/adverb (common single words)
        single_word_rejects = [
            'caring', 'inclusive', 'mental', 'emotional', 'physical', 'psychological',
            'professional', 'positive', 'negative', 'preparing', 'scheduling',
            'requirement', 'etc..', 'including', 'determination', 'optimism',
            'stewardship', 'ingenuity', 'responsibility', 'from', 'go', 'able'
        ]
        if skill_lower in single_word_rejects:
            return False

        # Reject if contains multiple spaces (likely sentence fragment)
        if '  ' in skill_lower:
            return False

        # Reject if word count is > 5 (likely sentence, not skill)
        if word_count > 5:
            return False

        # Reject phrases that are too descriptive (contain "and" in the middle)
        if ' and ' in skill_lower and word_count > 2:
            return False

        # Reject if it's too generic (single generic words under 5 chars)
        if word_count == 1 and len(skill_lower) < 5:
            generic_single = ['and', 'or', 'the', 'for', 'with', 'from', 'into', 'go']
            if skill_lower in generic_single:
                return False

        return True
