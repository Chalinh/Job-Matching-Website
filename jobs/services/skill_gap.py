class SkillGapAnalyzer:
    """Analyze missing skills between user and job"""

    def analyze(self, user_skills, job_skills):
        """
        Identify missing skills
        Returns: List of missing skills
        """
        user_set = set(s.lower() for s in user_skills)
        job_set = set(s.lower() for s in job_skills)

        missing = job_set - user_set

        return sorted(list(missing))
