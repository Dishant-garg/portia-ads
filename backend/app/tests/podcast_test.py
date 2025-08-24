from app.agents.podcast_plans import create_podcast_production_system
from app.core.portia_client import PortiaClient

def test_run_podcast_plan():
    client = PortiaClient()
    plan = create_podcast_production_system()
    plan_run_inputs = {
        "episode_topic": "AI in Healthcare: The Future of Medical Diagnosis",
        "source_content": "AI is revolutionizing healthcare by improving diagnostic accuracy and reducing medical errors...",
        "target_duration": 25,
        "host_style": "conversational",
        "episode_number": "001"
    }
    result = client.run_plan2(plan, plan_run_inputs=plan_run_inputs)
    print("Plan run result:", result)
    assert result is not None

if __name__ == "__main__":
    test_run_podcast_plan()


