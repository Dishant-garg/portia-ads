from app.agents.research_plans import create_market_research_plan
from app.core.portia_client import PortiaClient

def test_run_market_research_plan():
    client = PortiaClient()
    plan = create_market_research_plan()
    plan_run_inputs = {
    "topic": "AI_in_Healthcare",
    "target_audience": "Healthcare professionals, hospital administrators, medical researchers",
    "competitor_domains": ["healthitnews.com", "medicalfuturist.com"],
    "research_depth": "comprehensive"
}
    result = client.run_plan2(plan, plan_run_inputs=plan_run_inputs)
    print("Plan run result:", result)
    assert result is not None

if __name__ == "__main__":
    test_run_market_research_plan()