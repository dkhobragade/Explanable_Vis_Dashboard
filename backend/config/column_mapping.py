"""
Column Mapping Configuration
Maps your CSV columns to internal system columns
"""

# Your actual CSV columns from OCES dataset
CSV_COLUMNS = {
    'STRUCTURE': 'structure',
    'STRUCTURE_ID': 'structure_id',
    'STRUCTURE_NAME': 'structure_name',
    'ACTION': 'action',
    'REF_AREA': 'region',  # Maps to region/area
    'Reference area': 'region_name',
    'FREQ': 'frequency',
    'Frequency of observation': 'frequency_name',
    'COMMODITY': 'product',  # Maps to commodity/product
    'Commodity': 'product_name',
    'MEASURE': 'measure',
    'Measure': 'measure_name',
    'UNIT_MEASURE': 'unit',
    'Unit of measure': 'unit_name',
    'VERSION_ID': 'version_id',
    'Version ID': 'version_name',
    'TIME_PERIOD': 'year',  # Maps to time period
    'Time period': 'year_name',
    'OBS_VALUE': 'value',  # Maps to observation value
    'Observation value': 'value_name',
    'OBS_STATUS': 'obs_status',
    'Observation status': 'obs_status_name',
    'UNIT_MULT': 'unit_mult',
    'Unit multiplier': 'unit_mult_name',
    'DECIMALS': 'decimals',
    'Decimals': 'decimals_name',
    'CONVENTION': 'convention',
    'Agricultural convention': 'convention_name',
}

# Key columns for the system
KEY_COLUMNS = {
    'region_column': 'REF_AREA',  # Use for grouping by area
    'product_column': 'COMMODITY',  # Use for grouping by commodity
    'time_column': 'TIME_PERIOD',  # Use for time series
    'value_column': 'OBS_VALUE',  # The main metric to visualize
    'measure_column': 'MEASURE',  # Type of measurement
}

# Expected data types
EXPECTED_TYPES = {
    'REF_AREA': 'object',  # Text
    'COMMODITY': 'object',  # Text
    'TIME_PERIOD': 'int64',  # Year as integer
    'OBS_VALUE': 'float64',  # Numeric value
    'MEASURE': 'object',  # Text
}

# Column aliases - what users might call these columns
COLUMN_ALIASES = {
    'region': ['REF_AREA', 'ref_area', 'area', 'country', 'location'],
    'product': ['COMMODITY', 'commodity', 'crop', 'item'],
    'year': ['TIME_PERIOD', 'time_period', 'year', 'period'],
    'value': ['OBS_VALUE', 'obs_value', 'observation value', 'metric', 'amount'],
    'measure': ['MEASURE', 'measure', 'measurement', 'type'],
}


def get_column_name(user_input: str) -> str:
    """
    Map user input to actual CSV column name
    
    Args:
        user_input: What the user said (e.g., "wheat", "united states", "2019")
        
    Returns:
        The actual column name to use for filtering
    """
    user_input_lower = user_input.lower()
    
    # Check if it's a known column name
    for category, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias.lower() in user_input_lower or user_input_lower in alias.lower():
                return KEY_COLUMNS.get(category + '_column', category)
    
    return None


def normalize_column_name(col_name: str) -> str:
    """Normalize column name from CSV"""
    return col_name.strip().upper()
