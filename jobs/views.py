from django.shortcuts import render

# Create your views here.
def search(request):
    return render(request, 'jobs/search.html')

def search_results(request):
    if request.method == 'POST':
        job_title = request.POST.get('job_title')
        skills = request.POST.get('skills')
        experience = request.POST.get('experience')
        education = request.POST.get('education')

        results = [
            {
                'job_title': job_title,
                'company': 'Demo Company',
                'match_score': 75,
                'missing_skills': ['Django', 'REST API']
            }
        ]
        return render(request, 'jobs/results.html', {'results': results})
    return render(request, 'jobs/search.html')