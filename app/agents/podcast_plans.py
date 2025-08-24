from portia import PlanBuilderV2, StepOutput, Input
from ..schema.content_schemas import PodcastPackage

def create_podcast_production_system():
    """Complete podcast production pipeline."""
    return (
        PlanBuilderV2("Podcast Production Pipeline")
        
        .input(name="episode_topic", description="Main topic for podcast episode")
        .input(name="source_content", description="Source article or research content")
        .input(name="target_duration", description="Target episode length in minutes", default_value=25)
        .input(name="host_style", description="Host personality: conversational/professional/energetic", default_value="conversational")
        .input(name="episode_number", description="Episode number for series")
        
        # Step 1: Research Supporting Content
        .invoke_tool_step(
            step_name="research_podcast_content",
            tool="search_tool",
            args={
                "query": f"{Input('episode_topic')} podcast interviews expert insights recent developments 2024"
            }
        )
        
        # Step 2: Find Related Podcasts for Reference
        .invoke_tool_step(
            step_name="analyze_similar_podcasts",
            tool="search_tool",
            args={
                "query": f"popular podcasts about {Input('episode_topic')} high engagement format structure"
            }
        )
        
        # Step 3: Create Podcast Script Structure
        .llm_step(
            task="""
            Create detailed podcast script for: {episode_topic}
            
            Source content: {source_content}
            Research insights: {research_podcast_content}
            Similar podcasts: {analyze_similar_podcasts}
            Target duration: {target_duration} minutes
            Host style: {host_style}
            Episode number: {episode_number}
            
            Script structure:
            1. Intro hook (30-60 seconds)
               - Attention-grabbing opener
               - Episode preview
               - Host introduction
            
            2. Topic introduction (2-3 minutes)
               - Why this topic matters
               - What listeners will learn
               - Personal context/story
            
            3. Main content sections (15-18 minutes)
               - 3-4 key segments with clear transitions
               - Practical examples and stories
               - Audience engagement questions
               - Natural speech patterns and conversational flow
            
            4. Key takeaways (2-3 minutes)
               - Summary of main points
               - Actionable insights
               - Personal recommendations
            
            5. Outro and CTA (1-2 minutes)
               - Episode recap
               - Next episode preview
               - Subscription reminder
               - Contact information
            
            Include timing markers, emphasis notes, and natural pause indicators.
            """,
            inputs=[
                Input("episode_topic"),
                Input("source_content"),
                StepOutput("research_podcast_content"),
                StepOutput("analyze_similar_podcasts"),
                Input("target_duration"),
                Input("host_style"),
                Input("episode_number")
            ],
          
        )
        
        # Step 4: Generate Show Notes
        .llm_step(
            task="""
            Create comprehensive show notes for podcast episode:
            
            Script: {create_podcast_script}
            Episode topic: {episode_topic}
            Episode number: {episode_number}
            
            Show notes should include:
            1. Episode summary (150-200 words)
            2. Key topics discussed with approximate timestamps
            3. Resources and links mentioned
            4. Quotable moments or key insights
            5. Contact information and social links
            6. Previous/next episode links
            7. Transcript highlights
            8. SEO-optimized description for podcast platforms
            """,
            inputs=[
                StepOutput("create_podcast_script"),
                Input("episode_topic"),
                Input("episode_number")
            ],
          
        )
        
        # Step 5: Create Chapter Markers
        .llm_step(
            task="""
            Create chapter markers from podcast script: {create_podcast_script}
            
            Generate:
            1. Chapter titles (descriptive and engaging)
            2. Start timestamps for each chapter
            3. Brief chapter descriptions
            4. Key topics covered in each chapter
            
            Aim for 4-6 chapters for a {target_duration}-minute episode.
            """,
            inputs=[
                StepOutput("create_podcast_script"),
                Input("target_duration")
            ],
          
        )
        
        # Step 6: Generate Audio Production Instructions
        .llm_step(
            task="""
            Create audio production instructions:
            
            Script: {create_podcast_script}
            Host style: {host_style}
            Target duration: {target_duration}
            
            Instructions should cover:
            1. Voice tone and pacing guidance
            2. Emphasis and inflection notes
            3. Background music suggestions (intro/outro/transitions)
            4. Audio effects and processing requirements
            5. Editing guidelines for flow and timing
            6. Quality standards and technical specs
            7. File naming and organization conventions
            """,
            inputs=[
                StepOutput("create_podcast_script"),
                Input("host_style"),
                Input("target_duration")
            ],
          
        )
        
        # Step 7: Package Episode Materials
        .function_step(
            function=lambda script, notes, chapters, audio, topic, episode: {
                "episode_script": script,
                "show_notes": notes,
                "chapter_markers": chapters,
                "audio_instructions": audio,
                "episode_metadata": {
                    "title": f"Episode {episode}: {topic}",
                    "episode_number": episode,
                    "topic": topic,
                    "estimated_duration": f"{Input('target_duration')} minutes",
                    "created_date": "2025-08-24",
                    "status": "ready_for_production"
                }
            },
            args={
                "script": StepOutput("create_podcast_script"),
                "notes": StepOutput("generate_show_notes"),
                "chapters": StepOutput("create_chapter_markers"),
                "audio": StepOutput("create_audio_instructions"),
                "topic": Input("episode_topic"),
                "episode": Input("episode_number")
            },
           
        )
        
        # Step 8: Save Podcast Package
        .invoke_tool_step(
            step_name="save_podcast_package",
            tool="file_writer_tool",
            args={
                "filename": f"podcast_episodes/episode_{Input('episode_number')}_package.json",
                "content": StepOutput("package_episode_materials")
            }
        )
        
        .final_output(output_schema=PodcastPackage)
        .build()
    )

def create_podcast_audio_production():
    """Audio production pipeline using text-to-speech."""
    return (
        PlanBuilderV2("Podcast Audio Production Pipeline")
        
        .input(name="podcast_script", description="Complete podcast script")
        .input(name="voice_settings", description="Voice configuration", default_value={"voice": "professional", "speed": 1.0})
        .input(name="background_music", description="Background music preferences", default_value="subtle_ambient")
        
        # Note: This would use text-to-speech tools when available
        # For now, creating production instructions
        
        # Step 1: Prepare Script for TTS
        .llm_step(
            task="""
            Prepare script for text-to-speech production: {podcast_script}
            
            Voice settings: {voice_settings}
            
            Create TTS-optimized version with:
            1. SSML tags for emphasis and pauses
            2. Pronunciation guides for difficult words
            3. Pacing instructions
            4. Segment breaks for processing
            5. Audio cue markers for music/effects
            """,
            inputs=[
                Input("podcast_script"),
                Input("voice_settings")
            ],
           
        )
        
        # Step 2: Create Audio Segments Plan
        .llm_step(
            task="""
            Create audio production plan: {prepare_tts_script}
            
            Background music: {background_music}
            
            Plan includes:
            1. Intro music (10-15 seconds)
            2. Main content segments with transitions
            3. Background music levels and fade points
            4. Outro music (10-15 seconds)
            5. Chapter transition effects
            6. Overall mixing guidelines
            """,
            inputs=[
                StepOutput("prepare_tts_script"),
                Input("background_music")
            ],
            
        )
        
        .final_output(
            output_schema=PodcastPackage,
            summarize=True
        )
        .build()
    )
