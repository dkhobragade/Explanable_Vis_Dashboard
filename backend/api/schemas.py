"""
API Request/Response Schemas
Pydantic models for data validation.
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class QueryRequest(BaseModel):
    """Request model for chart recommendation queries."""
    query: str = Field(..., description="Natural language query for visualization")
    user_id: Optional[str] = None
    context: Optional[Dict[str, Any]] = None


class ChartData(BaseModel):
    """Data point for a chart."""
    pass  # Dynamic based on chart type


class RecommendationResponse(BaseModel):
    """Response model for chart recommendations."""
    chart_type: str
    confidence: float
    data: List[Dict[str, Any]]
    fields: List[str]
    filters: Dict[str, List[str]]
    temporal_field: Optional[str]
    explanation: str
    rule_reason: str


class MetadataResponse(BaseModel):
    """Response model for metadata endpoint."""
    column_name: str
    data_type: str
    cardinality: int
    is_numeric: bool
    is_categorical: bool
    is_temporal: bool
    distinct_values: Optional[List[Any]]
    stats: Optional[Dict[str, float]]


class FeedbackRequest(BaseModel):
    """Request model for collecting user feedback."""
    query: str
    recommended_chart: str
    user_preferred_chart: Optional[str] = None
    helpful: bool
    comments: Optional[str] = None
    user_id: Optional[str] = None


class FeedbackResponse(BaseModel):
    """Response model for feedback submission."""
    feedback_id: str
    received_at: datetime
    message: str


class DataResponse(BaseModel):
    """Response model for raw data endpoint."""
    rows: List[Dict[str, Any]]
    total_rows: int
    columns: List[str]


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    message: str
    timestamp: datetime
