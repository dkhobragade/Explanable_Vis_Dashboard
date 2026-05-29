"""
Metadata Endpoint
Returns metadata about the dataset columns.
"""
from fastapi import APIRouter, HTTPException
from ..schemas import MetadataResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["metadata"])

# Global state
_metadata_store = None


def init_route(metadata_store):
    """Initialize route with metadata store."""
    global _metadata_store
    _metadata_store = metadata_store


@router.get("/metadata")
async def get_all_metadata():
    """Get metadata for all columns in the dataset."""
    try:
        if not _metadata_store or not _metadata_store.metadata:
            raise HTTPException(
                status_code=500,
                detail="Metadata not loaded"
            )
        
        return _metadata_store.metadata
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting metadata: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting metadata: {str(e)}"
        )


@router.get("/metadata/{column}", response_model=MetadataResponse)
async def get_column_metadata(column: str) -> MetadataResponse:
    """
    Get metadata for a specific column.
    
    Args:
        column: Column name
        
    Returns:
        MetadataResponse: Column metadata
    """
    try:
        if not _metadata_store or not _metadata_store.metadata:
            raise HTTPException(
                status_code=500,
                detail="Metadata not loaded"
            )
        
        col_meta = _metadata_store.get_column_info(column)
        
        if not col_meta:
            raise HTTPException(
                status_code=404,
                detail=f"Metadata not found for column '{column}'"
            )
        
        response = MetadataResponse(
            column_name=col_meta.get('name', column),
            data_type=col_meta.get('data_type', 'unknown'),
            cardinality=col_meta.get('cardinality', 0),
            is_numeric=col_meta.get('is_numeric', False),
            is_categorical=col_meta.get('is_categorical', False),
            is_temporal=col_meta.get('is_temporal', False),
            distinct_values=col_meta.get('distinct_values'),
            stats={
                'min': col_meta.get('min'),
                'max': col_meta.get('max'),
                'mean': col_meta.get('mean'),
                'median': col_meta.get('median'),
            } if col_meta.get('is_numeric') else None
        )
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting column metadata: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting column metadata: {str(e)}"
        )


@router.get("/metadata/columns/numeric")
async def get_numeric_columns():
    """Get list of numeric columns."""
    try:
        if not _metadata_store:
            raise HTTPException(status_code=500, detail="Metadata not loaded")
        
        return {
            "numeric_columns": _metadata_store.get_numeric_columns()
        }
    except Exception as e:
        logger.error(f"Error getting numeric columns: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metadata/columns/categorical")
async def get_categorical_columns():
    """Get list of categorical columns."""
    try:
        if not _metadata_store:
            raise HTTPException(status_code=500, detail="Metadata not loaded")
        
        return {
            "categorical_columns": _metadata_store.get_categorical_columns()
        }
    except Exception as e:
        logger.error(f"Error getting categorical columns: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metadata/columns/temporal")
async def get_temporal_columns():
    """Get list of temporal columns."""
    try:
        if not _metadata_store:
            raise HTTPException(status_code=500, detail="Metadata not loaded")
        
        return {
            "temporal_columns": _metadata_store.get_temporal_columns()
        }
    except Exception as e:
        logger.error(f"Error getting temporal columns: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
