"""
Step 1: Data Cleaner
Handles missing values, type conversions, and data validation.
"""
import pandas as pd
import numpy as np


class DataCleaner:
    """Cleans and validates OECD agricultural data."""
    
    def __init__(self, df):
        """Initialize cleaner with raw dataframe."""
        self.df = df.copy()
        self.cleaning_report = {}
    
    def clean(self):
        """
        Execute all cleaning steps.
        
        Returns:
            pd.DataFrame: Cleaned dataframe
        """
        print("[Data Cleaner] Starting data cleaning...")
        
        # Step 1: Remove duplicates
        initial_rows = len(self.df)
        self.df = self.df.drop_duplicates()
        self.cleaning_report['duplicates_removed'] = initial_rows - len(self.df)
        
        # Step 2: Handle missing values
        self._handle_missing_values()
        
        # Step 3: Convert types
        self._convert_types()
        
        # Step 4: Validate ranges
        self._validate_ranges()
        
        print(f"[Data Cleaner] Cleaning complete. {len(self.df)} rows remaining")
        print(f"[Data Cleaner] Report: {self.cleaning_report}")
        
        return self.df
    
    def _handle_missing_values(self):
        """Handle missing values in the dataset."""
        initial_nulls = self.df.isnull().sum().sum()
        
        # For numeric columns, we can fill with median or drop
        # For categorical columns, fill with 'Unknown'
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if self.df[col].dtype in ['int64', 'float64']:
                    # Fill numeric with median
                    self.df[col].fillna(self.df[col].median(), inplace=True)
                else:
                    # Fill categorical with 'Unknown'
                    self.df[col].fillna('Unknown', inplace=True)
        
        final_nulls = self.df.isnull().sum().sum()
        self.cleaning_report['null_values_handled'] = initial_nulls
        print(f"[Data Cleaner] Handled {initial_nulls} null values")
    
    def _convert_types(self):
        """Convert columns to appropriate data types."""
        type_conversions = {
            'year': 'int32',
            'value': 'float64',
        }
        
        for col, dtype in type_conversions.items():
            if col in self.df.columns:
                try:
                    self.df[col] = self.df[col].astype(dtype)
                    print(f"[Data Cleaner] Converted '{col}' to {dtype}")
                except Exception as e:
                    print(f"[Data Cleaner] Warning: Could not convert '{col}': {e}")
        
        # Ensure categorical columns are strings
        categorical_cols = ['country', 'region', 'commodity', 'measure', 'unit']
        for col in categorical_cols:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype('string')
    
    def _validate_ranges(self):
        """Validate that values are in expected ranges."""
        # Year should be between 1950 and 2050
        if 'year' in self.df.columns:
            invalid_years = self.df[(self.df['year'] < 1950) | (self.df['year'] > 2050)]
            if len(invalid_years) > 0:
                print(f"[Data Cleaner] Warning: {len(invalid_years)} rows with invalid years")
                self.df = self.df[~self.df.index.isin(invalid_years.index)]
                self.cleaning_report['invalid_years_removed'] = len(invalid_years)
        
        # Production values should be positive
        if 'value' in self.df.columns:
            invalid_values = self.df[self.df['value'] < 0]
            if len(invalid_values) > 0:
                print(f"[Data Cleaner] Warning: {len(invalid_values)} rows with negative values")
                self.df = self.df[~self.df.index.isin(invalid_values.index)]
                self.cleaning_report['negative_values_removed'] = len(invalid_values)
    
    def get_report(self):
        """Get the cleaning report."""
        return self.cleaning_report


def clean_data(df):
    """
    Convenience function to clean data.
    
    Args:
        df (pd.DataFrame): Raw dataframe
        
    Returns:
        pd.DataFrame: Cleaned dataframe
    """
    cleaner = DataCleaner(df)
    return cleaner.clean()


if __name__ == "__main__":
    from loader import load_raw_data
    
    df = load_raw_data()
    cleaned_df = clean_data(df)
    print("\nCleaned data sample:")
    print(cleaned_df.head())
