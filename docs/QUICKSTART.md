# Quick Start - Commands Only

## Prerequisites
- Python 3.8+
- Node.js 16+
- npm

## Terminal 1: Backend (Python)

```bash
python -m venv venv

# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r backend/requirements.txt
python backend/test_backend.py

python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Wait for: `Application startup complete`

## Terminal 2: Frontend (React)

```bash
npm install
npm run dev
```

Wait for: `Ready in X.Xs`

## Browser

Open: **http://localhost:3000**

Click example query → See chart!

## Test API (Optional)

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show wheat production trends"}'
```

## Example Queries

- "Show wheat production trends over time"
- "Compare maize production by country"
- "What are the top wheat regions?"
- "Production breakdown by commodity"

See SETUP.md for full documentation.
