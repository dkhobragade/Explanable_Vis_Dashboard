"""
Query Endpoint
Handles natural language queries and returns chart recommendations.
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..schemas import QueryRequest, RecommendationResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["query"])

# Global state - will be initialized in main.py
_pipeline = None
_parser = None


def init_route(pipeline, parser):
    """Initialize route with pipeline and parser instances."""
    global _pipeline, _parser
    _pipeline = pipeline
    _parser = parser


@router.post("/query", response_model=RecommendationResponse)
async def get_recommendation(request: QueryRequest) -> Dict[str, Any]:
    """
    Get a chart recommendation based on a natural language query.
    
    Args:
        request (QueryRequest): Query and context
        
    Returns:
        RecommendationResponse: Chart recommendation with data and explanation
        
    Raises:
        HTTPException: If query is invalid or processing fails
    """
    try:
        if not request.query or len(request.query.strip()) < 3:
            raise HTTPException(
                status_code=400,
                detail="Query must be at least 3 characters long"
            )
        
        print(f"[Query API] Received query: {request.query}")
        
        # Parse the query
        parsed_query = _parser.parse(request.query)
        
        # Generate recommendation
        recommendation = _pipeline.recommend(parsed_query)
        
        # Convert to response model
        response = RecommendationResponse(
            chart_type=recommendation['chart_type'],
            confidence=recommendation['confidence'],
            data=recommendation['data'],
            fields=recommendation['fields'],
            filters=recommendation['filters'],
            temporal_field=recommendation['temporal_field'],
            explanation=recommendation['explanation'],
            rule_reason=recommendation['rule_reason']
        )
        
        logger.info(f"Generated recommendation: {recommendation['chart_type']}")
        
        return response
    
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing query: {str(e)}"
        )


@router.get("/query/examples")
async def get_example_queries():
    """Get example queries that users can try."""
    return {
        "examples": [
            {
                "query": "Show wheat production trends in Europe over time",
                "description": "Time series showing wheat production changes"
            },
            {
                "query": "Compare maize production across countries",
                "description": "Bar chart comparing production between nations"
            },
            {
                "query": "What are the top wheat producing regions?",
                "description": "Ranking of regions by wheat production"
            },
            {
                "query": "Show production breakdown by commodity",
                "description": "Pie chart showing proportion of different crops"
            },
            {
                "query": "How does USA wheat production compare to Europe?",
                "description": "Comparison between major producing regions"
            },
        ]
    }
