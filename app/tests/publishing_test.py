from app.agents.publishing_plans import create_multi_platform_publisher
from app.core.portia_client import PortiaClient

def test_run_publishing_plan():
    client = PortiaClient()
    plan = create_multi_platform_publisher()
    plan_run_inputs = {
        "content_package": {
            "main_article": "# AI-Powered Medical Diagnosis: Transforming Healthcare in 2025\n\nArtificial intelligence is revolutionizing medical diagnosis...",
            "social_variants": {
                "twitter": "🚀 AI is transforming healthcare diagnosis! New study shows 95% accuracy in early disease detection. #AIHealthcare #MedicalAI",
                "linkedin": "Healthcare professionals: AI diagnostic tools are now achieving 95% accuracy rates...",
                "facebook": "Did you know AI can now detect diseases earlier than traditional methods?"
            },
            "seo_analysis": "Optimized for keywords: AI medical diagnosis, healthcare AI, medical technology",
            "content_types": ["blog", "social"]
        },
        "publishing_schedule": "2025-08-24T10:00:00Z",
        "target_platforms": ["wordpress", "twitter", "linkedin"],
        "approval_required": False
    }
    result = client.run_plan2(plan, plan_run_inputs=plan_run_inputs)
    print("Plan run result:", result)
    assert result is not None

if __name__ == "__main__":
    test_run_publishing_plan()
