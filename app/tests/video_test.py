from app.agents.video_plans import create_video_production_system
from app.core.portia_client import PortiaClient

def test_run_video_plan():
    client = PortiaClient()
    plan = create_video_production_system()
    plan_run_inputs = {
        "video_topic": "AI-Powered Medical Diagnosis Explained",
        "target_platform": "youtube",
        "video_length": "8-10 minutes",
        "video_style": "educational",
        "brand_guidelines": "Professional blue theme, modern fonts, clean graphics"
    }
    result = client.run_plan2(plan, plan_run_inputs=plan_run_inputs)
    print("Plan run result:", result)
    assert result is not None

if __name__ == "__main__":
    test_run_video_plan()
