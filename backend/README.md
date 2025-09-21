# Advanced Feedback Agent Backend

A FastAPI backend with an AI-powered feedback analysis system using Pydantic AI and Google Gemini.

## Features

### Basic Analytics
- Average rating calculation
- Sentiment analysis using TextBlob
- Common keyword extraction
- Statistical summaries

### AI-Powered Analytics
- **Comprehensive Insights**: AI-generated analysis of feedback patterns, themes, and trends
- **Individual Analysis**: Detailed AI analysis of specific feedback items
- **Priority Issues**: Automatic identification of high-priority problems
- **Feature Requests**: Extraction and categorization of feature requests
- **Sentiment Classification**: Advanced emotional tone detection
- **Actionable Recommendations**: Specific improvement suggestions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

3. Run the application:
```bash
uvicorn main:router --reload
```

## API Endpoints

### Submit Feedback
```http
POST /feedback
Content-Type: application/json

{
  "user_id": "user123",
  "rating": 4,
  "comment": "Great product but could use better documentation",
  "category": "general",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

### Get Basic Insights
```http
GET /feedback/basic-insights
```
Returns traditional analytics without AI processing.

### Get AI Insights
```http
GET /feedback/ai-insights
```
Returns comprehensive AI-powered analysis including:
- Overall sentiment assessment
- Key themes and patterns
- Improvement suggestions
- Urgency levels
- Trending issues

### Get Priority Issues
```http
GET /feedback/priority-issues
```
Returns feedback items that require immediate attention.

### Get Feature Requests
```http
GET /feedback/feature-requests
```
Returns categorized feature requests with AI analysis.

### Analyze Individual Feedback
```http
POST /feedback/analyze/{feedback_id}
```
Get detailed AI analysis of a specific feedback item.

### Get All Feedback
```http
GET /feedback/all
```
Returns all stored feedback with count.

## Response Examples

### AI Insights Response
```json
{
  "ai_insights": {
    "overall_sentiment": "positive",
    "sentiment_score": 0.65,
    "key_themes": ["documentation", "user experience", "performance"],
    "improvement_suggestions": [
      "Improve documentation clarity",
      "Add more tutorials",
      "Optimize loading times"
    ],
    "urgency_level": "medium",
    "category_breakdown": {
      "bug": 2,
      "feature": 5,
      "general": 8
    },
    "trending_issues": ["slow loading", "confusing UI"],
    "positive_highlights": ["great design", "helpful support"]
  },
  "statistics": {
    "total_feedback": 15,
    "average_rating": 4.2,
    "rating_distribution": {
      "5": 8,
      "4": 4,
      "3": 2,
      "2": 1,
      "1": 0
    }
  }
}
```

### Individual Analysis Response
```json
{
  "feedback": {
    "user_id": "user123",
    "rating": 2,
    "comment": "App crashes frequently on login",
    "category": "bug"
  },
  "analysis": {
    "main_concern": "Application stability issues during authentication",
    "emotion": "frustrated",
    "priority": "high",
    "category": "bug",
    "actionable_items": [
      "Investigate login authentication flow",
      "Add error handling for crash scenarios",
      "Implement login retry mechanism"
    ]
  }
}
```

## Environment Variables

- `GEMINI_API_KEY`: Your Google Gemini API key for Pydantic AI functionality

## Dependencies

- **FastAPI**: Web framework
- **Pydantic AI**: AI-powered analysis with structured outputs
- **TextBlob**: Basic sentiment analysis
- **Google Gemini**: Language model for advanced analysis
- **SlowAPI**: Rate limiting middleware
- **Redis**: Rate limiting storage (optional)

## Architecture

The system uses Pydantic AI to provide structured, validated AI responses. The `AdvancedFeedbackAgent` class includes:

1. **FeedbackInsights**: Comprehensive analysis model
2. **FeedbackSummary**: Individual feedback analysis model
3. **Dual AI Agents**: Specialized agents for different analysis types
4. **Backward Compatibility**: Legacy `FeedbackAgent` still works

## Error Handling

## Rate Limiting

The system includes built-in rate limiting for AI API calls:
- **Limit**: 2 requests per minute per agent instance
- **Behavior**: Automatically waits when limit is reached
- **Thread-safe**: Uses threading locks for concurrent safety

All AI endpoints include proper error handling and will return HTTP 500 with descriptive error messages if AI analysis fails. Basic endpoints remain functional even without Gemini API access.