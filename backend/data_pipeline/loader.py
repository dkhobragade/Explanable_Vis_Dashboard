"""
Step 1: Data Loader
Loads OECD agricultural data from CSV file.
"""
import os
import pandas as pd
from pathlib import Path


def get_data_path():
    """Get the path to the data file. Looks for oces_data.csv first, then oecd_agricultural_data.csv"""
    backend_dir = Path(__file__).parent.parent
    
    # Try oces_data.csv first (user's custom data)
    oces_path = backend_dir / "data" / "oces_data.csv"
    if oces_path.exists():
        return oces_path
    
    # Fall back to default OECD data
    return backend_dir / "data" / "oecd_agricultural_data.csv"


def load_raw_data():
    """
    Load raw data from CSV - handles both OCES and simple formats.
    Auto-detects column format and normalizes for the system.
    
    Returns:
        pd.DataFrame: Data with normalized columns
    """
    data_path = get_data_path()
    
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found at {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"[Data Loader] Loaded {len(df)} rows from {data_path}")
    print(f"[Data Loader] Columns: {list(df.columns)}")
    
    # Handle OCES format (has OBS_VALUE column)
    if 'OBS_VALUE' in df.columns:
        print("[Data Loader] Detected OCES format")
        
        # Standardize column names for the system
        column_mapping = {
            'REF_AREA': 'region',
            'Reference area': 'region_name',
            'COMMODITY': 'product',
            'Commodity': 'product_name',
            'TIME_PERIOD': 'year',
            'OBS_VALUE': 'value',
            'MEASURE': 'measure',
            'Unit of measure': 'unit',
            'UNIT_MEASURE': 'unit_code'
        }
        
        # Keep only columns that exist
        cols_to_keep = [col for col in column_mapping.keys() if col in df.columns]
        df = df[cols_to_keep].copy()
        
        # Rename to standardized names
        df.rename(columns={col: column_mapping[col] for col in cols_to_keep}, inplace=True)
        
        # Convert to numeric types
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
        if 'value' in df.columns:
            df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # Remove rows with missing critical values
        df = df.dropna(subset=['value', 'year'])
        print(f"[Data Loader] Processed to {len(df)} valid rows")
    
    return df


def get_data_info(df):
    """
    Get basic information about the dataset.
    
    Args:
        df (pd.DataFrame): The dataset
        
    Returns:
        dict: Info about the dataset
    """
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "columns": list(df.columns),
        "data_types": df.dtypes.to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "memory_usage_mb": df.memory_usage(deep=True).sum() / 1024**2,
    }


if __name__ == "__main__":
    # Test the loader
    df = load_raw_data()
    print("\nData Info:")
    print(get_data_info(df))
    print("\nFirst 5 rows:")
    print(df.head())
