from django.db import models


class Job(models.Model):
    """Normalized job posting (loaded from JSON)"""
    job_id = models.CharField(max_length=50, unique=True, db_index=True)
    job_title = models.CharField(max_length=200, db_index=True)
    company = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True, db_index=True)
    industry = models.CharField(max_length=100, blank=True)

    # Experience
    min_years_experience = models.IntegerField(default=0)

    # Education
    education_level = models.CharField(max_length=50, blank=True)
    education_major = models.CharField(max_length=100, blank=True)

    # JSON fields
    skills = models.JSONField(default=list)  # ["python", "django"]
    languages = models.JSONField(default=list)  # [{"name": "english", "level": "good"}]

    # Metadata
    raw_text = models.TextField(blank=True)
    pubdate = models.DateTimeField(null=True, blank=True)
    expdate = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_id}: {self.job_title}"

    class Meta:
        db_table = 'jobs'
        ordering = ['-pubdate']


# Temporary models for matching (not stored in database)
class UserProfile:
    """Temporary user profile for matching"""
    def __init__(self, years_of_experience=0, current_job_title='',
                 education_level='', education_major='',
                 preferred_location='', willing_to_relocate=False):
        self.years_of_experience = years_of_experience
        self.current_job_title = current_job_title
        self.education_level = education_level
        self.education_major = education_major
        self.preferred_location = preferred_location
        self.willing_to_relocate = willing_to_relocate


class UserSkill:
    """Temporary user skill for matching"""
    def __init__(self, skill_name, proficiency='intermediate'):
        self.skill_name = skill_name
        self.proficiency = proficiency


class UserLanguage:
    """Temporary user language for matching"""
    def __init__(self, language_name, proficiency):
        self.language_name = language_name
        self.proficiency = proficiency
