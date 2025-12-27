# Job Matching Website - Features Documentation

## Table of Contents
1. [Overview](#overview)
2. [Core Features](#core-features)
3. [Technical Architecture](#technical-architecture)
4. [Matching Algorithm](#matching-algorithm)
5. [User Features](#user-features)
6. [Database Schema](#database-schema)
7. [Deployment & Performance](#deployment--performance)

---

## Overview

The **Job Matching Website** is an intelligent job recommendation platform that uses advanced machine learning and semantic analysis to match job seekers with relevant job postings. The system analyzes multiple dimensions of compatibility including skills, education, experience, languages, and location preferences.

### Key Highlights
- ✅ **AI-Powered Matching**: Uses sentence transformers for semantic skill matching
- ✅ **Multi-Factor Scoring**: Considers 5+ factors for comprehensive job matching
- ✅ **Skill Gap Analysis**: Identifies missing skills and provides learning recommendations
- ✅ **Real-time Matching**: Instant job recommendations based on user profiles
- ✅ **PostgreSQL Database**: Scalable database with efficient querying
- ✅ **Production-Ready**: Deployed on Render with optimized performance

---

## Core Features

### 1. **Intelligent Job Matching Engine**

The heart of the system is a sophisticated matching algorithm that evaluates job compatibility across multiple dimensions.

#### Matching Components:

**a) Skill Matching (60% weight)**
- **Exact Matching**: Direct string comparison for exact skill names
- **Semantic Matching**: AI-powered understanding of similar skills
  - Example: "Python" matches with "Python Programming", "Django", "Flask"
  - Uses `sentence-transformers/all-MiniLM-L6-v2` model
  - Cosine similarity threshold: 0.7 for semantic matches
- **Scoring Algorithm**:
  ```
  skill_score = (exact_matches + 0.7 * semantic_matches) / total_job_skills
  ```

**b) Education Matching (20% weight)**
- **Level Matching**:
  - Exact match: 100%
  - Higher qualification: 80%
  - Lower qualification: 50%
- **Major Matching**:
  - Same major: +20% bonus
  - Related major (e.g., "Computer Science" ↔ "Software Engineering"): +10% bonus
- Supports levels: High School, Associate, Bachelor, Master, PhD

**c) Experience Matching (15% weight)**
- **Perfect Match**: User experience ≥ job requirement = 100%
- **Slight Under-qualification**: Within 1 year = 80%
- **Moderate Gap**: 1-3 years under = 60%
- **Significant Gap**: 3-5 years under = 40%
- **Major Gap**: 5+ years under = 20%
- **Over-qualification**: Bonus scoring for extra experience

**d) Language Matching (3% weight)**
- Supports proficiency levels: Basic, Intermediate, Advanced, Native
- Weighted scoring based on proficiency match:
  - Exact level match: 100%
  - One level difference: 75%
  - Two levels difference: 50%
  - Three levels difference: 25%

**e) Location Matching (2% weight)**
- **Exact Location Match**: 100%
- **Same City/Region**: 80%
- **Willing to Relocate**: 60%
- **Remote Opportunities**: Highest priority

---

### 2. **Skill Gap Analysis**

Provides actionable insights for career development.

**Features:**
- Identifies missing skills required for target jobs
- Categorizes skills by importance (required vs. preferred)
- Prioritizes learning based on job market demand
- Suggests skill development paths

**Example Output:**
```
Missing Skills for "Senior Python Developer":
  Critical:
    - Docker (required by 85% of matches)
    - Kubernetes (required by 70% of matches)

  Recommended:
    - AWS (nice to have)
    - GraphQL (emerging skill)
```

---

### 3. **User Profile Management**

**Profile Components:**
- **Personal Information**:
  - Name, email, phone
  - Location preferences
  - Relocation willingness

- **Skills**:
  - Skill name
  - Proficiency level (1-5 scale)
  - Years of experience with skill

- **Education**:
  - Degree level
  - Major/Field of study
  - Institution name
  - Graduation year

- **Experience**:
  - Total years of professional experience
  - Industry preferences
  - Job title preferences

- **Languages**:
  - Language name
  - Proficiency level (Basic → Native)

---

### 4. **Job Search & Filtering**

**Pre-filtering System:**
- Reduces search space from 10,000+ jobs to ~500 candidates
- Filters applied:
  1. **Location Filter**: Matches preferred location (if not willing to relocate)
  2. **Experience Filter**: User experience ≥ (job requirement - 2 years)
  3. **Skill Overlap Filter**: At least 1 common skill
  4. **Industry Filter**: Matches user's industry preferences (if specified)

**Benefits:**
- ⚡ Faster matching (processes 500 vs 10,000 jobs)
- 🎯 More relevant results
- 💰 Lower computational cost

---

### 5. **Job Recommendations**

**Output Format:**
Each recommendation includes:
- **Match Score**: Overall compatibility (0-100%)
- **Component Scores**: Breakdown by category
  - Skill match: X%
  - Education match: Y%
  - Experience match: Z%
  - Language match: W%
  - Location match: V%
- **Missing Skills**: List of skills to acquire
- **Job Details**:
  - Job title
  - Company name
  - Location
  - Required skills
  - Education requirements
  - Experience requirements
  - Languages required
  - Post date & expiration date

**Ranking:**
- Top 20 matches displayed by default
- Sorted by match score (descending)
- Minimum match threshold: 30%

---

## Technical Architecture

### Tech Stack

**Backend:**
- **Framework**: Django 6.0
- **Database**: PostgreSQL 13+ (production) / SQLite3 (development)
- **Web Server**: Gunicorn with custom configuration
- **Static Files**: WhiteNoise

**Machine Learning:**
- **Library**: sentence-transformers
- **Model**: `all-MiniLM-L6-v2` (384-dimensional embeddings)
- **Framework**: PyTorch 2.0+
- **Computation**: NumPy for vector operations

**Frontend:**
- Django Templates
- Bootstrap 5 (responsive design)
- Vanilla JavaScript (for interactivity)

**Deployment:**
- **Platform**: Render
- **Environment**: Python 3.11+
- **Process Manager**: Gunicorn
- **Database**: Managed PostgreSQL

---

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│              (Django Templates + Bootstrap)                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Django Views Layer                       │
│              (UserProfile CRUD, Job Matching)                │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Matching Engine Layer                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ SkillScorer  │  │ EduScorer    │  │ ExpScorer    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐                         │
│  │ LangScorer   │  │ LocScorer    │                         │
│  └──────────────┘  └──────────────┘                         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  ML/AI Services Layer                        │
│  ┌────────────────────────────────────────────────┐         │
│  │   EmbeddingService (Singleton Pattern)         │         │
│  │   - Lazy loading                                │         │
│  │   - SentenceTransformer model caching          │         │
│  │   - Cosine similarity computation               │         │
│  └────────────────────────────────────────────────┘         │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Database Layer                           │
│              PostgreSQL with Django ORM                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │   Jobs   │  │  Users   │  │ Skills   │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
└─────────────────────────────────────────────────────────────┘
```

---

### Performance Optimizations

**1. Lazy Model Loading**
- ML models load only on first use (not during startup)
- Prevents memory spikes and worker timeouts
- Singleton pattern ensures single model instance

**2. Database Query Optimization**
- Pre-filtering reduces matching candidates by 95%
- Indexed fields for faster lookups
- Batch queries using Django ORM select_related/prefetch_related

**3. Gunicorn Configuration**
- **Workers**: 1 (memory-optimized for ML models)
- **Threads**: 2 (concurrent request handling)
- **Timeout**: 300 seconds (allows model loading)
- **Max Requests**: 100 (prevents memory leaks)
- **Worker Recycling**: Automatic restart after threshold

**4. Static File Serving**
- WhiteNoise middleware for efficient static file serving
- Compressed manifest storage
- CDN-ready configuration

---

## Database Schema

### Models Overview

#### 1. **UserProfile**
Stores job seeker information and preferences.

```python
UserProfile:
  - user (OneToOne → Django User)
  - phone
  - preferred_location
  - willing_to_relocate (Boolean)
  - years_of_experience (Integer)
  - education_level (Choice)
  - education_major
  - created_at
  - updated_at

Relations:
  - skills (Many-to-Many → UserSkill)
  - languages (Many-to-Many → UserLanguage)
```

#### 2. **UserSkill**
Represents user's skills and proficiency.

```python
UserSkill:
  - user_profile (ForeignKey → UserProfile)
  - skill_name
  - proficiency_level (1-5)
  - years_of_experience
```

#### 3. **UserLanguage**
Stores user's language capabilities.

```python
UserLanguage:
  - user_profile (ForeignKey → UserProfile)
  - language_name
  - proficiency (Basic/Intermediate/Advanced/Native)
```

#### 4. **Job**
Contains job posting information.

```python
Job:
  - job_id (Primary Key)
  - job_title
  - company
  - location
  - industry
  - min_years_experience
  - education_level
  - education_major
  - skills (JSONField - Array)
  - languages (JSONField - Array)
  - raw_text (Full job description)
  - pubdate (Publication date)
  - expdate (Expiration date)
  - created_at
  - updated_at
```

**Indexes:**
- `job_id` (Primary key)
- `location` (B-tree index)
- `min_years_experience` (B-tree index)
- `skills` (GIN index for JSONB - PostgreSQL)

---

## Matching Algorithm

### Detailed Flow

```
1. User submits profile
   ↓
2. Pre-filter jobs (500 candidates from 10k+ jobs)
   - Location match
   - Experience match
   - Skill overlap check
   ↓
3. For each candidate job:
   a. Compute skill score (exact + semantic)
   b. Compute education score
   c. Compute experience score
   d. Compute language score
   e. Compute location score
   ↓
4. Calculate weighted match score:
   score = (0.60 * skill) + (0.20 * edu) +
           (0.15 * exp) + (0.03 * lang) +
           (0.02 * loc)
   ↓
5. Analyze skill gaps
   - Missing required skills
   - Missing preferred skills
   ↓
6. Sort by match score (descending)
   ↓
7. Return top 20 matches
```

### Semantic Matching Example

**User Skills**: `["Python", "Django", "SQL"]`

**Job Skills**: `["Python Programming", "Web Development", "Database Management", "Docker"]`

**Matching Process**:
1. **Exact Matches**:
   - "Python" ≈ "Python Programming" → Semantic match (similarity: 0.85)

2. **Semantic Matches**:
   - "Django" ≈ "Web Development" → Semantic match (similarity: 0.72)
   - "SQL" ≈ "Database Management" → Semantic match (similarity: 0.78)

3. **Missing Skills**:
   - "Docker" → No match (recommended to learn)

**Final Skill Score**: `(1 * 1.0 + 2 * 0.7) / 4 = 0.60 = 60%`

---

## User Features

### 1. Profile Creation
- Create comprehensive user profile
- Add/edit/delete skills
- Add/edit/delete languages
- Specify location and relocation preferences

### 2. Job Matching
- One-click job matching
- View top 20 recommended jobs
- See detailed match breakdown
- Understand why each job was recommended

### 3. Skill Gap Analysis
- Identify missing skills for target jobs
- Get prioritized learning recommendations
- Track skill development progress

### 4. Job Details View
- Full job description
- Company information
- Required qualifications
- Application deadline

---

## Deployment & Performance

### Production Configuration

**Render Deployment Settings:**
```yaml
Build Command: ./build.sh
Start Command: gunicorn config.wsgi:application --config gunicorn.conf.py

Environment Variables:
  - SECRET_KEY: [Generated secure key]
  - DEBUG: False
  - DATABASE_URL: [PostgreSQL connection string]
  - ALLOWED_HOSTS: [Render domain]
  - RENDER_EXTERNAL_HOSTNAME: [Render URL]
```

**Gunicorn Settings:**
- Bind: `0.0.0.0:$PORT`
- Workers: 1 (optimized for ML workloads)
- Threads: 2
- Timeout: 300 seconds
- Max Requests: 100 (worker recycling)
- Preload App: False (lazy loading)

### Performance Metrics

**Expected Performance:**
- First request: 20-30 seconds (model loading)
- Subsequent requests: 2-5 seconds
- Matching 500 candidates: ~3 seconds
- Memory usage: ~800MB-1.2GB (with ML model loaded)
- Database queries: ~5-10 per match request

### Scalability Considerations

**Current Limitations:**
- Single worker (memory constraints)
- ML model loading time
- In-memory model caching

**Recommended Upgrades:**
- **Render Standard Plan**: 2GB RAM for better performance
- **Redis Caching**: Cache embedding computations
- **Background Jobs**: Celery for async matching
- **Model Optimization**: Quantize model for smaller size

---

## API Endpoints (Internal)

### User Profile Management
- `GET /profile/` - View user profile
- `POST /profile/create/` - Create new profile
- `POST /profile/edit/` - Update profile
- `POST /profile/skills/add/` - Add skill
- `POST /profile/skills/delete/<id>/` - Remove skill

### Job Matching
- `GET /jobs/match/` - Get job recommendations
- `GET /jobs/<job_id>/` - View job details
- `GET /jobs/` - Browse all jobs

---

## Security Features

### Production Security
- ✅ Secret key stored in environment variables
- ✅ Debug mode disabled in production
- ✅ ALLOWED_HOSTS whitelist
- ✅ CSRF protection enabled
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection (template escaping)
- ✅ Secure database connections (SSL)

### Environment Variables
All sensitive data stored in `.env` file (not committed to git):
```
SECRET_KEY=<django-secret-key>
DATABASE_URL=<postgresql-connection-string>
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

---

## Future Enhancements

### Planned Features
1. **User Authentication & Authorization**
   - Job seeker accounts
   - Employer accounts
   - Role-based access control

2. **Application Tracking**
   - Track applied jobs
   - Application status updates
   - Interview scheduling

3. **Advanced Filtering**
   - Salary range filtering
   - Company size preferences
   - Remote/hybrid/onsite filtering

4. **Resume Parsing**
   - Upload PDF/DOCX resume
   - Auto-populate profile fields
   - Skill extraction from resume

5. **Email Notifications**
   - New job matches
   - Application status updates
   - Weekly job recommendations

6. **Analytics Dashboard**
   - Profile views
   - Application success rate
   - Skill market demand trends

7. **Employer Portal**
   - Post job listings
   - Search candidates
   - Applicant tracking system

---

## Troubleshooting

### Common Issues

**1. Memory Errors (Worker Timeout)**
- **Cause**: ML models consuming too much memory
- **Solution**: Upgrade Render plan or disable semantic matching

**2. Slow First Request**
- **Cause**: ML model loading on first use
- **Solution**: Expected behavior, subsequent requests are fast

**3. No Job Matches**
- **Cause**: Profile criteria too strict
- **Solution**: Enable "willing to relocate" or broaden skill set

**4. Database Connection Error**
- **Cause**: Missing DATABASE_URL environment variable
- **Solution**: Set DATABASE_URL in Render dashboard

---

## Contributing

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/Job-Matching-Website.git
cd Job-Matching-Website

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### Running Tests
```bash
python manage.py test jobs
```

---

## License

This project is for educational purposes. See LICENSE file for details.

---

## Contact & Support

For questions or issues:
- GitHub Issues: [Create an issue](https://github.com/yourusername/Job-Matching-Website/issues)
- Email: your-email@example.com

---

**Last Updated**: December 2025
**Version**: 1.0.0
