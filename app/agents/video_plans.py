import json
from portia import PlanBuilderV2, StepOutput, Input
from ..schema.content_schemas import VideoPackage

def parse_bullet_list(text):
    """Parse a markdown bullet list into a list of strings."""
    return [line.strip("* ").strip() for line in text.splitlines() if line.strip().startswith("*")]

def parse_thumbnail_concepts(text):
    """Split thumbnail concepts by double newlines or numbers."""
    return [item.strip() for item in text.split("\n\n") if item.strip()]

def parse_json(text):
    """Parse a JSON string, or return an empty dict if parsing fails."""
    try:
        return json.loads(text)
    except Exception:
        return {}

def create_video_production_system():
    """Complete video production pipeline."""
    return (
        PlanBuilderV2("Video Production Pipeline")

        # Inputs
        .input(
            name="video_topic",
            description="Main topic of the video"
        )
        .input(
            name="video_style",
            description="Vibe/tone of the video (e.g., 'educational', 'entertaining', 'professional')"
        )
        .input(
            name="brand_guidelines",
            description="Target audience or brand guidelines for the video"
        )
        .input(
            name="target_platform",
            description="Platform to generate the video for (e.g., 'youtube', 'instagram', 'tiktok')"
        )

        # Step 1: Create Video Script
        .llm_step(
            step_name="create_video_script",
            task="Write a detailed video script for the topic '{video_topic}' with a '{video_style}' vibe for the '{brand_guidelines}' audience, tailored for '{target_platform}'.",
            inputs=[
                Input("video_topic"),
                Input("video_style"),
                Input("brand_guidelines"),
                Input("target_platform")
            ]
        )

        # Step 2: Create Shot List
        .llm_step(
            step_name="create_shot_list",
            task="Generate a shot list for the video script as a markdown bullet list.",
            inputs=[StepOutput("create_video_script")]
        )

        # Step 2b: Parse Shot List
        .function_step(
            function=parse_bullet_list,
            args={"text": StepOutput("create_shot_list")},
            
        )

        # Step 3: Generate Thumbnail Concepts
        .llm_step(
            step_name="generate_thumbnail_concepts",
            task="Suggest three thumbnail concepts for the video, each separated by two newlines.",
            inputs=[StepOutput("create_video_script")]
        )

        # Step 3b: Parse Thumbnail Concepts
        .function_step(
            function=parse_thumbnail_concepts,
            args={"text": StepOutput("generate_thumbnail_concepts")},
            
        )

        # Step 4: Create Video Metadata (as JSON)
        .llm_step(
            step_name="create_video_metadata",
            task="""
            Generate video metadata for the video as a valid JSON object with the following keys:
            - title (string)
            - description (string)
            - tags (list of strings)
            Respond ONLY with valid JSON.
            """,
            inputs=[StepOutput("create_video_script"), Input("video_topic"), Input("target_platform")]
        )

        # Step 4b: Parse Video Metadata
        .function_step(
            function=parse_json,
            args={"text": StepOutput("create_video_metadata")},
           
        )

        # Step 5: Create Editing Instructions
        .llm_step(
            step_name="create_editing_instructions",
            task="Write editing instructions for the video editor based on the script and shot list.",
            inputs=[StepOutput("create_video_script"), StepOutput("parse_shot_list")]
        )

        # Step 6: Generate Video (using video_generation_tool)
        .invoke_tool_step(
            step_name="generate_video",
            tool="portia:mcp:mcp.invideo.io:generate_video_from_script",
            args={
                "script": StepOutput("create_video_script"),
                "topic": Input("video_topic"),
                "vibe": Input("video_style"),
                "targetAudience": Input("brand_guidelines"),
                "platform": Input("target_platform")
            }
        )

        # Step 7: Package Video Production Materials
        .function_step(
            function=lambda script, shots, thumbs, metadata, editing, topic, platform, video_url: {
                "video_script": script,
                "shot_list": shots,
                "thumbnail_concepts": thumbs,
                "video_metadata": metadata,
                "editing_instructions": editing,
                "video_url": video_url,
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
                "shots": StepOutput("parse_shot_list"),
                "thumbs": StepOutput("parse_thumbnail_concepts"),
                "metadata": StepOutput("parse_video_metadata"),
                "editing": StepOutput("create_editing_instructions"),
                "topic": Input("video_topic"),
                "platform": Input("target_platform"),
                "video_url": StepOutput("generate_video")
            },
            
        )

        .final_output(
            output_schema=VideoPackage,
            summarize=True
        )
        .build()
    )
        