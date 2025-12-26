"""Text processing utility functions."""
import re
from typing import List

def normalize_text(text: str) -> str:
    """Normalize text: lowercase, strip whitespace, clean special chars."""
    if not text:
        return ""

    # Lowercase
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)

    # Strip
    text = text.strip()

    return text

def clean_skill(skill: str) -> str:
    """Clean individual skill string."""
    if not skill:
        return ""

    # Remove special characters except alphanumeric, space, hyphen, slash, dot, +, #
    skill = re.sub(r'[^\w\s\-/\.+#&]', '', skill)

    # Remove extra whitespace
    skill = re.sub(r'\s+', ' ', skill)

    # Strip
    skill = skill.strip()

    return skill

def extract_section(text: str, section_headers: List[str]) -> str:
    """Extract content from specific sections (e.g., 'Skills:', 'Requirements:')."""
    text_lower = text.lower()

    for header in section_headers:
        pattern = rf"{re.escape(header)}\s*:?\s*([^\n]*(?:\n(?![\w\s]+:)[^\n]*)*)"
        match = re.search(pattern, text_lower, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1)

    return ""

def parse_bullet_points(text: str) -> List[str]:
    """Parse bullet points from text."""
    items = []

    # Split by common bullet point markers and newlines
    lines = re.split(r'[\n\r]+', text)

    for line in lines:
        # Remove bullet markers
        line = re.sub(r'^[\s\-\*•\d\.]+\s*', '', line)
        line = line.strip()

        if line:
            # Also split by semicolons and commas for inline lists
            sub_items = re.split(r'[;,]', line)
            items.extend([item.strip() for item in sub_items if item.strip()])

    return items

def is_likely_skill(text: str) -> bool:
    """Heuristic to check if text is likely a skill name."""
    if not text or len(text) < 2:
        return False

    # Too long to be a skill name
    if len(text) > 50:
        return False

    # Contains too many common words (likely a sentence)
    common_words = ['the', 'and', 'or', 'for', 'with', 'in', 'to', 'of', 'a', 'an']
    word_count = sum(1 for word in text.split() if word in common_words)
    if word_count > 2:
        return False

    # Contains verbs (likely a sentence)
    verb_indicators = ['will', 'can', 'must', 'should', 'able to', 'required to']
    if any(verb in text for verb in verb_indicators):
        return False

    return True
