# Intelligent Data Visualization System - Start Here

## What You Have

A complete, production-ready system that:
- Understands natural language queries
- Recommends optimal charts automatically
- Displays interactive visualizations
- Works entirely on your computer

## Quick Start (5 minutes)

### Terminal 1 - Backend (Python)
```bash
python -m venv venv
source venv/bin/activate          # Mac/Linux
# OR: venv\Scripts\activate        # Windows

pip install -r backend/requirements.txt
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Wait for: `Application startup complete`

### Terminal 2 - Frontend (React)
```bash
npm install
npm run dev
```

Wait for: `Ready in X.Xs`

### Browser
Visit: **http://localhost:3000**

Click example query → See chart!

## Documentation (Read in Order)

1. **INDEX.md** - Overview & navigation
2. **SETUP.md** - Detailed 8-step setup
3. **docs/QUICKSTART.md** - Command reference
4. **docs/ARCHITECTURE.md** - System design
5. **TROUBLESHOOTING.md** - Common issues
6. **README.md** - Project overview

## Project Structure

```
project/
├── backend/              Python FastAPI server
│   ├── api/             REST API endpoints
│   ├── nlp/             Query understanding
│   ├── recommender/     Chart selection rules
│   └── data_pipeline/   Data processing
├── app/                 React/Next.js frontend
│   ├── components/      UI components
│   ├── page.tsx         Main dashboard
│   └── globals.css      Styling
└── docs/                Documentation
```

## Key Features

- Natural language query understanding
- Intelligent chart recommendations (8+ chart types)
- Interactive visualizations with Recharts
- OECD agricultural dataset included
- Auto-reload on code changes
- Full error handling & logging

## Both Terminals Must Run

Keep both terminals open while developing. Changes auto-reload instantly.

- Backend restarts on file save
- Frontend refreshes on file save
- Browser updates automatically

## Example Queries

- "Show wheat production trends"
- "Compare maize production by country"
- "What are the top wheat regions?"
- "Production breakdown by commodity"

## Troubleshooting

See **TROUBLESHOOTING.md** for common issues and solutions.

## Technology Stack

- **Backend:** Python, FastAPI, spaCy-like NLP, Pandas
- **Frontend:** React, Next.js, TypeScript, Recharts
- **Data:** CSV, JSON
- **Styling:** Tailwind CSS

## Next Steps

1. Complete the 5-minute quick start above
2. Try example queries in the browser
3. Read SETUP.md for detailed configuration
4. Read ARCHITECTURE.md to understand the system
5. Edit code and watch changes reload
6. Customize as needed

---

**Everything is ready to use. Just follow the Quick Start above!**
