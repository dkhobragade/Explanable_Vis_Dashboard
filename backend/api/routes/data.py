"""
Data Endpoint
Returns raw and processed data from the dataset.
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from ..schemas import DataResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["data"])

# Global state
_df = None


def init_route(df):
    """Initialize route with dataframe."""
    global _df
    _df = df


@router.get("/data", response_model=DataResponse)
async def get_data(
    limit: Optional[int] = Query(100, ge=1, le=1000),
    offset: Optional[int] = Query(0, ge=0),
    filters: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get raw data from the dataset.
    
    Args:
        limit: Maximum number of rows to return
        offset: Number of rows to skip
        filters: JSON-encoded filter conditions (optional)
        
    Returns:
        DataResponse: Data rows and metadata
    """
    try:
        df = _df.copy()
        
        # Apply filters if provided
        if filters:
            import json
            filter_dict = json.loads(filters)
            for col, values in filter_dict.items():
                if col in df.columns:
                    df = df[df[col].isin(values)]
        
        # Get total before pagination
        total_rows = len(df)
        
        # Apply pagination
        df = df.iloc[offset:offset + limit]
        
        # Convert to dict
        rows = df.to_dict('records')
        
        response = DataResponse(
            rows=rows,
            total_rows=total_rows,
            columns=list(_df.columns)
        )
        
        logger.info(f"Returned {len(rows)} data rows (total: {total_rows})")
        
        return response
    
    except Exception as e:
        logger.error(f"Error retrieving data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving data: {str(e)}"
        )


@router.get("/data/summary")
async def get_data_summary() -> Dict[str, Any]:
    """Get summary statistics about the dataset."""
    try:
        return {
            "total_rows": len(_df),
            "total_columns": len(_df.columns),
            "columns": list(_df.columns),
            "data_types": {col: str(_df[col].dtype) for col in _df.columns},
            "year_range": {
                "min": int(_df['year'].min()),
                "max": int(_df['year'].max())
            } if 'year' in _df.columns else None,
            "unique_countries": int(_df['country'].nunique()) if 'country' in _df.columns else 0,
            "unique_commodities": int(_df['commodity'].nunique()) if 'commodity' in _df.columns else 0,
        }
    
    except Exception as e:
        logger.error(f"Error getting data summary: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting data summary: {str(e)}"
        )


@router.get("/data/values/{column}")
async def get_column_values(column: str) -> Dict[str, Any]:
    """
    Get unique values for a specific column.
    
    Args:
        column: Column name
        
    Returns:
        Dict with unique values
    """
    try:
        if column not in _df.columns:
            raise HTTPException(
                status_code=404,
                detail=f"Column '{column}' not found"
            )
        
        unique_values = sorted(_df[column].dropna().unique().tolist())
        
        return {
            "column": column,
            "unique_count": len(unique_values),
            "values": unique_values
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting column values: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting column values: {str(e)}"
        )
