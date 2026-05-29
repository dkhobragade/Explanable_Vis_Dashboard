# Intelligent Data Visualization System - Architecture

## System Overview

This is a complete end-to-end system that automatically recommends chart types based on natural language queries. The system uses Python backend (FastAPI) with React frontend and OECD agricultural data.

## Architecture Layers

### Layer 1: Data Pipeline (Backend)
**Steps 1-3: Data Preparation**

```
Raw CSV Data
    ↓
[Loader] - Load from CSV
    ↓
[Cleaner] - Handle missing values, type conversions
    ↓
[Validator] - Schema validation, consistency checks
    ↓
Cleaned DataFrames (Pandas)
    ↓
[Metadata Extractor] - Analyze columns
    ↓
[Knowledge Graph Builder] - Create semantic relationships
    ↓
Metadata JSON + Knowledge Graph JSON
```

**Key Components:**
- `data_pipeline/loader.py` - Loads OECD agricultural CSV
- `data_pipeline/cleaner.py` - Cleans data (nulls, types, validation)
- `data_pipeline/validator.py` - Validates against schema
- `metadata/extractor.py` - Extracts column statistics and types
- `knowledge_graph/builder.py` - Creates entity relationships

### Layer 2: Recommendation Engine (Backend)
**Steps 4-6: Intelligence**

```
User Query (Natural Language)
    ↓
[NLP Parser] - Extract intent & entities
    - Intent detection (trend, compare, rank, etc.)
    - Entity extraction (wheat, Europe, USA, etc.)
    - Temporal reference detection
    ↓
Parsed Query {intent, entities, filters}
    ↓
[Rules Engine] - Select chart type
    - Rule 1: Temporal + Metric → Line Chart
    - Rule 2: Category + Metric → Bar Chart
    - Rule 3: Multiple Metrics → Grouped Bar
    - Rule 4: Part-to-whole → Pie Chart
    - Rule 5: Single Value → Card
    ↓
[Data Preparation] - Filter & aggregate data
    ↓
Chart Recommendation {type, data, explanation}
```

**Key Components:**
- `nlp/parser.py` - Pattern-based NLP using regex
- `recommender/rules.py` - Chart selection rules
- `recommender/pipeline.py` - End-to-end pipeline

### Layer 3: API (Backend)
**Step 7: REST API**

FastAPI server with endpoints:
- `POST /api/query` - Get chart recommendation
- `GET /api/data` - Get raw dataset
- `GET /api/metadata` - Get column metadata
- `POST /api/feedback` - Submit user feedback
- `GET /api/health` - Health check

**Key Component:**
- `api/main.py` - FastAPI application entry point

### Layer 4: Frontend (React)
**Steps 8-10: User Interface**

```
User Interface
    ↓
[QueryInput] - Text input with examples
    ↓
HTTP POST /api/query
    ↓
[ChartDisplay] - Renders chart based on type
    - LineChart (Recharts)
    - BarChart (Recharts)
    - PieChart (Recharts)
    - CardDisplay (Static)
    ↓
[RecommendationExplanation] - Shows reasoning & confidence
    ↓
Interactive Visualization
```

**Key Components:**
- `app/page.tsx` - Main dashboard
- `app/components/QueryInput.tsx` - Query input form
- `app/components/ChartDisplay.tsx` - Chart renderer
- `app/components/charts/*.tsx` - Specific chart types
- `app/components/RecommendationExplanation.tsx` - Reasoning display

## Data Flow Example

```
User: "Show wheat production trends in Europe over time"

1. QueryInput sends to /api/query
2. NLP Parser:
   - Intent: "trend"
   - Entities: wheat, Europe
   - Temporal: true (over time)
3. Pipeline resolves:
   - Fields: [year, value, region]
   - Temporal field: year
4. Rules Engine:
   - Detects: Temporal + Metric
   - Selects: Line Chart
   - Confidence: 90%
5. Data Preparation:
   - Filter: region = "Europe", commodity = "Wheat"
   - Group by: year, sum production
   - Result: [{year: 2015, value: ...}, ...]
6. Response:
   - Chart Type: line
   - Data: [...]
   - Explanation: "Line chart is ideal for showing trends over time"
7. Frontend:
   - Renders Recharts LineChart
   - Shows explanation
   - Displays data points
```

## Database Schema

### OECD Agricultural Data (CSV)
```
Columns:
- year (int32) - Year of measurement
- country (string) - Country name
- region (string) - Geographic region
- commodity (string) - Agricultural commodity
- measure (string) - Measurement type
- value (float64) - Numeric value
- unit (string) - Unit of measurement
```

### Feedback Storage (JSONL)
```
{
  "feedback_id": "uuid",
  "timestamp": "ISO8601",
  "query": "user query",
  "recommended_chart": "chart type",
  "user_preferred_chart": "chart type or null",
  "helpful": boolean,
  "comments": "user comments",
  "user_id": "user id or anonymous"
}
```

