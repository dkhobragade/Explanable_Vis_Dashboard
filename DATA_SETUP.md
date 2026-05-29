# Data Setup Guide

## Current Setup

Your data folder is ready at: `backend/data/`

Currently using: `oces_data.csv` (sample data with 40 rows)

## Columns in Current Data

```
id                  - Row identifier
region              - Geographic region (North America, Europe, Asia, South America, Africa)
product             - Agricultural product (Wheat, Maize, Rice, Barley, Soybeans)
year                - Year (2015-2019)
area_hectares       - Area under cultivation in hectares
production_tonnes   - Total production in tonnes
yield_per_hectare   - Yield per hectare (tonnes/hectare)
```

## Replacing with Your Data

### Step 1: Prepare Your CSV File

Ensure your CSV file has:
- Proper headers in the first row
- Consistent data types in each column
- No special characters that break CSV parsing

### Step 2: Upload Your File

1. Save your CSV file as: `oces_data.csv`
2. Place it in: `backend/data/` folder
3. Replace the existing sample file

### Step 3: The System Will Automatically:

✓ Load your data on next backend start
✓ Extract metadata (column types, unique values)
✓ Build knowledge graph from your data
✓ Detect entities for NLP parsing
✓ Validate data quality

**No code changes needed!** The system auto-detects and adapts to your data structure.

## How It Works

The data loader in `backend/data_pipeline/loader.py`:

1. Looks for `oces_data.csv` first
2. If not found, falls back to `oecd_agricultural_data.csv`
3. Loads with pandas
4. Passes to validation pipeline
5. Metadata extraction happens automatically

## File Replacement Steps

### Option 1: Direct File Replacement

```bash
# Navigate to your project
cd /path/to/project

# Replace the file
# Copy your oces_data.csv to backend/data/oces_data.csv
```

### Option 2: Via Upload

1. Download current project ZIP
2. Extract to your computer
3. Go to `backend/data/` folder
4. Delete `oces_data.csv`
5. Add your CSV file (keep the name `oces_data.csv`)
6. Run the system

## Data Requirements

### Minimum Requirements:
- At least 2 columns
- At least 10 rows
- CSV format with headers

### Recommended:
- 5-10 columns (for better analysis)
- 100+ rows (for meaningful visualizations)
- Consistent data types
- No empty values in key columns

## Supported Data Types

✓ Numeric (int, float)
✓ Text (string, category)
✓ Date/Time (YYYY-MM-DD)
✓ Boolean

## What Happens When You Change Data

1. **On Backend Start:**
   - System loads your CSV
   - Analyzes column types
   - Extracts metadata

2. **NLP Parser Updates:**
   - Recognizes your column names as entities
   - Matches user queries to your columns

3. **Recommender Engine:**
   - Uses data types to suggest charts
   - Adapts rules based on your data structure

4. **Frontend:**
   - Automatically displays available columns
   - Shows example queries for your data

## Testing Your Data

After uploading, test with:

```bash
# Terminal
python backend/test_backend.py
```

This will show:
- ✓ Data loaded successfully
- ✓ Number of rows and columns
- ✓ Column names and types
- ✓ Data sample (first 5 rows)

## Troubleshooting

### "Data file not found"
- Check file exists in `backend/data/`
- File name must be exactly `oces_data.csv`
- No spaces or special characters

### "CSV parsing error"
- Open file in text editor
- Check for special characters
- Ensure proper CSV formatting
- Try opening in Excel to verify

### "Unknown column type"
- System may treat as text if unclear
- Number columns with text get converted to text
- Use consistent formats in columns

### Data doesn't appear in charts
- Check NLP parser recognizes column names
- Try explicit query with exact column name
- Check browser console for errors (F12)

## Large File Handling

For large CSV files (100MB+):

1. Split into multiple files (if possible)
2. Or upload file incrementally
3. System will load and process automatically

The sample data (`oces_data.csv`) is currently 40 rows. Replace with your actual data file keeping the same filename.

## Column Name Best Practices

When preparing your data:

✓ Use clear, descriptive names
✓ Use lowercase with underscores: `production_tonnes`
✓ Avoid special characters
✓ Keep names concise (< 20 chars)

Bad:     `Prod $$$`, `COLUMN1`, `data-item`
Good:    `production`, `region_code`, `product_name`

## Next Steps

1. Prepare your CSV file
2. Replace `backend/data/oces_data.csv`
3. Restart backend server
4. System auto-detects and uses your data
5. Test with queries

The entire system is ready to work with your data!
