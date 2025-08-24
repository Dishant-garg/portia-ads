from app.agents.publishing_plans import create_notion_publisher
from app.core.portia_client import PortiaClient

def test_run_notion_publishing_plan():
    client = PortiaClient()
    plan = create_notion_publisher()
    plan_run_inputs = {
        "content_package": {
            "main_article": "# AI-Powered Medical Diagnosis: Transforming Healthcare in 2025\n\nArtificial intelligence is revolutionizing medical diagnosis, offering unprecedented accuracy in early disease detection. Recent studies show AI diagnostic tools achieving 95% accuracy rates, significantly outperforming traditional diagnostic methods.\n\n## Key Benefits\n\n- **Early Detection**: AI can identify diseases in their earliest stages\n- **Improved Accuracy**: 95% accuracy vs 80% traditional methods\n- **Cost Reduction**: Lower healthcare costs through prevention\n- **Global Access**: Democratizing expert diagnosis worldwide\n\n## Implementation Challenges\n\nWhile promising, AI medical diagnosis faces several challenges including data privacy concerns, regulatory approval processes, and integration with existing healthcare systems.\n\n## Conclusion\n\nAI-powered medical diagnosis represents a paradigm shift in healthcare, promising better outcomes for patients worldwide.",
            "seo_analysis": "Optimized for keywords: AI medical diagnosis, healthcare AI, medical technology, diagnostic accuracy",
            "content_types": ["blog", "notion_site"]
        },
        "publishing_schedule": "2025-08-24T10:00:00Z",
        "content_id": "ai_medical_diagnosis_2025"
    }
    result = client.run_plan2(plan, plan_run_inputs=plan_run_inputs)
    print("Notion publishing plan result:", result)
    assert result is not None

if __name__ == "__main__":
    test_run_notion_publishing_plan()
