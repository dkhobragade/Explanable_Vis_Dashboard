# Intelligent Data Visualization System

An end-to-end system that automatically recommends chart types based on natural language queries. Ask questions about OECD agricultural data in plain English, and the system intelligently selects the best visualization and displays your data.

## Features

✨ **Natural Language Queries** - Ask questions like "Show wheat production trends in Europe"

📊 **Intelligent Chart Recommendations** - Automatically selects optimal chart types (line, bar, pie, etc.)

🔍 **Interactive Visualization** - See data come alive with Recharts visualizations

💡 **Explainable AI** - Understand why each chart was recommended

📈 **Real-time Processing** - Sub-200ms latency from query to visualization

🎯 **Feedback Loop** - System learns from user interactions

## How It Works

```
Natural Language Query
    ↓
NLP Parser (Intent + Entity Extraction)
    ↓
Rules-Based Recommendation Engine
    ↓
Data Preparation & Filtering
    ↓
Interactive Chart Visualization
```

## System Architecture

```
┌─────────────────────────────────────────────┐
│         React Frontend (Next.js)            │
│   - Query Input, Chart Display, UI         │
└────────────────┬────────────────────────────┘
                 │ HTTP REST API
┌────────────────▼────────────────────────────┐
│       FastAPI Backend (Python)              │
│  ├─ NLP Parser (Intent/Entities)           │
│  ├─ Rules Engine (Chart Selection)         │
│  ├─ Data Pipeline (Cleaning/Validation)    │
│  └─ API Endpoints (/query, /data, etc.)   │
└────────────────┬────────────────────────────┘
                 │
┌────────────────▼────────────────────────────┐
│        Data Layer                           │
│  ├─ OECD Agricultural Data (CSV)           │
│  ├─ Metadata (JSON)                        │
│  ├─ Knowledge Graph (JSON)                 │
│  └─ Feedback (JSONL)                       │
└─────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
# Install backend dependencies
cd backend
pip3 install -r requirements.txt
cd ..

# Install frontend dependencies
npm install
```

### Run Locally

**Terminal 1 - Backend:**
```bash
cd backend
python api/main.py
```

**Terminal 2 - Frontend:**
```bash
npm run dev
```

Open http://localhost:3000 in your browser.

## Example Queries

Try these natural language queries:

- **"Show wheat production trends over time"** 
  → Line chart with temporal trends
  
- **"Compare maize production across countries"** 
  → Bar chart comparing nations
  
- **"What are the top wheat producing regions?"** 
  → Ranked horizontal bar chart
  
- **"Show production breakdown by commodity"** 
  → Pie chart with proportions
  
- **"Wheat production in USA vs Europe"** 
  → Side-by-side comparison

## Technology Stack

### Backend
- **Python 3.9+**
- **FastAPI** - Modern web framework
- **Pandas** - Data processing
- **spaCy/Regex** - Natural language parsing
- **Pydantic** - Data validation

### Frontend
- **Next.js 16** - React framework
- **React 19** - UI library
- **Recharts** - Chart visualization
- **Tailwind CSS** - Styling
- **TypeScript** - Type safety

### Data
- **OECD Agricultural Data** (CSV)
- **Metadata** (JSON)
- **Knowledge Graph** (JSON)
- **Feedback** (JSONL)

## API Endpoints

### Chart Recommendation
```
POST /api/query
Body: { "query": "Show wheat production trends" }
Returns: { chart_type, confidence, data, explanation }
```

### Raw Data
```
GET /api/data?limit=100&offset=0
Returns: { rows, total_rows, columns }
```

### Metadata
```
GET /api/metadata
GET /api/metadata/{column}
Returns: Column statistics and metadata
```

### Feedback
```
POST /api/feedback
Body: { query, recommended_chart, user_preferred_chart, helpful, comments }
Returns: { feedback_id, received_at }
```

### Health Check
```
GET /health
Returns: { status, timestamp, initialized }
```

## Key Components

### Backend Modules

**Data Pipeline** (Steps 1-3)
- Load raw CSV data
- Clean missing values & types
- Validate schema consistency
- Extract metadata
- Build knowledge graph

**Recommendation Engine** (Steps 4-7)
- Parse natural language queries
- Extract intent & entities
- Apply chart selection rules
- Prepare data for visualization
- Generate explanations

**API** (Step 7)
- FastAPI application
- RESTful endpoints
- CORS middleware
- Request validation

