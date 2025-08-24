import json
import os
from app.agents.content_plans import create_content_planning_system, create_article_writing_system, create_fact_checking_system
from app.core.portia_client import PortiaClient

def test_run_content_planning_system():
    client = PortiaClient()
    plan = create_content_planning_system()
    
    # Load research summary from saved report
    research_summary = ""
    try:
        research_file = "research_reports/AI_in_Healthcare_market_research.json"
        if os.path.exists(research_file):
            with open(research_file, 'r') as f:
                research_summary = f.read()
                print(f"Loaded research report from {research_file}")
        else:
            print(f"Research file not found at {research_file}")
            research_summary = "AI healthcare market research data not available"
    except Exception as e:
        print(f"Error loading research file: {e}")
        research_summary = "AI healthcare market research data not available"
    
    plan_run_inputs = {
        "research_summary": research_summary,
        "content_goals": "Establish thought leadership in AI healthcare, drive engagement from healthcare professionals",
        "brand_guidelines": "Professional yet approachable tone, evidence-based content",
        "publishing_frequency": "3x per week"
    }
    result = client.run_plan2(plan, plan_run_inputs=plan_run_inputs)
    print("Content Planning System result:", result)
    assert result is not None

def test_run_article_writing_system():
    client = PortiaClient()
    plan = create_article_writing_system()
    plan_run_inputs = {
        "topic": "AI-Powered Medical Diagnosis: Transforming Healthcare in 2025",
        "target_keywords": ["AI medical diagnosis", "artificial intelligence healthcare", "AI diagnostics"],
        "word_count_target": 1500,
        "audience_level": "intermediate",
        "content_angle": "Practical implementation guide for healthcare professionals"
    }
    result = client.run_plan2(plan, plan_run_inputs=plan_run_inputs)
    print("Article Writing System result:", result)
    assert result is not None

def test_run_fact_checking_system():
    client = PortiaClient()
    plan = create_fact_checking_system()
    plan_run_inputs = {
        "content_to_verify": """
        AI in healthcare is projected to reach $613.81 billion by 2034, growing at a CAGR of 37%.
        Currently, 100% of healthcare systems use AI for clinical documentation.
        Studies show that 46% of patients use AI symptom checkers for mental health concerns.
        The FDA has approved over 1250 AI-based medical devices as of 2024.
        """,
        "verification_level": "thorough"
    }
    result = client.run_plan2(plan, plan_run_inputs=plan_run_inputs)
    print("Fact Checking System result:", result)
    assert result is not None

if __name__ == "__main__":
    print("Testing Content Planning System...")
    test_run_content_planning_system()
    
    print("\nTesting Article Writing System...")
    test_run_article_writing_system()
    
    print("\nTesting Fact Checking System...")
    test_run_fact_checking_system()
    
    print("\nAll content plan tests completed!")
