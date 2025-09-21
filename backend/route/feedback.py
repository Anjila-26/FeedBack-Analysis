from fastapi import APIRouter, HTTPException
from models.feedback import Feedback
from agent.feedback_agent import AdvancedFeedbackAgent
from typing import List
from database import (
    insert_feedback,
    get_all_feedback,
    get_feedback_by_id,
    get_feedback_count,
    get_feedback_statistics
)

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Feedback API is running"}

@router.post("/feedback")
def submit_feedback(feedback: Feedback):
    feedback_id = insert_feedback(feedback)
    return {"message": "Feedback received", "feedback_id": feedback_id}

@router.get("/feedback/basic-insights")
def basic_feedback_insights():
    """Get basic insights without AI analysis."""
    feedback_list = get_all_feedback()
    if not feedback_list:
        raise HTTPException(status_code=404, detail="No feedback available")

    agent = AdvancedFeedbackAgent(feedback_list)
    db_stats = get_feedback_statistics()

    return {
        "statistics": db_stats,
        "average_rating": agent.average_rating(),
        "average_sentiment": agent.sentiment_analysis(),
        "common_keywords": agent.common_keywords()
    }

@router.get("/feedback/ai-insights")
async def ai_feedback_insights():
    """Get comprehensive AI-powered insights."""
    feedback_list = get_all_feedback()
    if not feedback_list:
        raise HTTPException(status_code=404, detail="No feedback available")

    agent = AdvancedFeedbackAgent(feedback_list)
    try:
        insights = await agent.generate_comprehensive_insights()
        return {
            "ai_insights": insights.dict(),
            "statistics": get_feedback_statistics()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI analysis failed: {str(e)}")

@router.get("/feedback/priority-issues")
async def get_priority_issues():
    """Get high-priority issues that need immediate attention."""
    feedback_list = get_all_feedback()
    if not feedback_list:
        raise HTTPException(status_code=404, detail="No feedback available")

    agent = AdvancedFeedbackAgent(feedback_list)
    try:
        issues = await agent.get_priority_issues()
        return {"priority_issues": issues}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Priority analysis failed: {str(e)}")

@router.get("/feedback/feature-requests")
async def get_feature_requests():
    """Get analyzed feature requests."""
    feedback_list = get_all_feedback()
    if not feedback_list:
        raise HTTPException(status_code=404, detail="No feedback available")

    agent = AdvancedFeedbackAgent(feedback_list)
    try:
        requests = await agent.get_feature_requests()
        return {"feature_requests": requests}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feature analysis failed: {str(e)}")

@router.post("/feedback/analyze/{feedback_id}")
async def analyze_individual_feedback(feedback_id: int):
    """Analyze a specific piece of feedback."""
    feedback = get_feedback_by_id(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    agent = AdvancedFeedbackAgent([feedback])

    try:
        analysis = await agent.analyze_individual_feedback(feedback)
        return {
            "feedback": feedback.dict(),
            "analysis": analysis.dict()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Individual analysis failed: {str(e)}")

@router.get("/feedback/all")
def get_all_feedback_endpoint():
    """Get all stored feedback."""
    feedback_list = get_all_feedback()
    return {"feedback": [f.dict() for f in feedback_list], "count": len(feedback_list)}