### Frontend Components

**Query Interface**
- Natural language input
- Example queries
- Error handling

**Chart Display**
- Dynamic chart rendering
- Support for: Line, Bar, Pie, Card charts
- Responsive design

**Explanation**
- Recommendation reasoning
- Confidence score
- Data field summary

## Configuration

### Environment Variables

```
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
BACKEND_HOST=localhost
BACKEND_PORT=8000
```

### Backend Configuration

Modify in `backend/api/main.py`:
- CORS origins (for production)
- Logging level
- Data path
- Port

## Project Structure

```
├── backend/
│   ├── api/               # FastAPI application
│   ├── data/              # Data files (CSV)
│   ├── data_pipeline/     # Data processing
│   ├── metadata/          # Metadata extraction
│   ├── knowledge_graph/   # Entity relationships
│   ├── nlp/               # NLP parser
│   ├── recommender/       # Chart recommendation
│   ├── feedback/          # Feedback collection
│   └── requirements.txt
│
├── app/
│   ├── page.tsx           # Main dashboard
│   ├── components/        # React components
│   └── lib/              # Utilities
│
├── docs/
│   ├── ARCHITECTURE.md    # System design
│   ├── QUICKSTART.md      # Setup guide
│   ├── API.md            # API documentation
│   └── USER_GUIDE.md     # User features
│
└── public/               # Static files
```

## Documentation

- **[QUICKSTART.md](docs/QUICKSTART.md)** - Installation and setup
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design and components
- **[API.md](docs/API.md)** - API endpoint reference
- **[USER_GUIDE.md](docs/USER_GUIDE.md)** - Feature walkthroughs

## Performance

- **Query to Chart:** ~30-200ms (depends on data size)
- **Data Pipeline:** One-time initialization on startup
- **Memory:** ~50-100MB for sample dataset
- **Scalability:** Optimized for up to 10M+ rows with indexing

## Roadmap

### Phase 1: MVP ✅
- ✓ NLP query parsing
- ✓ Rules-based chart selection
- ✓ Interactive frontend
- ✓ OECD agricultural data

### Phase 2: Enhancement
- [ ] Machine learning for intent detection
- [ ] More chart types (Scatter, Heatmap, Treemap)
- [ ] User preferences & personalization
- [ ] Advanced feedback analysis

### Phase 3: Advanced
- [ ] Real-time data updates
- [ ] Multi-dataset support
- [ ] Custom rule builder UI
- [ ] Collaborative features

### Phase 4: Scale
- [ ] Distributed processing (Spark)
- [ ] Multi-language support
- [ ] BI tool integrations
- [ ] Enterprise deployment

## Extending the System

### Add More Data
1. Add CSV file to `backend/data/`
2. Create new loader in `data_pipeline/`
3. Update metadata extraction
4. Rebuild knowledge graph

### Custom Chart Types
1. Add to `ChartType` enum in `recommender/rules.py`
2. Create component in `app/components/charts/`
3. Update router in `ChartDisplay.tsx`
4. Add selection rules

### Improve NLP
1. Add patterns to `nlp/parser.py`
2. Train spaCy model for entity recognition
3. Implement entity disambiguation
4. Add synonym detection

## Contributing

This is a complete end-to-end implementation of an intelligent visualization system. To extend:

1. Identify the component to modify (NLP, Rules, Charts, etc.)
2. Follow existing patterns and naming conventions
3. Add tests for new functionality
4. Update documentation

## Performance Tips

- Use filters in queries to reduce data size
- System is optimized for datasets up to 1M rows
- For larger datasets, implement data aggregation
- Cache frequently requested queries
- Use pagination for data endpoints

## Troubleshooting

**API connection errors?**
- Ensure backend is running on port 8000
- Check CORS configuration
- Verify firewall allows port 8000

**No data showing?**
- Check CSV file exists: `backend/data/oecd_agricultural_data.csv`
- Try simpler query: "Show wheat"
- Check browser console for errors

**Slow performance?**
- Monitor backend logs
- Check data size being processed
- Consider data aggregation
- Profile with Chrome DevTools

## License

This is a demonstration project. Feel free to use and modify for your needs.

## Learn More

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev)
- [Next.js Documentation](https://nextjs.org/docs)
- [Recharts Documentation](https://recharts.org/)
- [OECD Data](https://data.oecd.org/)

---

**Built with ❤️ using Python, React, and FastAPI**
