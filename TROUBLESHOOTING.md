# Troubleshooting Guide - Query Fetch Errors

## Problem: "Query is getting failed" / Fetch Error

When you click "Search" or submit a query, you get an error message. This guide helps you fix it.

---

## Step 1: Verify Backend is Running

**Error Symptom:** "Failed to fetch" or "Connection refused"

This means the backend API is not running.

### Fix:

**Terminal 1 - Start Backend:**
```bash
cd /vercel/share/v0-project
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
cd backend
pip install -r requirements.txt
cd ..
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Wait for this message:
```
Application startup complete
[INFO] ✓ API Initialization Complete
```

---

## Step 2: Test Backend Components

**Before running the full server, test each component:**

```bash
cd /vercel/share/v0-project/backend
python test_backend.py
```

You should see:
```
[v0] Testing backend components...
[v0] Step 1: Testing data loader... ✓ Loaded 128 rows
[v0] Step 2: Testing metadata extractor... ✓
[v0] Step 3: Testing knowledge graph... ✓
[v0] Step 4: Testing NLP parser... ✓
[v0] Step 5: Testing recommendation pipeline... ✓
[v0] ✓ ALL TESTS PASSED!
```

If any step fails, see the specific fix below.

---

## Step 3: Start Frontend

**Terminal 2 (NEW TERMINAL) - Start Next.js:**
```bash
cd /vercel/share/v0-project
npm install
npm run dev
```

Wait for:
```
✓ Ready in 2.1s
➜  Local:   http://localhost:3000
```

---

## Specific Error Fixes

### Error: "ModuleNotFoundError: No module named 'pandas'"

**Fix:**
```bash
cd /vercel/share/v0-project/backend
pip install -r requirements.txt
```

---

### Error: "Data file not found"

**Fix:**
```bash
ls -la /vercel/share/v0-project/backend/data/
```

Should show: `oecd_agricultural_data.csv`

If missing, run:
```bash
cd /vercel/share/v0-project
python backend/test_backend.py
```

---

### Error: "Failed to get recommendation" (500 error)

**Fix:** Check backend logs for the actual error:

1. In the terminal running the backend, look for:
   ```
   ERROR - Error processing query: ...
   ```

2. Common issues:
   - **Missing column:** Check the data file has the right columns
   - **Parser issue:** Run `python backend/test_backend.py` to verify NLP parser

---

### Error: "Port 8000 already in use"

**Fix:**
```bash
# Find process using port 8000
lsof -i :8000  # On Mac/Linux
netstat -ano | findstr :8000  # On Windows

# Kill it
kill -9 <PID>  # On Mac/Linux
taskkill /PID <PID> /F  # On Windows

# Then restart
python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

---

### Error: "CORS blocked" / "Access to XMLHttpRequest blocked"

This should be fixed (CORS is enabled in the API), but if you see it:

**Frontend error in console:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/query' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Fix:** Backend must have CORS middleware enabled (it does by default).

---

## Debugging Checklist

Before troubleshooting further:

- [ ] Backend running on `http://localhost:8000` (check terminal)
- [ ] Frontend running on `http://localhost:3000` (check browser)
- [ ] Both in separate terminals
- [ ] Backend shows "Application startup complete"
- [ ] Frontend shows "Ready in X.Xs"
- [ ] Health check: Visit `http://localhost:8000/health` - should return JSON
- [ ] Test endpoint: Visit `http://localhost:8000/api/query/examples` - should return example queries

---

## Quick Test Request

**If everything is running, test the API directly:**

```bash
curl -X POST http://localhost:8000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Show wheat production trends", "user_id": "test-user"}'
```

You should get a JSON response with chart recommendation.

---

## Still Broken?

1. **Check console logs:**
   - Browser: F12 → Console tab → Look for red errors
   - Backend: Look at terminal where you ran uvicorn

2. **Restart everything:**
   ```bash
   # Kill both processes (Ctrl+C in terminals)
   # Close all terminals
   # Start fresh: backend first, then frontend
   ```

3. **Clear cache:**
   - Browser: F12 → Network → Disable cache (checkbox)
   - Or use Incognito/Private window

4. **Check file permissions:**
   ```bash
   chmod +x /vercel/share/v0-project/backend/test_backend.py
   python /vercel/share/v0-project/backend/test_backend.py
   ```

---

## Architecture Check

The system has these layers - test each:

```
Browser (localhost:3000) 
    ↓ (HTTP fetch)
FastAPI Backend (localhost:8000)
    ↓
NLP Parser → Rules Engine → Data Pipeline
    ↓
Returns chart recommendation (JSON)
    ↓
React renders chart
```

If any layer fails, the entire chain breaks.

---

## Environment Variables

Check `.env.local`:
```bash
cat /vercel/share/v0-project/.env.local
```

Should have:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If missing or wrong, update it:
```
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > /vercel/share/v0-project/.env.local
```

---

## Need More Help?

1. Run the test script and share output: `python backend/test_backend.py`
2. Share the exact error message from browser console (F12)
3. Share the exact error message from backend terminal
4. Check if you can reach the health endpoint: `curl http://localhost:8000/health`

Good luck! The system is designed to work end-to-end.
