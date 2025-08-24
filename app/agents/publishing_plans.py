from portia import PlanBuilderV2, StepOutput, Input
from ..schema.content_schemas import PublishingResults

def create_notion_publisher():
    """Notion-focused content publishing system for blog/site creation."""
    return (
        PlanBuilderV2("Notion Blog Publishing Pipeline")
        
        .input(name="content_package", description="Complete content package to publish")
        .input(name="publishing_schedule", description="When to publish")
        .input(name="content_id", description="Content identifier for reports", default_value="default")
        
        # Step 1: Format Content for Notion
        .llm_step(
            step_name="format_for_notion",
            task="""
            Optimize content for Notion blog/site publishing:
            
            Source content: {content_package}
            
            Create Notion-optimized version considering:
            1. Notion block structure and formatting
            2. Proper heading hierarchy
            3. Callout boxes and dividers
            4. Code blocks and tables
            5. Image placement and captions
            6. Internal linking structure
            7. Page properties and metadata
            8. SEO-friendly page structure
            
            Generate a well-structured Notion page that functions as a professional blog post.
            """,
            inputs=[Input("content_package")]
        )
        
        # Step 2: Publish to Notion
        .single_tool_agent_step(
            step_name="publish_to_notion",
            tool="portia:mcp:mcp.notion.com:notion_create_pages",
            task="""
            Publish content to Notion as a blog post/site page:
            
            Content: {format_for_notion}
            Publishing schedule: {publishing_schedule}
            
            Tasks:
            1. Log into Notion workspace
            2. use the tool to create a new page
            3. Create new page with optimized content
            4. Add proper Notion blocks (headings, text, callouts, dividers)
            5. Set page properties (title, tags, publish date, status)
            6. Configure page for public sharing/site publication
            7. Enable comments if desired
            8. Get published page URL
            9. Verify page displays correctly in site view
            
            Focus on creating a professional blog post that leverages Notion's site capabilities.
            """,
            inputs=[
                StepOutput("format_for_notion"),
                Input("publishing_schedule")
            ]
        )
        
        # Step 3: Track Publishing Results
        .function_step(
            step_name="compile_publishing_results",
            function=lambda notion_result, content_id: {
                "platform_results": {
                    "notion": "published" if notion_result else "not_published"
                },
                "published_urls": [],
                "publishing_timestamp": "2025-08-24T04:30:00Z",
                "content_id": content_id,
                "status": "completed"
            },
            args={
                "notion_result": StepOutput("publish_to_notion"),
                "content_id": Input("content_id")
            }
        )
        
        # Step 4: Save Publishing Report
        # .invoke_tool_step(
        #     step_name="save_publishing_report",
        #     tool="file_writer_tool",
        #     args={
        #         "filename": f"publishing_reports/notion_publication_report_{Input('content_id')}.json",
        #         "content": StepOutput("compile_publishing_results")
        #     }
        # )




        .final_output(output_schema=PublishingResults)
        .build()
    )
