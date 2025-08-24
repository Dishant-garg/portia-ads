from app.agents.video_plans import create_video_production_system
from app.core.portia_client import PortiaClient

def test_video_production_plan():
    client = PortiaClient()
    plan = create_video_production_system()
    plan_run_inputs = {
        "video_topic": "AI in Healthcare",
        "video_style": "educational",
        "brand_guidelines": "Healthcare professionals, hospital administrators, medical researchers",
        "target_platform": "youtube"
    }
    result = client.run_plan2(plan, plan_run_inputs)
    print("Video production plan result:")
    print(result)
    assert result is not None

if __name__ == "__main__":
    test_video_production_plan()