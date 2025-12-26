"""Strategy 2: Section-based parsing for structured job postings."""
import json
import re
from typing import List, Set
from ..config import TECHNICAL_SKILLS_FILE, EnhancedExtractionConfig
from ..utils.text_utils import extract_section, parse_bullet_points, is_likely_skill, clean_skill

class SectionParser:
    """Extract skills from specific sections like 'Skills:', 'Requirements:', etc."""

    def __init__(self, config: EnhancedExtractionConfig = None):
        """Initialize section parser."""
        self.config = config or EnhancedExtractionConfig()
        self.section_headers = [
            'skills', 'required skills', 'technical skills', 'key skills',
            'requirements', 'required', 'qualifications', 'required qualifications',
            'must have', 'responsibilities', 'job requirements',
            'essential skills', 'core skills'
        ]

        # Load technical skills for validation
        with open(TECHNICAL_SKILLS_FILE, 'r', encoding='utf-8') as f:
            skills_data = json.load(f)
        self.tech_skills = set()
        for category, skills in skills_data.items():
            self.tech_skills.update(skill.lower() for skill in skills)

    def extract(self, text: str) -> List[str]:
        """Extract skills from structured sections."""
        if not text:
            return []

        found_skills = set()

        # Extract from each potential section
        for header in self.section_headers:
            section_text = extract_section(text, [header])
            if section_text:
                # Parse bullet points and list items
                items = parse_bullet_points(section_text)

                for item in items:
                    item = clean_skill(item)

                    # Filter by length
                    if len(item) < self.config.SECTION_MIN_LENGTH:
                        continue
                    if len(item) > self.config.SECTION_MAX_LENGTH:
                        continue

                    # Check if it's likely a skill
                    if is_likely_skill(item):
                        # Prefer if in technical skills database
                        if item in self.tech_skills:
                            found_skills.add(item)
                        # Or if it's short and concise (likely a skill name)
                        elif len(item) <= 30 and len(item.split()) <= 4:
                            found_skills.add(item)

        return sorted(found_skills)

    def extract_batch(self, texts: List[str]) -> List[List[str]]:
        """Batch extraction."""
        return [self.extract(text) for text in texts]
