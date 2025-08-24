import json
from app.agents.podcast_plans import create_podcast_audio_production
from app.core.portia_client import PortiaClient

def test_podcast_audio_production_from_package():
    # Load the pregenerated episode package
    with open("podcast_episodes/episode_001_package.json") as f:
        episode_package = json.load(f)

    # Use the episode_script from the package as the podcast_script input
    podcast_script = episode_package["episode_script"]

    plan = create_podcast_audio_production()
    plan_run_inputs = {
        "podcast_script": podcast_script,
        "voice_id": "JBFqnCBsd6RMkjVDRZzb",
        "model_id": "eleven_multilingual_v2",
        "output_format": "mp3_44100_128",
        "output_path": "podcast_episodes/episode_001_audio.mp3",
        "background_music": "subtle_ambient"
    }
    client = PortiaClient()
    result = client.run_plan2(plan, plan_run_inputs)
    print("Podcast audio production result:")
    print(result)
    assert result is not None

if __name__ == "__main__":
    test_podcast_audio_production_from_package()