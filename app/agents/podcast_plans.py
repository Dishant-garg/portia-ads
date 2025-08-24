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
                "search_query": f"{Input('episode_topic')} podcast interviews expert insights recent developments 2024"
            }
        )
        
        # Step 2: Find Related Podcasts for Reference
        .invoke_tool_step(
            step_name="analyze_similar_podcasts",
            tool="search_tool",
            args={
                "search_query": f"popular podcasts about {Input('episode_topic')} high engagement format structure"
            }
        )
        
        # Step 3: Create Podcast Script Structure
        .llm_step(
            step_name="create_podcast_script",
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
            ]
        )
        
        # Step 4: Generate Show Notes
        .llm_step(
            step_name="generate_show_notes",
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
            ]
        )
        
        # Step 5: Create Chapter Markers
        .llm_step(
            step_name="create_chapter_markers",
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
            ]
        )
        
        # Step 6: Generate Audio Production Instructions
        .llm_step(
            step_name="create_audio_instructions",
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
            ]
        )
        
        # Step 7: Package Episode Materials
        .function_step(
            step_name="package_episode_materials",
            function=lambda script, notes, chapters, audio, topic, episode, duration: {
                "episode_script": script,
                "show_notes": notes,
                "chapter_markers": chapters,
                "audio_instructions": audio,
                "episode_metadata": {
                    "title": f"Episode {episode}: {topic}",
                    "episode_number": episode,
                    "topic": topic,
                    "estimated_duration": f"{duration} minutes",
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
                "episode": Input("episode_number"),
                "duration": Input("target_duration")
            }
        )

        # Step 8: Ensure podcast_episodes folder exists
        .invoke_tool_step(
            step_name="create_podcast_folder",
            tool="make_directory_tool",
            args={
                "path": "podcast_episodes"
            }
        )

        # Step 9: Save Podcast Package
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

import re

def extract_spoken_content(text: str) -> str:
    # Try to extract content between <speak>...</speak> tags
    match = re.search(r"<speak>(.*?)</speak>", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Otherwise, try to extract lines that look like dialogue or narration
    lines = text.splitlines()
    spoken_lines = []
    for line in lines:
        # Heuristic: skip lines that are bullet points, section headers, or instructions
        if line.strip().startswith("*") or line.strip().startswith("**") or ":" in line:
            continue
        if line.strip():
            spoken_lines.append(line.strip())
    return "\n".join(spoken_lines)

def create_podcast_audio_production():
    """Audio production pipeline using text-to-speech."""
    return (
        PlanBuilderV2("Podcast Audio Production Pipeline")
        
        .input(name="podcast_script", description="Complete podcast script")
        .input(name="voice_id", description="ElevenLabs voice ID", default_value="JBFqnCBsd6RMkjVDRZzb")
        .input(name="model_id", description="Model ID for TTS", default_value="eleven_multilingual_v2")
        .input(name="output_format", description="Audio output format", default_value="mp3_44100_128")
        .input(name="output_path", description="Where to save the audio file", default_value="podcast_episodes/episode_audio.mp3")
        .input(name="background_music", description="Background music preferences", default_value="subtle_ambient")
        
        # Step 1: Prepare TTS Script
        .llm_step(
            step_name="prepare_tts_script",
            task="""
            Prepare the following podcast script for text-to-speech production. 
            Output ONLY the SSML or plain text that should be spoken, with no instructions or bullet points.
            If possible, wrap the output in <speak>...</speak> tags.

            Podcast script:
            {podcast_script}
            """,
            inputs=[
                Input("podcast_script")
            ]
        )
        
        # Step 2: Create Audio Segments Plan
        .llm_step(
            step_name="create_audio_segments_plan",
            task="""
            Given the TTS-ready script below, create an audio production plan for the editor.
            DO NOT repeat or reformat the script itself—just describe music, transitions, mixing, and effects.

            TTS Script:
            {prepare_tts_script}

            Plan includes:
            1. Intro music (10-15 seconds)
            2. Main content segments with transitions
            3. Background music levels and fade points
            4. Outro music (10-15 seconds)
            5. Chapter transition effects
            6. Overall mixing guidelines
            7. Keep it concise and clear and under 1000 words.
            """,
            inputs=[
                StepOutput("prepare_tts_script"),
                Input("background_music")
            ]
        )

        # Step 3: Extract only the spoken content (from the TTS script)
        .function_step(
            step_name="extract_spoken_content",
            function=extract_spoken_content,
            args={"audio_segments_plan": StepOutput("prepare_tts_script")}
        )

        # Step 4: Generate Podcast Audio (after segment plan, using only the clean script)
        .invoke_tool_step(
            step_name="generate_podcast_audio",
            tool="elevenlabs_tts_tool",
            args={
                "text": StepOutput("extract_spoken_content"),
                "voice_id": Input("voice_id"),
                "model_id": Input("model_id"),
                "output_format": Input("output_format"),
                "output_path": Input("output_path")
            }
        )
        
        .final_output(
            output_schema=PodcastPackage,
            summarize=True
        )
        .build()
    )