import json
import os
from app.agents.content_plans import create_content_planning_system
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
    print("Plan run result:", result)
    assert result is not None

if __name__ == "__main__":
    test_run_content_planning_system()
