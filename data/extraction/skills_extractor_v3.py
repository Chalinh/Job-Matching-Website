"""Enhanced skills extractor with improved technical skills detection."""
from typing import List, Dict, Set
import json
from .config import EnhancedExtractionConfig, TECHNICAL_SKILLS_FILE
from .strategies.regex_matcher import RegexMatcher
from .strategies.section_parser import SectionParser
from .strategies.keybert_extractor import KeyBERTExtractor
from .strategies.ner_extractor import NERExtractor
from .postprocessing.normalizer import Normalizer
from .postprocessing.deduplicator import Deduplicator
from .postprocessing.validator import Validator

class EnhancedSkillsExtractor:
    """Enhanced orchestrator with improved technical skills detection."""

    def __init__(self, config: EnhancedExtractionConfig = None):
        """Initialize enhanced skills extractor."""
        self.config = config or EnhancedExtractionConfig()

        print("Initializing Enhanced Skills Extractor v3...")

        # Load technical skills for direct text scanning
        with open(TECHNICAL_SKILLS_FILE, 'r', encoding='utf-8') as f:
            skills_data = json.load(f)
        self.all_tech_skills = set()
        for category, skills in skills_data.items():
            self.all_tech_skills.update(skill.lower() for skill in skills)

        # Initialize strategies with enhanced config
        print("  Loading Strategy 1: Regex Matcher...")
        self.regex_matcher = RegexMatcher()

        print("  Loading Strategy 2: Section Parser...")
        self.section_parser = SectionParser(self.config)

        print("  Loading Strategy 3: Enhanced KeyBERT...")
        self.keybert_extractor = KeyBERTExtractor(self.config)

        print("  Loading Strategy 4: NER Extractor...")
        self.ner_extractor = NERExtractor(self.config)

        # Post-processing
        print("  Loading Post-processing modules...")
        self.normalizer = Normalizer()
        self.deduplicator = Deduplicator()
        self.validator = Validator(self.config)

        print("Enhanced Skills Extractor v3 ready!")

    def extract(self, text: str) -> List[str]:
        """
        Extract skills with enhanced technical skills detection.

        Returns:
            List of clean, deduplicated skills.
        """
        if not text:
            return []

        # Step 1: Run all extraction strategies
        results = {}

        results['regex'] = self.regex_matcher.extract(text)
        results['section'] = self.section_parser.extract(text)
        results['keybert'] = self.keybert_extractor.extract(text)
        results['ner'] = self.ner_extractor.extract(text)

        # Step 2: Enhanced direct scanning for missed technical skills
        results['direct_scan'] = self._direct_skill_scan(text)

        # Step 3: Extract soft skills
        results['soft_skills'] = self._extract_soft_skills(text)

        # Step 4: Aggregate results with enhanced priority
        aggregated_skills = self._aggregate_results(results)

        # Step 5: Post-processing pipeline
        normalized = self.normalizer.normalize(aggregated_skills)
        validated = self.validator.validate(normalized)
        deduplicated = self.deduplicator.deduplicate(validated)

        return deduplicated

    def _direct_skill_scan(self, text: str) -> List[str]:
        """
        Direct scanning for technical skills that might be missed.

        Looks for software names, tools, and technologies in parentheses,
        lists, and common patterns.
        """
        import re

        text_lower = text.lower()
        found = set()

        # Pattern 1: Skills in parentheses: "knowledge (Python, Java, SQL)"
        paren_pattern = r'\(([^)]{5,200})\)'
        paren_matches = re.findall(paren_pattern, text_lower)

        for match in paren_matches:
            # Split by common delimiters
            items = re.split(r'[,;&]', match)
            for item in items:
                item = item.strip()
                # Check if it's a known technical skill
                if item in self.all_tech_skills:
                    found.add(item)

        # Pattern 2: "Use X, Y, and Z" or "Able to use X"
        use_pattern = r'(?:use|using|able to use|proficiency in|knowledge of|experience with)\s+([a-z0-9\s,&+#.-]{5,100})(?:\.|,|;|$)'
        use_matches = re.findall(use_pattern, text_lower)

        for match in use_matches:
            items = re.split(r'[,;&]|\s+and\s+', match)
            for item in items:
                item = item.strip()
                if item in self.all_tech_skills and len(item) > 2:
                    found.add(item)

        # Pattern 3: Bullet point items that are technical skills
        # Already handled by section parser, but double-check
        bullet_pattern = r'(?:^|[\r\n])[\s\-\*•]\s*([a-z0-9\s+#.-]{2,40})(?:$|[\r\n])'
        bullet_matches = re.findall(bullet_pattern, text_lower, re.MULTILINE)

        for match in bullet_matches:
            match = match.strip()
            if match in self.all_tech_skills:
                found.add(match)

        # Pattern 4: Common software version patterns "Python 3", "Office 365"
        version_pattern = r'\b([a-z]+)\s+(?:\d+|365|office|suite)\b'
        version_matches = re.findall(version_pattern, text_lower)

        for match in version_matches:
            if match in self.all_tech_skills:
                found.add(match)

        return sorted(found)

    def _extract_soft_skills(self, text: str) -> List[str]:
        """Extract recognized soft skills."""
        text_lower = text.lower()
        found = set()

        for skill in self.config.SOFT_SKILLS:
            if skill in text_lower:
                found.add(skill)

        return sorted(found)

    def _aggregate_results(self, results: Dict[str, List[str]]) -> List[str]:
        """
        Aggregate results with enhanced priority scoring.

        Priority weights (higher = more reliable):
        - Regex match: 12 (highest - exact match from database)
        - Direct scan: 11 (very high - targeted extraction)
        - Section match: 9 (high - from structured sections)
        - KeyBERT: 6 (medium - semantic extraction)
        - NER: 5 (medium-low - entity recognition)
        - Soft skills: 4 (low - common but important)
        """
        skill_scores: Dict[str, int] = {}

        weights = {
            'regex': 12,
            'direct_scan': 11,
            'section': 9,
            'keybert': 6,
            'ner': 5,
            'soft_skills': 4
        }

        for strategy, skills in results.items():
            weight = weights.get(strategy, 1)
            for skill in skills:
                skill_lower = skill.lower()
                if skill_lower in skill_scores:
                    skill_scores[skill_lower] += weight
                else:
                    skill_scores[skill_lower] = weight

        # Return skills sorted by score (but we'll sort alphabetically later)
        return list(skill_scores.keys())

    def extract_batch(self, texts: List[str]) -> List[List[str]]:
        """Extract skills from multiple texts."""
        return [self.extract(text) for text in texts]

    def get_extraction_stats(self, text: str) -> Dict:
        """Get detailed statistics about extraction process."""
        results = {}
        results['regex'] = self.regex_matcher.extract(text)
        results['section'] = self.section_parser.extract(text)
        results['keybert'] = self.keybert_extractor.extract(text)
        results['ner'] = self.ner_extractor.extract(text)
        results['direct_scan'] = self._direct_skill_scan(text)
        results['soft_skills'] = self._extract_soft_skills(text)

        aggregated = self._aggregate_results(results)
        normalized = self.normalizer.normalize(aggregated)
        validated = self.validator.validate(normalized)
        final = self.deduplicator.deduplicate(validated)

        return {
            'strategy_results': {
                'regex': len(results['regex']),
                'section': len(results['section']),
                'keybert': len(results['keybert']),
                'ner': len(results['ner']),
                'direct_scan': len(results['direct_scan']),
                'soft_skills': len(results['soft_skills'])
            },
            'pipeline_stages': {
                'aggregated': len(aggregated),
                'normalized': len(normalized),
                'validated': len(validated),
                'final': len(final)
            },
            'final_skills': final,
            'by_strategy': results
        }
