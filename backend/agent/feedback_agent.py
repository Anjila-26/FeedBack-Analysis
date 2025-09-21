import os
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from models.feedback import Feedback, FeedbackInsights, FeedbackSummary
from collections import Counter
import json

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider

from textblob import TextBlob
from rate_limiter import get_rate_limiter

class AdvancedFeedbackAgent:
    def __init__(self, feedbacks: List[Feedback], use_redis_rate_limiter: bool = False):
        self.feedbacks = feedbacks
        self.rate_limiter = get_rate_limiter(
            max_calls=2,
            time_window=60,
            use_redis=use_redis_rate_limiter
        )

        # Initialize AI agents (optional - graceful fallback if not available)
        self.ai_enabled = False
        self.feedback_analyzer = None
        self.insights_generator = None

        try:
            api_key = os.getenv('GEMINI_API_KEY')
            if api_key:
                provider = GoogleProvider(api_key=api_key)
                model = GoogleModel('gemini-1.5-flash', provider=provider)

                # Agent for analyzing individual feedback
                self.feedback_analyzer = Agent(
                    model,
                    result_type=FeedbackSummary,
                    system_prompt="""
                    You are an expert feedback analyst. Analyze individual customer feedback
                    to extract key insights, categorize issues, and identify actionable items.
                    Focus on understanding the user's intent, emotional state, and specific problems.
                    """
                )

                # Agent for generating comprehensive insights
                self.insights_generator = Agent(
                    model,
                    result_type=FeedbackInsights,
                    system_prompt="""
                    You are a product insights specialist. Analyze collections of feedback to
                    identify patterns, trends, and strategic insights. Provide actionable
                    recommendations for product improvement and prioritize issues by impact.
                    """
                )
                self.ai_enabled = True
            else:
                print("AI features disabled: GEMINI_API_KEY not set")
                self.ai_enabled = False
        except Exception as e:
            print(f"AI features disabled: {e}")
            self.ai_enabled = False

    def average_rating(self) -> Optional[float]:
        """Calculate average rating."""
        if not self.feedbacks:
            return None
        ratings = [f.rating for f in self.feedbacks]
        return sum(ratings) / len(ratings)

    def sentiment_analysis(self) -> Optional[float]:
        """Basic sentiment analysis using TextBlob."""
        if not self.feedbacks:
            return None

        try:
            sentiments = [TextBlob(f.comment).sentiment.polarity for f in self.feedbacks]
            return sum(sentiments) / len(sentiments)
        except:
            # Fallback: simple rating-based sentiment
            ratings = [f.rating for f in self.feedbacks]
            avg_rating = sum(ratings) / len(ratings)
            return (avg_rating - 3) / 2  # Convert 1-5 scale to -1 to 1

    def common_keywords(self, n: int = 5) -> List[tuple]:
        """Extract most common keywords."""
        if not self.feedbacks:
            return []
        words = []
        for f in self.feedbacks:
            words += f.comment.lower().split()
        return Counter(words).most_common(n)

    def _basic_feedback_analysis(self, feedback: Feedback) -> FeedbackSummary:
        """Basic fallback analysis when AI is not available."""
        try:
            sentiment = TextBlob(feedback.comment).sentiment.polarity
        except:
            # Fallback: simple rating-based sentiment
            sentiment = (feedback.rating - 3) / 2

        # Determine emotion based on rating and sentiment
        if feedback.rating >= 4 and sentiment > 0.1:
            emotion = "satisfied"
        elif feedback.rating <= 2 or sentiment < -0.1:
            emotion = "frustrated"
        else:
            emotion = "neutral"

        # Determine priority based on rating
        if feedback.rating <= 2:
            priority = "high"
        elif feedback.rating == 3:
            priority = "medium"
        else:
            priority = "low"

        # Extract main concern from comment
        main_concern = feedback.comment[:100] + "..." if len(feedback.comment) > 100 else feedback.comment

        return FeedbackSummary(
            main_concern=main_concern,
            emotion=emotion,
            priority=priority,
            category=feedback.category or "general",
            actionable_items=["Review customer feedback", "Follow up if needed"]
        )

    async def analyze_individual_feedback(self, feedback: Feedback) -> FeedbackSummary:
        """Analyze individual feedback using AI with rate limiting."""
        if not self.ai_enabled:
            return self._basic_feedback_analysis(feedback)

        # Apply rate limiting
        self.rate_limiter.wait_if_needed()

        prompt = f"""
        Analyze this customer feedback:

        Rating: {feedback.rating}/5
        Comment: {feedback.comment}
        Category: {feedback.category or 'Not specified'}
        User ID: {feedback.user_id or 'Anonymous'}

        Provide a detailed analysis including the main concern, emotional tone,
        priority level, and specific actionable items.
        """

        result = await self.feedback_analyzer.run(prompt)
        return result.data

    def _basic_comprehensive_insights(self) -> FeedbackInsights:
        """Basic fallback insights when AI is not available."""
        if not self.feedbacks:
            return FeedbackInsights(
                overall_sentiment="neutral",
                sentiment_score=0.0,
                key_themes=[],
                improvement_suggestions=[],
                urgency_level="low",
                category_breakdown={},
                trending_issues=[],
                positive_highlights=[]
            )

        avg_rating = self.average_rating()
        sentiment_score = self.sentiment_analysis()
        keywords = self.common_keywords()

        # Basic sentiment analysis
        if sentiment_score > 0.1:
            overall_sentiment = "positive"
        elif sentiment_score < -0.1:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"

        # Basic urgency assessment
        low_ratings = [f for f in self.feedbacks if f.rating <= 2]
        if len(low_ratings) > len(self.feedbacks) * 0.3:
            urgency_level = "high"
        elif len(low_ratings) > len(self.feedbacks) * 0.1:
            urgency_level = "medium"
        else:
            urgency_level = "low"

        # Category breakdown
        categories = [f.category for f in self.feedbacks if f.category]
        category_breakdown = dict(Counter(categories))

        # Key themes from keywords
        key_themes = [word for word, _ in keywords[:5]]

        return FeedbackInsights(
            overall_sentiment=overall_sentiment,
            sentiment_score=sentiment_score,
            key_themes=key_themes,
            improvement_suggestions=["Analyze detailed feedback", "Address low-rated items"],
            urgency_level=urgency_level,
            category_breakdown=category_breakdown,
            trending_issues=["Check recent feedback patterns"],
            positive_highlights=["Review high-rated feedback"] if avg_rating > 4 else []
        )

    async def generate_comprehensive_insights(self) -> FeedbackInsights:
        """Generate comprehensive insights from all feedback with rate limiting."""
        if not self.feedbacks:
            return FeedbackInsights(
                overall_sentiment="neutral",
                sentiment_score=0.0,
                key_themes=[],
                improvement_suggestions=[],
                urgency_level="low",
                category_breakdown={},
                trending_issues=[],
                positive_highlights=[]
            )

        if not self.ai_enabled:
            return self._basic_comprehensive_insights()

        # Apply rate limiting
        self.rate_limiter.wait_if_needed()

        # Prepare feedback summary for AI analysis
        feedback_summary = []
        for i, feedback in enumerate(self.feedbacks):
            feedback_summary.append({
                "id": i + 1,
                "rating": feedback.rating,
                "comment": feedback.comment,
                "category": feedback.category,
                "timestamp": feedback.timestamp
            })

        avg_rating = self.average_rating()
        sentiment_score = self.sentiment_analysis()

        prompt = f"""
        Analyze this collection of customer feedback and provide comprehensive insights:

        Total Feedback Count: {len(self.feedbacks)}
        Average Rating: {avg_rating:.2f}/5
        Average Sentiment Score: {sentiment_score:.2f}

        Feedback Data:
        {json.dumps(feedback_summary, indent=2)}

        Provide detailed analysis including:
        1. Overall sentiment assessment
        2. Key themes and patterns
        3. Specific improvement suggestions
        4. Urgency assessment
        5. Category breakdown
        6. Trending issues that need attention
        7. Positive aspects users appreciate
        """

        result = await self.insights_generator.run(prompt)
        return result.data

    async def get_priority_issues(self) -> List[Dict[str, Any]]:
        """Get high-priority issues that need immediate attention."""
        priority_issues = []

        for feedback in self.feedbacks:
            if feedback.rating <= 2:  # Low ratings
                analysis = await self.analyze_individual_feedback(feedback)
                if analysis.priority in ['high', 'medium']:
                    priority_issues.append({
                        "feedback": feedback.dict(),
                        "analysis": analysis.dict()
                    })

        return priority_issues

    async def get_feature_requests(self) -> List[Dict[str, Any]]:
        """Extract and categorize feature requests."""
        feature_requests = []

        for feedback in self.feedbacks:
            if feedback.category == 'feature' or 'feature' in feedback.comment.lower():
                analysis = await self.analyze_individual_feedback(feedback)
                feature_requests.append({
                    "feedback": feedback.dict(),
                    "analysis": analysis.dict()
                })

        return feature_requests

    def get_statistics(self) -> Dict[str, Any]:
        """Get basic statistics about the feedback."""
        if not self.feedbacks:
            return {}

        ratings = [f.rating for f in self.feedbacks]
        categories = [f.category for f in self.feedbacks if f.category]

        return {
            "total_feedback": len(self.feedbacks),
            "average_rating": self.average_rating(),
            "rating_distribution": dict(Counter(ratings)),
            "category_distribution": dict(Counter(categories)),
            "sentiment_score": self.sentiment_analysis(),
            "latest_feedback_count": len([f for f in self.feedbacks if f.timestamp]),
        }