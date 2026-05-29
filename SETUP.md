# Setup Guide - Intelligent Data Visualization System

## Prerequisites

Install these once:
- **Python 3.8+** - https://www.python.org/downloads/
- **Node.js 16+** - https://nodejs.org/
- **VS Code** - https://code.visualstudio.com/

Verify installation:
```bash
python3 --version
node --version
npm --version
```

---

## Step 1: Download Project

From v0:
1. Click three dots menu (top right)
2. Select "Download ZIP"
3. Extract to your desired location
4. Open folder in VS Code: `File → Open Folder`

---

## Step 2: Setup Backend (Python)

Open terminal in VS Code: `Ctrl + `` (backtick)

### Create Virtual Environment
```bash
python -m venv venv
```

### Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line.

### Install Dependencies
```bash
pip3 install -r backend/requirements.txt
```

### Test Backend Setup
```bash
python3 backend/test_backend.py
```

You should see green checkmarks and "All tests passed successfully!"

---

## Step 3: Start Backend Server

Keep same terminal, run:
```bash
python3 -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Wait for:
```
Application startup complete
```

**⚠️ IMPORTANT:** Keep this terminal running. Don't close it.

---

## Step 4: Open Second Terminal for Frontend

In VS Code, click the `+` button next to "Terminal" at bottom

OR press: `Ctrl + Shift + `` (backtick)

---

## Step 5: Setup Frontend (React/Node)

In Terminal 2, run:
```bash
npm install
```

Wait 2-3 minutes for completion.

---

## Step 6: Start Frontend Server

In Terminal 2, run:
```bash
npm run dev
```

Wait for:
```
Ready in X.Xs
➜ Local: http://localhost:3000
```

**⚠️ IMPORTANT:** Keep this terminal running too.

---

## Step 7: Open in Browser

Go to: **http://localhost:3000**

You should see:
- Dark theme dashboard
- Input box: "What would you like to analyze?"
- Example queries below

---

## Step 8: Test It Works

Click an example query:
```
"Show wheat production trends"
```

You should see:
- Loading spinner
- Line chart appears
- Explanation below
- Data summary

**✅ If you see the chart: SUCCESS!**

---

## Development Workflow

### Making Changes

**Backend (Python):**
1. Edit file in `backend/`
2. Save: `Ctrl+S`
3. Server auto-restarts
4. Changes ready instantly

**Frontend (React):**
1. Edit file in `app/`
2. Save: `Ctrl+S`
3. Browser auto-refreshes
4. Changes visible instantly

### Key Files to Edit

**Backend:**
- `backend/api/routes/query.py` - Query endpoint
- `backend/recommender/rules.py` - Chart selection logic
- `backend/nlp/parser.py` - Query understanding
- `backend/data/oecd_*.csv` - Your data

**Frontend:**
- `app/page.tsx` - Main page
- `app/components/QueryInput.tsx` - Input component
- `app/components/ChartDisplay.tsx` - Chart rendering
- `app/globals.css` - Styling

---

## Running Next Time

Just follow these 3 steps:

1. Open VS Code with project
2. Open terminal: `Ctrl + ``
3. Run backend: `python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload`
4. Open Terminal 2: `Ctrl + Shift + ``
5. Run frontend: `npm run dev`
6. Browser: `http://localhost:3000`

---

## Keep Both Terminals Running

**CRITICAL:** Never close both terminals at once (unless done working).

If one stops:
1. Look for red error text
2. Fix the error
3. Run the command again

---

## Stopping Everything

To shut down:
1. Terminal 1: Press `Ctrl+C`
2. Terminal 2: Press `Ctrl+C`
3. Wait for both to stop
4. Close VS Code

---

## Troubleshooting

**Q: "ModuleNotFoundError: No module named 'fastapi'"**
- Did you activate venv? Should see `(venv)` in terminal
- Run: `source venv/bin/activate` (Mac/Linux) or `venv\Scripts\activate` (Windows)

