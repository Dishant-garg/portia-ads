from portia import PlanBuilderV2, StepOutput, Input
from schema.content_schemas import PublishingResults

def create_multi_platform_publisher():
    """Multi-platform content publishing system."""
    return (
        PlanBuilderV2("Multi-Platform Publishing Pipeline")
        
        .input(name="content_package", description="Complete content package to publish")
        .input(name="publishing_schedule", description="When and where to publish")
        .input(name="target_platforms", description="List of platforms to publish to")
        .input(name="approval_required", description="Require human approval before publishing", default_value=True)
        
        # Step 1: Format Content for Each Platform
        .llm_step(
            task="""
            Adapt content for each target platform: {target_platforms}
            
            Source content: {content_package}
            
            For each platform, create optimized version considering:
            1. Platform-specific character/word limits
            2. Hashtag and mention conventions
            3. Visual content requirements
            4. Engagement optimization tactics
            5. Platform algorithm preferences
            6. Audience behavior patterns
            
            Generate platform-specific versions maintaining core message consistency.
            """,
            inputs=[
                Input("target_platforms"),
                Input("content_package")
            ],
            name="format_for_platforms"
        )
        
        # Step 2: Human Approval Gate (if required)
        .if_(
            condition=lambda approval: approval == True,
            args={"approval": Input("approval_required")}
        )
        .llm_step(
            task="""
            Review content for publishing approval:
            
            Content package: {content_package}
            Platform versions: {format_for_platforms}
            Publishing schedule: {publishing_schedule}
            
            Assess:
            1. Content quality and accuracy
            2. Brand voice consistency
            3. Legal/compliance considerations
            4. Timing appropriateness
            5. Platform optimization quality
            
            Determine if human approval is needed based on:
            - Sensitive topics
            - High-stakes campaigns
            - New audience segments
            - Regulatory considerations
            
            If approval needed, raise clarification with specific review points.
            """,
            inputs=[
                Input("content_package"),
                StepOutput("format_for_platforms"),
                Input("publishing_schedule")
            ],
            name="approval_review"
        )
        .endif()
        
        # Step 3: WordPress Publishing
        .if_(
            condition="'wordpress' in target_platforms",
            args={"target_platforms": Input("target_platforms")}
        )
        .single_tool_agent_step(
            tool="browser_tool",
            task="""
            Publish content to WordPress:
            
            Content: {format_for_platforms.wordpress_version}
            
            Tasks:
            1. Log into WordPress admin
            2. Create new post with optimized content
            3. Add featured image and alt text
            4. Set categories and tags
            5. Configure SEO settings
            6. Schedule or publish based on timing
            7. Verify publication and get URL
            """,
            inputs=[StepOutput("format_for_platforms")],
            name="publish_to_wordpress"
        )
        .endif()
        
        # Step 4: YouTube Publishing
        .if_(
            condition="'youtube' in target_platforms",
            args={"target_platforms": Input("target_platforms")}
        )
        .single_tool_agent_step(
            tool="browser_tool", 
            task="""
            Upload video to YouTube:
            
            Video metadata: {format_for_platforms.youtube_version}
            
            Tasks:
            1. Access YouTube Studio
            2. Upload video file
            3. Add optimized title and description
            4. Set appropriate tags
            5. Upload custom thumbnail
            6. Configure end screens and cards
            7. Set visibility and schedule
            8. Get video URL and analytics setup
            """,
            inputs=[StepOutput("format_for_platforms")],
            name="publish_to_youtube"
        )
        .endif()
        
        # Step 5: Social Media Publishing
        .if_(
            condition="any platform in ['twitter', 'linkedin', 'facebook', 'instagram'] in target_platforms",
            args={"target_platforms": Input("target_platforms")}
        )
        .invoke_tool_step(
            step_name="publish_to_social_media",
            tool="apify_actor",
            args={
                "actor_id": "apify/social-media-publisher",  # If available
                "input": {
                    "platforms": Input("target_platforms"),
                    "content_variants": StepOutput("format_for_platforms"),
                    "schedule": Input("publishing_schedule")
                }
            }
        )
        .endif()
        
        # Step 6: Podcast Distribution
        .if_(
            condition="'podcast' in content_package.content_types",
            args={"content_package": Input("content_package")}
        )
        .llm_step(
            task="""
            Prepare podcast for distribution:
            
            Podcast content: {content_package.podcast_version}
            
            Create distribution package with:
            1. RSS feed updates
            2. Spotify podcast submission
            3. Apple Podcasts metadata
            4. Google Podcasts optimization
            5. Episode show notes formatting
            6. Transcript preparation
            7. Social media promotion posts
            """,
            inputs=[Input("content_package")],
            name="distribute_podcast"
        )
        .endif()
        
        # Step 7: Track Publishing Results
        .function_step(
            function=lambda wordpress, youtube, social, podcast, platforms: {
                "platform_results": {
                    "wordpress": wordpress if wordpress else "not_published",
                    "youtube": youtube if youtube else "not_published", 
                    "social_media": social if social else "not_published",
                    "podcast": podcast if podcast else "not_published"
                },
                "published_urls": [
                    url for url in [
                        wordpress.get("url") if wordpress else None,
                        youtube.get("url") if youtube else None,
                        social.get("urls") if social else None
                    ] if url
                ],
                "publishing_timestamp": "2025-08-24T04:30:00Z",
                "platforms_targeted": platforms,
                "status": "published"
            },
            args={
                "wordpress": StepOutput("publish_to_wordpress"),
                "youtube": StepOutput("publish_to_youtube"),
                "social": StepOutput("publish_to_social_media"),
                "podcast": StepOutput("distribute_podcast"),
                "platforms": Input("target_platforms")
            },
            name="compile_publishing_results"
        )
        
        # Step 8: Save Publishing Report
        .invoke_tool_step(
            step_name="save_publishing_report",
            tool="file_writer_tool",
            args={
                "filename": f"publishing_reports/publication_report_{Input('content_id', 'default')}.json",
                "content": StepOutput("compile_publishing_results")
            }
        )
        
        .final_output(output_schema=PublishingResults)
        .build()
    )
