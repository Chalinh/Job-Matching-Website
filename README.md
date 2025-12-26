# 🎯 Job Matching Website

A smart, **guest-only** job matching system that uses AI to match user profiles with 3,680 real job postings. No login required - just search and find your perfect job!

## ✨ Features

- 🚫 **No Authentication** - Direct access to search (guest-only)
- 🤖 **AI-Powered Matching** - Hybrid exact + semantic skill matching
- 📊 **Weighted Scoring** - Skills 40%, Education 25%, Experience 20%, Language 10%, Location 5%
- 🎯 **Top 5 Results** - Shows only the best matches
- 📈 **Skill Gap Analysis** - See what skills you need to develop
- 🎨 **Beautiful UI** - Modern Tailwind CSS design
- 🗄️ **SQLite Database** - Simple, no installation required, production-ready
- ⚡ **Fast Matching** - Semantic search with sentence transformers

---

## 🚀 Super Quick Start (2 Minutes!)

### Prerequisites

**Only Python 3.x** - That's it! No database installation needed.

### Setup Commands

```bash
# 1. Activate virtual environment
cd d:\Job-Matching-Website
venv\Scripts\activate

# 2. Create database tables
python manage.py migrate

# 3. Load 3,680 job postings
python manage.py load_jobs

# 4. Start the server
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

**Done!** ✅

---

## 📖 What Just Happened?

1. **`migrate`** - Created SQLite database (`db.sqlite3`) and tables automatically
2. **`load_jobs`** - Loaded 3,680 normalized job postings from JSON
3. **`runserver`** - Started Django development server

No PostgreSQL, no manual SQL, no complicated setup!

---

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | 🚀 Complete deployment guide for production |
| **[SIMPLE_SETUP.md](SIMPLE_SETUP.md)** | ⚡ Super simple SQLite setup (2 minutes!) |
| **[PROJECT_STATUS.md](PROJECT_STATUS.md)** | 📊 Full system architecture & troubleshooting |

---

## 🛠️ Management Commands

### Data Management
```bash
# Load jobs from JSON
python manage.py load_jobs

# Create/apply migrations (creates tables via code)
python manage.py makemigrations
python manage.py migrate
```

### Subsequent Runs
```bash
# Just activate and run
venv\Scripts\activate
python manage.py runserver
```

---

## 📊 Database Info

- **Type**: SQLite3 (built into Python, production-ready)
- **File**: `db.sqlite3` (created automatically)
- **Jobs**: 1,777 normalized postings
- **Size**: ~15 MB after loading data
- **Performance**: Excellent for job search applications

---

**Built with**: Django, SQLite, Sentence Transformers, Tailwind CSS

**Status**: Production Ready ✅ | Zero Configuration 🎉 | Just Run It! 🚀

⚡ **Launch in 2 minutes!**
