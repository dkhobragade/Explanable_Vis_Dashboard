# Project Documentation Index

## Essential Documentation

### 1. **SETUP.md** - Start Here
Complete setup guide for running the project locally in VS Code.
- Prerequisites installation
- Step-by-step backend setup (Python)
- Step-by-step frontend setup (React)
- Development workflow
- Troubleshooting common issues

**When to read:** Before running the project for the first time

---

### 2. **docs/QUICKSTART.md** - Commands Only
Quick reference for copy-paste commands.
- Minimal setup steps
- Backend commands
- Frontend commands
- Example API calls

**When to read:** If you just need the commands

---

### 3. **docs/ARCHITECTURE.md** - System Design
Deep dive into how the system works.
- System components
- Data flow diagram
- Module descriptions
- How queries are processed
- Recommendation logic

**When to read:** To understand the system structure and design patterns

---

### 4. **TROUBLESHOOTING.md** - Error Fixes
Solutions for common problems.
- Backend setup errors
- Frontend errors
- Port conflicts
- API connection issues
- Data problems

**When to read:** When you encounter errors

---

### 5. **README.md** - Project Overview
High-level project description.
- What the system does
- Key features
- Technology stack
- Basic usage

**When to read:** To understand what the project is about

---

## Project Structure

```
project-root/
├── SETUP.md                    ← START HERE
├── INDEX.md                    (this file)
├── README.md                   (project overview)
├── TROUBLESHOOTING.md          (common issues)
├── backend/                    (Python FastAPI)
│   ├── api/                   (REST endpoints)
│   ├── nlp/                   (query parsing)
│   ├── recommender/           (chart selection)
│   ├── data_pipeline/         (data processing)
│   ├── data/                  (OECD dataset)
│   └── requirements.txt       (dependencies)
├── app/                        (React/Next.js)
│   ├── page.tsx               (main page)
│   ├── components/            (React components)
│   └── globals.css            (styling)
├── docs/
│   ├── QUICKSTART.md          (command reference)
│   └── ARCHITECTURE.md        (system design)
└── package.json               (Node dependencies)
```

---

## Quick Start (5 Steps)

1. **Read:** SETUP.md
2. **Terminal 1:** `python -m venv venv && source venv/bin/activate && pip install -r backend/requirements.txt && python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload`
3. **Terminal 2:** `npm install && npm run dev`
4. **Browser:** http://localhost:3000
5. **Click:** Example query

---

## Development Workflow

1. **Edit** files in `backend/` or `app/`
2. **Save** with Ctrl+S
3. **Backend auto-restarts**, Frontend **auto-refreshes**
4. **See changes** immediately in browser

---

## Key Files to Edit

### Backend (Python)
- `backend/api/routes/query.py` - Query endpoint
- `backend/recommender/rules.py` - Chart selection
- `backend/nlp/parser.py` - Query understanding
- `backend/data/oecd_*.csv` - Your data

### Frontend (React)
- `app/page.tsx` - Main page
- `app/components/QueryInput.tsx` - Input
- `app/components/ChartDisplay.tsx` - Charts
- `app/globals.css` - Styling

---

## Both Terminals Must Run

```
Terminal 1: Python Backend (port 8000)
Terminal 2: React Frontend (port 3000)
Browser: http://localhost:3000
```

Keep both running while developing. Never close both at once.

---

## Getting Help

1. **How do I set it up?** → Read **SETUP.md**
2. **What are the commands?** → Read **docs/QUICKSTART.md**
3. **I'm getting an error** → Read **TROUBLESHOOTING.md**
4. **How does it work?** → Read **docs/ARCHITECTURE.md**
5. **What is this project?** → Read **README.md**

---

## File Locations

| What | Where |
|------|-------|
| Setup instructions | SETUP.md |
| Quick commands | docs/QUICKSTART.md |
| System design | docs/ARCHITECTURE.md |
| Troubleshooting | TROUBLESHOOTING.md |
| Project overview | README.md |
| Python backend | backend/ |
| React frontend | app/ |
| Data | backend/data/ |

---

**Everything is documented. Start with SETUP.md and follow the steps.**
