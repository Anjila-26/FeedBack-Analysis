from pydantic import BaseModel, Field
from typing import Optional
from typing import List, Dict

class Feedback(BaseModel):
    user_id: Optional[str]
    rating: int = Field(..., ge=1, le=5)
    comment: str
    timestamp: Optional[str]
    category: Optional[str]  # e.g., 'bug', 'feature', 'general'

class FeedbackInsights(BaseModel):
    """Structured insights from feedback analysis."""
    overall_sentiment: str = Field(description="Overall sentiment: positive, negative, or neutral")
    sentiment_score: float = Field(description="Sentiment score between -1 and 1")
    key_themes: List[str] = Field(description="Main themes or topics mentioned")
    improvement_suggestions: List[str] = Field(description="Specific suggestions for improvement")
    urgency_level: str = Field(description="Urgency level: low, medium, high, critical")
    category_breakdown: Dict[str, int] = Field(description="Count of feedback by category")
    trending_issues: List[str] = Field(description="Issues that appear frequently")
    positive_highlights: List[str] = Field(description="What users like most")

class FeedbackSummary(BaseModel):
    """Summary of individual feedback."""
    main_concern: str = Field(description="Primary concern or topic")
    emotion: str = Field(description="Emotional tone: frustrated, satisfied, confused, etc.")
    priority: str = Field(description="Priority level: low, medium, high")
    category: str = Field(description="Category: bug, feature, usability, performance, etc.")
    actionable_items: List[str] = Field(description="Specific actionable items")
