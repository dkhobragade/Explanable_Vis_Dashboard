"""
Feedback Endpoint
Collects user feedback about recommendations.
"""
from fastapi import APIRouter, HTTPException
from ..schemas import FeedbackRequest, FeedbackResponse
from datetime import datetime
import uuid
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["feedback"])

FEEDBACK_FILE = Path("backend/feedback/feedback_log.jsonl")


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest) -> FeedbackResponse:
    """
    Submit feedback about a chart recommendation.
    
    Args:
        request (FeedbackRequest): Feedback data
        
    Returns:
        FeedbackResponse: Confirmation with feedback ID
    """
    try:
        # Generate feedback ID
        feedback_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        # Prepare feedback record
        feedback_record = {
            "feedback_id": feedback_id,
            "timestamp": timestamp.isoformat(),
            "query": request.query,
            "recommended_chart": request.recommended_chart,
            "user_preferred_chart": request.user_preferred_chart,
            "helpful": request.helpful,
            "comments": request.comments,
            "user_id": request.user_id or "anonymous"
        }
        
        # Save feedback (append to JSONL file)
        FEEDBACK_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(FEEDBACK_FILE, 'a') as f:
            f.write(json.dumps(feedback_record) + '\n')
        
        logger.info(f"Feedback recorded: {feedback_id}")
        
        response = FeedbackResponse(
            feedback_id=feedback_id,
            received_at=timestamp,
            message="Thank you for your feedback! It helps us improve recommendations."
        )
        
        return response
    
    except Exception as e:
        logger.error(f"Error saving feedback: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saving feedback: {str(e)}"
        )


@router.get("/feedback/stats")
async def get_feedback_stats():
    """Get statistics about collected feedback."""
    try:
        if not FEEDBACK_FILE.exists():
            return {
                "total_feedback": 0,
                "helpful_count": 0,
                "helpful_percentage": 0.0,
                "most_recommended_chart": None,
                "most_preferred_chart": None
            }
        
        feedback_list = []
        with open(FEEDBACK_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    feedback_list.append(json.loads(line))
        
        if not feedback_list:
            return {
                "total_feedback": 0,
                "helpful_count": 0,
                "helpful_percentage": 0.0
            }
        
        # Calculate stats
        total = len(feedback_list)
        helpful = sum(1 for fb in feedback_list if fb.get('helpful', False))
        
        # Most common recommendations
        recommended_charts = {}
        preferred_charts = {}
        
        for fb in feedback_list:
            rec = fb.get('recommended_chart')
            if rec:
                recommended_charts[rec] = recommended_charts.get(rec, 0) + 1
            
            pref = fb.get('user_preferred_chart')
            if pref:
                preferred_charts[pref] = preferred_charts.get(pref, 0) + 1
        
        return {
            "total_feedback": total,
            "helpful_count": helpful,
            "helpful_percentage": helpful / total if total > 0 else 0.0,
            "most_recommended_chart": max(recommended_charts, key=recommended_charts.get) if recommended_charts else None,
            "most_preferred_chart": max(preferred_charts, key=preferred_charts.get) if preferred_charts else None,
        }
    
    except Exception as e:
        logger.error(f"Error getting feedback stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting feedback stats: {str(e)}"
        )
