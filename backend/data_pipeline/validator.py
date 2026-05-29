"""
Step 1: Data Validator
Schema validation and consistency checks.
"""
import pandas as pd


# Define expected schema
EXPECTED_SCHEMA = {
    'year': 'int32',
    'country': 'string',
    'region': 'string',
    'commodity': 'string',
    'measure': 'string',
    'value': 'float64',
    'unit': 'string',
}

REQUIRED_COLUMNS = list(EXPECTED_SCHEMA.keys())


class DataValidator:
    """Validates OECD agricultural data against schema."""
    
    def __init__(self, df):
        """Initialize validator with dataframe."""
        self.df = df
        self.errors = []
        self.warnings = []
    
    def validate(self):
        """
        Run all validation checks.
        
        Returns:
            bool: True if validation passed, False otherwise
        """
        print("[Data Validator] Starting validation...")
        
        # Check required columns
        self._check_required_columns()
        
        # Check data types
        self._check_data_types()
        
        # Check for required values
        self._check_required_values()
        
        # Check logical consistency
        self._check_consistency()
        
        if self.errors:
            print(f"[Data Validator] FAILED with {len(self.errors)} errors")
            for error in self.errors:
                print(f"  ERROR: {error}")
            return False
        
        if self.warnings:
            print(f"[Data Validator] PASSED with {len(self.warnings)} warnings")
            for warning in self.warnings:
                print(f"  WARNING: {warning}")
        else:
            print("[Data Validator] PASSED all checks")
        
        return True
    
    def _check_required_columns(self):
        """Check that all required columns are present."""
        missing = set(REQUIRED_COLUMNS) - set(self.df.columns)
        if missing:
            self.errors.append(f"Missing columns: {missing}")
        else:
            print("[Data Validator] ✓ All required columns present")
    
    def _check_data_types(self):
        """Check that columns have correct data types."""
        for col, expected_type in EXPECTED_SCHEMA.items():
            if col not in self.df.columns:
                continue
            
            actual_type = str(self.df[col].dtype)
            
            # Allow some flexibility in string representation
            if expected_type == 'string' and actual_type in ['string', 'object']:
                continue
            elif expected_type != actual_type:
                self.warnings.append(
                    f"Column '{col}' has type {actual_type}, expected {expected_type}"
                )
        
        print("[Data Validator] ✓ Data types checked")
    
    def _check_required_values(self):
        """Check that no required values are missing."""
        for col in REQUIRED_COLUMNS:
            if col not in self.df.columns:
                continue
            
            nulls = self.df[col].isnull().sum()
            if nulls > 0:
                self.errors.append(
                    f"Column '{col}' has {nulls} null values (required non-null)"
                )
        
        if not self.errors:
            print("[Data Validator] ✓ No missing required values")
    
    def _check_consistency(self):
        """Check logical consistency of the data."""
        # Year should be within reasonable range
        if 'year' in self.df.columns:
            year_min, year_max = self.df['year'].min(), self.df['year'].max()
            if year_min < 1950 or year_max > 2050:
                self.warnings.append(
                    f"Year values outside 1950-2050 range: {year_min}-{year_max}"
                )
        
        # Value should be positive (for production)
        if 'value' in self.df.columns:
            negatives = (self.df['value'] < 0).sum()
            if negatives > 0:
                self.errors.append(f"Found {negatives} negative values in 'value' column")
        
        # Check that combinations are unique (year + country + commodity)
        if all(col in self.df.columns for col in ['year', 'country', 'commodity']):
            duplicates = self.df.duplicated(
                subset=['year', 'country', 'commodity'], 
                keep=False
            ).sum()
            if duplicates > 0:
                self.warnings.append(
                    f"Found {duplicates} potential duplicate records "
                    "(same year, country, commodity)"
                )
        
        print("[Data Validator] ✓ Consistency checks passed")
    
    def get_errors(self):
        """Get list of validation errors."""
        return self.errors
    
    def get_warnings(self):
        """Get list of validation warnings."""
        return self.warnings


def validate_data(df):
    """
    Convenience function to validate data.
    
    Args:
        df (pd.DataFrame): Dataframe to validate
        
    Returns:
        bool: True if validation passed
    """
    validator = DataValidator(df)
    return validator.validate()


if __name__ == "__main__":
    from loader import load_raw_data
    from cleaner import clean_data
    
    df = load_raw_data()
    df = clean_data(df)
    validate_data(df)
