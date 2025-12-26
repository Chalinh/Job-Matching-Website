"""Deduplication module to remove redundant and overlapping skills."""
import json
from typing import List, Set, Dict
from ..config import SYNONYMS_FILE

class Deduplicator:
    """Remove duplicate, substring, and synonym skills."""

    def __init__(self):
        """Initialize with synonym mappings."""
        self.synonyms: Dict[str, List[str]] = {}
        self._load_synonyms()

    def _load_synonyms(self):
        """Load synonym mappings."""
        try:
            with open(SYNONYMS_FILE, 'r', encoding='utf-8') as f:
                self.synonyms = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Synonyms file not found at {SYNONYMS_FILE}")

    def deduplicate(self, skills: List[str]) -> List[str]:
        """Remove duplicates, substrings, and merge synonyms."""
        if not skills:
            return []

        # Step 1: Remove exact duplicates (case-insensitive)
        unique_skills = list(set(skill.lower() for skill in skills))

        # Step 2: Merge synonyms
        merged_skills = self._merge_synonyms(unique_skills)

        # Step 3: Remove substring duplicates
        deduplicated = self._remove_substrings(merged_skills)

        return sorted(deduplicated)

    def _merge_synonyms(self, skills: List[str]) -> List[str]:
        """Merge synonyms to canonical form."""
        merged = set()
        skill_set = set(skills)

        for skill in skills:
            # Check if this skill is in synonyms mapping
            canonical = None

            for main_term, synonyms in self.synonyms.items():
                if skill == main_term.lower():
                    canonical = main_term.lower()
                    break
                elif skill in [syn.lower() for syn in synonyms]:
                    canonical = main_term.lower()
                    break

            # Use canonical form if found, otherwise keep original
            if canonical:
                merged.add(canonical)
            else:
                merged.add(skill)

        return list(merged)

    def _remove_substrings(self, skills: List[str]) -> List[str]:
        """Remove skills that are substrings of other skills."""
        if not skills:
            return []

        # Sort by length (descending) to keep longer, more specific skills
        sorted_skills = sorted(skills, key=len, reverse=True)
        kept_skills = []

        for i, skill in enumerate(sorted_skills):
            is_substring = False

            # Check if this skill is a substring of any longer skill
            for longer_skill in sorted_skills[:i]:
                # Check if skill is a substring (with word boundaries)
                if skill in longer_skill and skill != longer_skill:
                    # Additional check: ensure it's actually a meaningful substring
                    # e.g., "python" in "python programming" - keep longer
                    # but "sales" and "sales manager" - keep both (different meanings)
                    words_skill = set(skill.split())
                    words_longer = set(longer_skill.split())

                    # If all words from shorter skill are in longer skill, it's a substring
                    if words_skill.issubset(words_longer):
                        is_substring = True
                        break

            if not is_substring:
                kept_skills.append(skill)

        return kept_skills
