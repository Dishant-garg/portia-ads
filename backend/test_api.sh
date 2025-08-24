#!/bin/bash

# Test script for Portia API endpoints
BASE_URL="http://localhost:5000"

echo "=== Testing Portia API Endpoints ==="
echo

# Test 1: List available tools (GET request)
echo "1. Testing /api/tools endpoint..."
curl -X GET "${BASE_URL}/api/tools" \
  -H "Content-Type: application/json" \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 2: Market Research
echo "2. Testing /api/market-research endpoint..."
curl -X POST "${BASE_URL}/api/market-research" \
  -H "Content-Type: application/json" \
  -d '{
    "industry": "Healthcare Technology",
    "target_market": "AI-powered medical diagnosis",
    "research_focus": "market size and trends"
  }' \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 3: Content Gap Analysis
echo "3. Testing /api/content-gap-analysis endpoint..."
curl -X POST "${BASE_URL}/api/content-gap-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "competitor_content": "AI healthcare blog posts",
    "target_audience": "healthcare professionals",
    "content_category": "technical articles"
  }' \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 4: Content Planning
echo "4. Testing /api/content-planning endpoint..."
curl -X POST "${BASE_URL}/api/content-planning" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI in Medical Diagnosis",
    "content_type": "blog_series",
    "target_audience": "healthcare professionals",
    "timeline": "4 weeks"
  }' \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 5: Article Writing
echo "5. Testing /api/article-writing endpoint..."
curl -X POST "${BASE_URL}/api/article-writing" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Future of AI in Medical Diagnosis",
    "target_length": "2000 words",
    "tone": "professional",
    "audience": "healthcare professionals"
  }' \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 6: Fact Checking
echo "6. Testing /api/fact-checking endpoint..."
curl -X POST "${BASE_URL}/api/fact-checking" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AI diagnostic tools have shown 95% accuracy in detecting skin cancer",
    "sources_required": true,
    "verification_level": "high"
  }' \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 7: Podcast Production
echo "7. Testing /api/podcast-production endpoint..."
curl -X POST "${BASE_URL}/api/podcast-production" \
  -H "Content-Type: application/json" \
  -d '{
    "episode_topic": "AI Revolution in Healthcare",
    "duration": "30 minutes",
    "format": "interview",
    "target_audience": "healthcare professionals"
  }' \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 8: Video Production
echo "8. Testing /api/video-production endpoint..."
curl -X POST "${BASE_URL}/api/video-production" \
  -H "Content-Type: application/json" \
  -d '{
    "video_type": "educational",
    "topic": "How AI Improves Medical Diagnosis",
    "duration": "5 minutes",
    "style": "animated explainer"
  }' \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 9: Publishing
echo "9. Testing /api/publishing endpoint..."
curl -X POST "${BASE_URL}/api/publishing" \
  -H "Content-Type: application/json" \
  -d '{
    "content_title": "AI in Healthcare: A Comprehensive Guide",
    "platform": "notion",
    "publish_date": "2025-08-25",
    "tags": ["AI", "Healthcare", "Technology"]
  }' \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

# Test 10: Master Pipeline
echo "10. Testing /api/master-pipeline endpoint..."
curl -X POST "${BASE_URL}/api/master-pipeline" \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "AI Healthcare Content Campaign",
    "content_types": ["article", "podcast", "video"],
    "timeline": "8 weeks",
    "target_audience": "healthcare professionals"
  }' \
  | jq '.' 2>/dev/null || echo "Response received"
echo -e "\n"

echo "=== API Testing Complete ==="
