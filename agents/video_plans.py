from portia import PlanBuilderV2, StepOutput, Input
from schema.content_schemas import VideoPackage

def create_video_production_system():
    """Complete video production pipeline."""
    return (
        PlanBuilderV2("Video Production Pipeline")
        
        .input(name="video_topic", description="Main video topic")
        .input(name="target_platform", description="youtube/tiktok/instagram/linkedin", default_value="youtube")
        .input(name="video_length", description="Target video length", default_value="8-10 minutes")
        .input(name="video_style", description="educational/entertainment/tutorial", default_value="educational")
        .input(name="brand_guidelines", description="Brand colors, fonts, style preferences")
        
        # Step 1: Analyze Platform Requirements
        .invoke_tool_step(
            step_name="research_platform_specs",
            tool="search_tool",
            args={
                "query": f"{Input('target_platform')} video best practices 2024 optimal length format engagement tips"
            }
        )
        
        # Step 2: Analyze High-Performing Videos
        .invoke_tool_step(
            step_name="analyze_viral_videos",
            tool="search_tool",
            args={
                "query": f"viral {Input('video_topic')} videos {Input('target_platform')} high engagement popular"
            }
        )
        
        # Step 3: Create Video Script
        .llm_step(
            task="""
            Create engaging video script for: {video_topic}
            
            Platform: {target_platform}
            Video length: {video_length}
            Style: {video_style}
            Platform research: {research_platform_specs}
            Viral video analysis: {analyze_viral_videos}
            
            Script structure:
            1. Hook (first 15 seconds) - CRITICAL for retention
               - Attention-grabbing statement or question
               - Value preview (what viewers will learn)
               - Visual hook description
            
            2. Introduction (15-30 seconds)
               - Brief personal introduction
               - Problem/topic setup
               - Video outline preview
            
            3. Main Content (60-80% of video)
               - 3-5 key points with clear transitions
               - Visual demonstrations or examples
               - Interactive elements (polls, questions)
               - Screen recordings or graphics cues
            
            4. Call-to-Action (final 10-15 seconds)
               - Subscribe reminder
               - Like/comment request
               - Next video preview
               - Social media links
            
            Include detailed visual cues, on-screen text suggestions, and pacing notes.
            """,
            inputs=[
                Input("video_topic"),
                Input("target_platform"),
                Input("video_length"),
                Input("video_style"),
                StepOutput("research_platform_specs"),
                StepOutput("analyze_viral_videos")
            ],
            name="create_video_script"
        )
        
        # Step 4: Create Shot List and Visual Plan
        .llm_step(
            task="""
            Create detailed shot list and visual plan: {create_video_script}
            
            Platform: {target_platform}
            Brand guidelines: {brand_guidelines}
            
            For each script section, specify:
            1. Camera angles and shots
            2. Visual elements needed (graphics, text, animations)
            3. B-roll footage requirements
            4. Screen recordings or demonstrations
            5. Lighting and setup requirements
            6. Props or materials needed
            7. Timing for each shot
            8. Transition effects between scenes
            """,
            inputs=[
                StepOutput("create_video_script"),
                Input("target_platform"),
                Input("brand_guidelines")
            ],
            name="create_shot_list"
        )
        
        # Step 5: Generate Thumbnail Concepts
        .llm_step(
            task="""
            Generate thumbnail design concepts for video: {video_topic}
            
            Platform: {target_platform}
            Brand guidelines: {brand_guidelines}
            Video style: {video_style}
            
            Create 5 thumbnail concepts with:
            1. Title text (large, readable)
            2. Visual elements and composition
            3. Color scheme (brand-aligned)
            4. Facial expressions or key visuals
            5. Platform-specific dimensions
            6. A/B testing variations
            
            Focus on click-through optimization and brand consistency.
            """,
            inputs=[
                Input("video_topic"),
                Input("target_platform"),
                Input("brand_guidelines"),
                Input("video_style")
            ],
            name="generate_thumbnail_concepts"
        )
        
        # Step 6: Create Video Metadata
        .llm_step(
            task="""
            Create optimized video metadata: {create_video_script}
            
            Topic: {video_topic}
            Platform: {target_platform}
            
            Generate:
            1. SEO-optimized title (multiple variations)
            2. Compelling description with keywords
            3. Relevant tags/hashtags
            4. Chapter markers with timestamps
            5. End screen elements
            6. Cards/annotations placement
            7. Playlist suggestions
            8. Upload schedule recommendations
            """,
            inputs=[
                StepOutput("create_video_script"),
                Input("video_topic"),
                Input("target_platform")
            ],
            name="create_video_metadata"
        )
        
        # Step 7: Generate Editing Instructions
        .llm_step(
            task="""
            Create comprehensive editing instructions:
            
            Script: {create_video_script}
            Shot list: {create_shot_list}
            Platform: {target_platform}
            Brand guidelines: {brand_guidelines}
            
            Editing guidelines:
            1. Pacing and rhythm (quick cuts vs. slow burns)
            2. Music and audio levels
            3. Color grading and visual style
            4. Text overlays and graphics timing
            5. Transition effects between scenes
            6. B-roll integration points
            7. Audio cleanup and enhancement
            8. Export settings for platform
            9. Quality control checklist
            """,
            inputs=[
                StepOutput("create_video_script"),
                StepOutput("create_shot_list"),
                Input("target_platform"),
                Input("brand_guidelines")
            ],
            name="create_editing_instructions"
        )
        
        # Step 8: Package Video Production Materials
        .function_step(
            function=lambda script, shots, thumbs, metadata, editing, topic, platform: {
                "video_script": script,
                "shot_list": shots,
                "thumbnail_concepts": thumbs,
                "video_metadata": metadata,
                "editing_instructions": editing,
                "production_details": {
                    "topic": topic,
                    "platform": platform,
                    "estimated_production_time": "4-6 hours",
                    "required_equipment": ["camera", "microphone", "lighting"],
                    "status": "ready_for_production"
                }
            },
            args={
                "script": StepOutput("create_video_script"),
                "shots": StepOutput("create_shot_list"),
                "thumbs": StepOutput("generate_thumbnail_concepts"),
                "metadata": StepOutput("create_video_metadata"),
                "editing": StepOutput("create_editing_instructions"),
                "topic": Input("video_topic"),
                "platform": Input("target_platform")
            },
            name="package_video_materials"
        )
        
        # Step 9: Save Video Package
        .invoke_tool_step(
            step_name="save_video_package",
            tool="file_writer_tool",
            args={
                "filename": f"video_production/{Input('video_topic')}_production_package.json",
                "content": StepOutput("package_video_materials")
            }
        )
        
        .final_output(output_schema=VideoPackage)
        .build()
    )
