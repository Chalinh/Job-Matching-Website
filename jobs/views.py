from django.shortcuts import render
from .forms import JobSearchForm
from .services.matcher import JobMatcher
from .models import UserProfile, UserSkill, UserLanguage


def search(request):
    """Display job search form"""
    form = JobSearchForm()
    return render(request, 'search.html', {'form': form})


def search_results(request):
    """Process search and display matched jobs"""
    if request.method == 'POST':
        form = JobSearchForm(request.POST)

        if form.is_valid():
            # Create temporary user profile (not saved to database)
            temp_profile = UserProfile(
                years_of_experience=form.cleaned_data.get('years_of_experience', 0),
                current_job_title=form.cleaned_data.get('current_job_title', ''),
                education_level=form.cleaned_data.get('education_level', ''),
                education_major=form.cleaned_data.get('education_major', ''),
                preferred_location=form.cleaned_data.get('preferred_location', ''),
                willing_to_relocate=form.cleaned_data.get('willing_to_relocate', False)
            )

            # Create temporary skill and language objects
            temp_skills = [
                UserSkill(skill_name=skill)
                for skill in form.cleaned_data.get('skills', [])
            ]

            temp_languages = [
                UserLanguage(
                    language_name=lang['name'],
                    proficiency=lang['level']
                )
                for lang in form.cleaned_data.get('languages', [])
            ]

            # Create a simple wrapper class to mimic Django's RelatedManager
            class TempRelatedManager:
                def __init__(self, items):
                    self._items = items

                def all(self):
                    return self._items

            # Add temp managers to profile
            temp_profile.skills = TempRelatedManager(temp_skills)
            temp_profile.languages = TempRelatedManager(temp_languages)

            # Initialize JobMatcher and find matches (top 5 results)
            # Database-only operation
            matcher = JobMatcher()
            matches = matcher.match(temp_profile, top_n=5)

            # Format results for template
            results = []
            for match in matches:
                job = match['job']
                results.append({
                    'job_id': job['job_id'],
                    'job_title': job['job_title'],
                    'company': job.get('company', 'N/A'),
                    'location': job.get('location', 'N/A'),
                    'match_score': round(match['match_score'] * 100, 1),  # Convert to percentage
                    'skill_score': round(match['skill_score'] * 100, 1),
                    'education_score': round(match['education_score'] * 100, 1),
                    'experience_score': round(match['experience_score'] * 100, 1),
                    'language_score': round(match['language_score'] * 100, 1),
                    'location_score': round(match['location_score'] * 100, 1),
                    'missing_skills': match['missing_skills'],
                    'required_experience': job['experience']['min_years'],
                    'education_level': job['education'].get('level', 'N/A'),
                    'education_major': job['education'].get('major', 'N/A'),
                })

            return render(request, 'results.html', {
                'results': results,
                'total_matches': len(results)
            })

    # If not POST or form invalid, redirect to search
    form = JobSearchForm()
    return render(request, 'search.html', {'form': form})