**Q: "Port 8000 already in use"**
- Kill process: `lsof -i :8000 | grep LISTEN | awk '{print $2}' | xargs kill -9`
- OR use different port: `--port 8001`

**Q: "npm: command not found"**
- Restart VS Code completely
- Reinstall Node.js from https://nodejs.org/

**Q: "Cannot reach backend API"**
- Terminal 1 not running?
- Check for "Application startup complete" message

**Q: "Blank white page"**
- Terminal 2 not running?
- Check browser console: Press `F12 → Console`

**Q: Can't see code changes**
- Did you save? `Ctrl+S`
- Refresh browser: `F5`

See **TROUBLESHOOTING.md** for more issues.

---

## Project Structure

```
project/
├── backend/                          (Python)
│   ├── api/
│   │   ├── main.py                   (FastAPI app)
│   │   └── routes/
│   │       ├── query.py              (Query endpoint)
│   │       ├── data.py               (Data endpoint)
│   │       └── metadata.py           (Metadata endpoint)
│   ├── nlp/
│   │   └── parser.py                 (Query parsing)
│   ├── recommender/
│   │   ├── rules.py                  (Chart selection)
│   │   └── pipeline.py               (Recommendation flow)
│   ├── data_pipeline/                (Data processing)
│   ├── data/
│   │   └── oecd_agricultural_data.csv
│   ├── requirements.txt              (Python packages)
│   └── test_backend.py               (Diagnostics)
│
├── app/                              (React/Next.js)
│   ├── page.tsx                      (Main page)
│   ├── layout.tsx                    (Layout)
│   ├── globals.css                   (Global styles)
│   └── components/
│       ├── QueryInput.tsx            (Input)
│       ├── ChartDisplay.tsx          (Charts)
│       ├── RecommendationExplanation.tsx
│       ├── LoadingSpinner.tsx
│       └── charts/
│           ├── LineChart.tsx
│           ├── BarChart.tsx
│           └── PieChart.tsx
│
├── package.json                      (Node packages)
├── tsconfig.json                     (TypeScript config)
├── next.config.mjs                   (Next.js config)
├── README.md                         (Project overview)
├── SETUP.md                          (This file)
├── ARCHITECTURE.md                   (System design)
└── TROUBLESHOOTING.md                (Common issues)
```

---

## System Flow

When you submit a query:

```
User Query (Browser)
    ↓
React Component (Frontend)
    ↓
POST to http://localhost:8000/api/query
    ↓
FastAPI Route Handler
    ↓
NLP Parser (understands query)
    ↓
Rules Engine (selects chart type)
    ↓
Data Pipeline (filters & prepares data)
    ↓
API Response (chart config + data)
    ↓
React Renders Chart (Recharts)
    ↓
User Sees Interactive Visualization
```

All in < 1 second!

---

## Understanding the Architecture

- **NLP Parser:** Extracts intent (trend, compare, rank) and entities (wheat, production)
- **Rules Engine:** Selects best chart based on query intent
- **Data Pipeline:** Loads OECD data, filters by entities, aggregates by intent
- **Frontend:** Renders interactive Recharts with explanations

See **ARCHITECTURE.md** for detailed system design.

---

## Getting Help

1. **Terminal errors?** → Check Terminal 1/2 output (red text)
2. **Browser errors?** → Press `F12 → Console`
3. **Still stuck?** → Read **TROUBLESHOOTING.md**
4. **Want to understand?** → Read **ARCHITECTURE.md**
5. **Overall overview?** → Read **README.md**

---

## Next Steps

1. ✅ Setup complete
2. Try different queries in browser
3. Edit files and see changes reload
4. Read **ARCHITECTURE.md** to understand system
5. Customize chart colors in `app/globals.css`
6. Modify example queries in `QueryInput.tsx`
7. Edit chart selection rules in `backend/recommender/rules.py`

---

**Everything is ready to develop. Happy coding!**
