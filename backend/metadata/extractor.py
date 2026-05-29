"""
Step 2: Metadata Extractor
Analyzes dataset to extract metadata about columns and relationships.
"""
import pandas as pd
from typing import Dict, List, Any
from datetime import datetime


class MetadataExtractor:
    """Extracts metadata from the dataset."""
    
    def __init__(self, df: pd.DataFrame):
        """Initialize extractor with dataframe."""
        self.df = df
        self.metadata = {
            'extraction_timestamp': datetime.now().isoformat(),
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': {}
        }
    
    def extract(self) -> Dict[str, Any]:
        """
        Extract metadata for all columns.
        
        Returns:
            dict: Complete metadata about the dataset
        """
        print("[Metadata Extractor] Starting extraction...")
        
        for column in self.df.columns:
            self.metadata['columns'][column] = self._extract_column_metadata(column)
        
        print(f"[Metadata Extractor] Extracted metadata for {len(self.df.columns)} columns")
        
        return self.metadata
    
    def _extract_column_metadata(self, column: str) -> Dict[str, Any]:
        """
        Extract metadata for a single column.
        
        Args:
            column (str): Column name
            
        Returns:
            dict: Metadata for the column
        """
        col_data = self.df[column]
        dtype = str(col_data.dtype)
        
        metadata = {
            'name': column,
            'data_type': dtype,
            'nullable': bool(col_data.isnull().any()),
            'null_count': int(col_data.isnull().sum()),
            'non_null_count': int(col_data.notna().sum()),
            'cardinality': int(col_data.nunique()),
            'distinct_values': self._get_distinct_values(col_data),
        }
        
        # Add type-specific metadata
        if dtype in ['int32', 'int64', 'float64']:
            metadata.update(self._get_numeric_metadata(col_data))
            metadata['is_numeric'] = True
            metadata['is_categorical'] = False
            metadata['is_temporal'] = False
        else:
            metadata['is_numeric'] = False
            metadata['is_categorical'] = True
            # Check if it might be temporal
            metadata['is_temporal'] = self._is_temporal_column(column, col_data)
        
        return metadata
    
    def _get_numeric_metadata(self, col_data: pd.Series) -> Dict[str, Any]:
        """Extract metadata for numeric columns."""
        return {
            'min': float(col_data.min()),
            'max': float(col_data.max()),
            'mean': float(col_data.mean()),
            'median': float(col_data.median()),
            'std_dev': float(col_data.std()),
        }
    
    def _get_distinct_values(self, col_data: pd.Series) -> List[Any]:
        """Get up to 20 distinct values from the column."""
        distinct = col_data.unique()[:20]
        return [str(v) for v in distinct]
    
    def _is_temporal_column(self, column_name: str, col_data: pd.Series) -> bool:
        """
        Heuristically determine if a column is temporal.
        
        Args:
            column_name (str): Column name
            col_data (pd.Series): Column data
            
        Returns:
            bool: True if column appears to be temporal
        """
        temporal_keywords = ['year', 'date', 'time', 'month', 'day', 'quarter']
        
        # Check column name
        if any(keyword in column_name.lower() for keyword in temporal_keywords):
            return True
        
        # Check data type and range for year columns
        if col_data.dtype in ['int32', 'int64']:
            min_val, max_val = col_data.min(), col_data.max()
            if 1800 <= min_val <= 2100 and 1800 <= max_val <= 2100:
                return True
        
        return False


class MetadataStore:
    """Stores and retrieves metadata."""
    
    def __init__(self, filepath: str = None):
        """Initialize store with optional filepath."""
        self.filepath = filepath or 'backend/metadata/metadata.json'
        self.metadata = {}
    
    def save(self, metadata: Dict[str, Any]) -> None:
        """
        Save metadata to file.
        
        Args:
            metadata (dict): Metadata to save
        """
        import json
        
        with open(self.filepath, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"[Metadata Store] Saved metadata to {self.filepath}")
    
    def load(self) -> Dict[str, Any]:
        """
        Load metadata from file.
        
        Returns:
            dict: Loaded metadata
        """
        import json
        
        try:
            with open(self.filepath, 'r') as f:
                self.metadata = json.load(f)
            print(f"[Metadata Store] Loaded metadata from {self.filepath}")
            return self.metadata
        except FileNotFoundError:
            print(f"[Metadata Store] No metadata file found at {self.filepath}")
            return {}
    
    def get_column_info(self, column: str) -> Dict[str, Any]:
        """Get metadata for a specific column."""
        return self.metadata.get('columns', {}).get(column, {})
    
    def get_numeric_columns(self) -> List[str]:
        """Get list of numeric columns."""
        columns = self.metadata.get('columns', {})
        return [col for col, meta in columns.items() if meta.get('is_numeric', False)]
    
    def get_categorical_columns(self) -> List[str]:
        """Get list of categorical columns."""
        columns = self.metadata.get('columns', {})
        return [col for col, meta in columns.items() if meta.get('is_categorical', False)]
    
    def get_temporal_columns(self) -> List[str]:
        """Get list of temporal columns."""
        columns = self.metadata.get('columns', {})
        return [col for col, meta in columns.items() if meta.get('is_temporal', False)]


if __name__ == "__main__":
    from data_pipeline import load_raw_data, clean_data
    
    df = load_raw_data()
    df = clean_data(df)
    
    extractor = MetadataExtractor(df)
    metadata = extractor.extract()
    
    store = MetadataStore()
    store.save(metadata)
    
    print("\nMetadata extracted and saved")
    print(f"Numeric columns: {store.get_numeric_columns()}")
    print(f"Categorical columns: {store.get_categorical_columns()}")
    print(f"Temporal columns: {store.get_temporal_columns()}")
