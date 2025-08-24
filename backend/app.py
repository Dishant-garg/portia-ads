from portia import Portia, PlanBuilderV2, StepOutput, Input, Config
from schema.content_schemas import FinalContentOutput
from agents.research_plans import create_market_research_plan
from agents.content_plans import create_content_planning_system, create_article_writing_system, create_fact_checking_system
from agents.podcast_plans import create_podcast_production_system
from agents.video_plans import create_video_production_system
from agents.publishing_plans import create_multi_platform_publisher

def create_master_content_production_system():
    """Master orchestrator for complete content production pipeline."""
    return (
        PlanBuilderV2("Master AI Content Production System")
        
        # Define all inputs
        .input(name="project_name", description="Name of the content production project")
        .input(name="primary_topic", description="Main topic for content creation")
        .input(name="target_audience", description="Target audience demographics and interests")
        .input(name="content_formats", description="List of content formats to create", 
               default_value=["article", "social_media"])
        .input(name="publishing_platforms", description="Platforms to publish content on")
        .input(name="brand_guidelines", description="Brand voice, style, and visual guidelines")
        .input(name="project_deadline", description="Project completion deadline")
        .input(name="approval_level", description="low/medium/high human oversight", default_value="medium")
        
        # Phase 1: Market Research & Analysis
        .sub_plan(
            plan=create_market_research_plan(),
            plan_inputs={
                "topic": Input("primary_topic"),
                "target_audience": Input("target_audience"),
                "research_depth": "comprehensive"
            },
            name="market_research_phase"
        )
        
        # Phase 2: Content Strategy & Planning
        .sub_plan(
            plan=create_content_planning_system(),
            plan_inputs={
                "research_summary": StepOutput("market_research_phase"),
                "content_goals": f"Create engaging {Input('content_formats')} content about {Input('primary_topic')}",
                "brand_guidelines": Input("brand_guidelines")
            },
            name="content_planning_phase"
        )
        
        # Phase 3: Article Creation (if requested)
        .if_(
            condition="'article' in content_formats",
            args={"content_formats": Input("content_formats")}
        )
        .sub_plan(
            plan=create_article_writing_system(),
            plan_inputs={
                "topic": Input("primary_topic"),
                "target_keywords": StepOutput("market_research_phase.target_keywords"),
                "audience_level": "intermediate",
                "content_angle": StepOutput("content_planning_phase.recommended_angles[0]")
            },
            name="article_creation_phase"
        )
        .endif()
        
        # Phase 4: Fact-Checking & Quality Control
        .if_(
            condition="'article' in content_formats",
            args={"content_formats": Input("content_formats")}
        )
        .sub_plan(
            plan=create_fact_checking_system(),
            plan_inputs={
                "content_to_verify": StepOutput("article_creation_phase.main_article"),
                "verification_level": "thorough"
            },
            name="fact_checking_phase"
        )
        .endif()
        
        # Phase 5: Podcast Production (if requested)
        .if_(
            condition="'podcast' in content_formats",
            args={"content_formats": Input("content_formats")}
        )
        .sub_plan(
            plan=create_podcast_production_system(),
            plan_inputs={
                "episode_topic": Input("primary_topic"),
                "source_content": StepOutput("article_creation_phase.main_article"),
                "target_duration": 25,
                "episode_number": 1
            },
            name="podcast_production_phase"
        )
        .endif()
        
        # Phase 6: Video Production (if requested)
        .if_(
            condition="'video' in content_formats",
            args={"content_formats": Input("content_formats")}
        )
        .sub_plan(
            plan=create_video_production_system(),
            plan_inputs={
                "video_topic": Input("primary_topic"),
                "target_platform": "youtube",
                "video_style": "educational",
                "brand_guidelines": Input("brand_guidelines")
            },
            name="video_production_phase"
        )
        .endif()
        
        # Phase 7: Human Approval Gate
        .llm_step(
            task="""
            Review all created content for final approval:
            
            Project: {project_name}
            Content created: {content_formats}
            Article (if created): {article_creation_phase}
            Fact-check results (if done): {fact_checking_phase}
            Podcast (if created): {podcast_production_phase}
            Video (if created): {video_production_phase}
            Approval level: {approval_level}
            
            Assess:
            1. Overall content quality and consistency
            2. Brand alignment across all formats
            3. Fact-checking results and accuracy
            4. Target audience appropriateness
            5. Publishing readiness
            
            If approval_level is 'high' or any quality issues detected, raise clarification for human review.
            Otherwise, approve for publishing.
            """,
            inputs=[
                Input("project_name"),
                Input("content_formats"),
                StepOutput("article_creation_phase"),
                StepOutput("fact_checking_phase"),
                StepOutput("podcast_production_phase"),
                StepOutput("video_production_phase"),
                Input("approval_level")
            ],
            name="final_approval_gate"
        )
        
        # Phase 8: Multi-Platform Publishing
        .sub_plan(
            plan=create_multi_platform_publisher(),
            plan_inputs={
                "content_package": {
                    "article": StepOutput("article_creation_phase"),
                    "podcast": StepOutput("podcast_production_phase"),
                    "video": StepOutput("video_production_phase")
                },
                "target_platforms": Input("publishing_platforms"),
                "approval_required": False  # Already approved above
            },
            name="publishing_phase"
        )
        
        # Phase 9: Generate Final Report
        .llm_step(
            task="""
            Generate comprehensive project completion report:
            
            Project: {project_name}
            Topic: {primary_topic}
            Research results: {market_research_phase}
            Content created: {content_formats}
            Publishing results: {publishing_phase}
            
            Create final report with:
            1. Executive summary of deliverables
            2. Content performance predictions
            3. Key metrics to track
            4. Next content recommendations
            5. Lessons learned and optimizations
            6. Resource utilization summary
            """,
            inputs=[
                Input("project_name"),
                Input("primary_topic"),
                StepOutput("market_research_phase"),
                Input("content_formats"),
                StepOutput("publishing_phase")
            ],
            name="generate_final_report"
        )
        
        # Step 10: Save Complete Project
        .invoke_tool_step(
            step_name="save_complete_project",
            tool="file_writer_tool",
            args={
                "filename": f"completed_projects/{Input('project_name')}_complete.json",
                "content": StepOutput("generate_final_report")
            }
        )
        
        .final_output(
            output_schema=FinalContentOutput,
            summarize=True
        )
        .build()
    )

# Example usage
if __name__ == "__main__":
    from portia import Portia, Config, LogLevel
    
    # Initialize Portia with all available tools
    portia = Portia(
        Config.from_default(default_log_level=LogLevel.INFO)
        # Tools will be automatically loaded from the registry
    )
    
    # Create the master plan
    master_plan = create_master_content_production_system()
    
    # Execute with sample inputs
    project_inputs = {
        "project_name": "AI Marketing Guide 2025",
        "primary_topic": "AI-powered content marketing strategies",
        "target_audience": "Digital marketers and business owners aged 25-45",
        "content_formats": ["article", "podcast", "video", "social_media"],
        "publishing_platforms": ["wordpress", "youtube", "linkedin", "twitter"],
        "brand_guidelines": "Professional, approachable, data-driven tone with blue/white color scheme",
        "project_deadline": "2025-09-01",
        "approval_level": "medium"
    }
    
    # Run the complete pipeline
    result = portia.run_plan(master_plan, plan_run_inputs=project_inputs)
    
    print("🎉 Content Production Pipeline Completed!")
    print(f"Project Status: {result.outputs.final_output.value.status}")
    print(f"Deliverables: {result.outputs.final_output.value.deliverables}")