## Technology Stack

### Backend
- **Framework:** FastAPI 0.104.1
- **Server:** Uvicorn
- **Data Processing:** Pandas 2.1.3, NumPy 1.26.2
- **NLP:** Regex-based patterns (spaCy for future)
- **Validation:** Pydantic 2.5.0
- **Database:** SQLite (optional, JSON currently)
- **Testing:** pytest

### Frontend
- **Framework:** Next.js 16
- **UI:** React 19
- **Charts:** Recharts
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui
- **Type Safety:** TypeScript

### Data Storage
- **Primary Data:** CSV (OECD agricultural data)
- **Metadata:** JSON (in-memory + file storage)
- **Knowledge Graph:** JSON (in-memory + file storage)
- **Feedback:** JSONL (line-delimited JSON)

## Key Algorithms

### Intent Detection
- Pattern matching using regex
- Multi-pattern matching with confidence scoring
- Returns top-scoring intent

### Entity Extraction
- Keyword-based extraction
- Uses knowledge graph for synonyms
- Maps entities to dataset columns

### Chart Selection (Rules Engine)
```
if (temporal_count > 0 && metric_count == 1):
  if (intent == 'area'):
    return AREA_CHART
  else:
    return LINE_CHART

elif (intent == 'rank'):
  return HORIZONTAL_BAR

elif (metric_count == 1 && categorical_count > 0):
  return BAR_CHART

elif (metric_count > 1 && categorical_count > 0):
  return GROUPED_BAR

# ... more rules ...
else:
  return BAR_CHART (default)
```

## Configuration & Deployment

### Development
```bash
# Backend
cd backend
pip install -r requirements.txt
python api/main.py  # Runs on http://localhost:8000

# Frontend  
cd ..
npm run dev  # Runs on http://localhost:3000
```

### Production
- Deploy backend to cloud (AWS, GCP, Azure, etc.)
- Deploy frontend to Vercel
- Use environment variables for configuration
- Enable CORS for cross-origin requests
- Set up monitoring and logging

## Extension Points

### Adding New Chart Types
1. Add to `recommender/rules.py` ChartType enum
2. Create component in `app/components/charts/`
3. Update ChartDisplay router
4. Add rules for selection

### Adding New Data Sources
1. Create loader in `data_pipeline/`
2. Implement cleaner and validator
3. Update metadata extractor
4. Add to knowledge graph

### Improving NLP
1. Add patterns to `nlp/parser.py`
2. Train spaCy model for entity recognition
3. Implement entity disambiguation
4. Add support for more languages

### Adding User Features
1. User preferences: `user/preferences.py`
2. Feedback analysis: `feedback/analyzer.py`
3. Personalization: Update pipeline with user context
4. A/B Testing: Track recommendation effectiveness

## Performance Considerations

### Data Loading
- Data loaded once at startup
- Metadata cached in memory
- Knowledge graph pre-built

### Query Processing
- NLP parsing: ~10-50ms
- Rule evaluation: ~1-5ms
- Data filtering & aggregation: ~10-100ms (depends on data size)
- Total latency: ~30-200ms per query

### Scalability
- Current: Single-machine Python backend
- Bottleneck: Data processing with large datasets
- Solutions:
  - Use distributed processing (Spark, Dask)
  - Cache query results
  - Implement query indexing
  - Use columnar storage (Parquet, ORC)

## Monitoring & Logging

### Backend Logs
- Data pipeline initialization
- Query processing steps
- Recommendation generation
- Errors and exceptions

### Frontend Errors
- Query submission failures
- API connection errors
- Chart rendering issues

### Metrics to Track
- Query success rate
- Average recommendation confidence
- Chart type distribution
- User feedback helpful rate
- Query response time

## Testing Strategy

### Unit Tests
- Data cleaner (missing values, types)
- Validator (schema checking)
- NLP parser (intent detection, entity extraction)
- Rules engine (chart recommendations)

### Integration Tests
- Full pipeline (query → recommendation)
- API endpoints (request/response validation)
- Frontend components (rendering, interactions)

### Test Data
- Small OECD subset
- Edge cases (empty data, single values)
- Invalid inputs (malformed queries)

## Future Enhancements

### Phase 1 (MVP) ✓
- Basic NLP with pattern matching
- Rules-based chart selection
- Frontend with basic charts
- OECD agricultural data

### Phase 2 (Enhancement)
- Machine learning for intent detection
- More chart types (Scatter, Heatmap, etc.)
- User personalization
- Advanced feedback analysis

### Phase 3 (Advanced)
- Real-time data updates
- Multi-dataset support
- Custom rule builder UI
- Recommendation explanation generator
- Collaborative features

### Phase 4 (Scale)
- Distributed processing
- Multi-language support
- Integration with BI tools
- Enterprise deployment
