import os
import json
from pathlib import Path
from pydantic import BaseModel, Field
from portia.tool import Tool, ToolRunContext
import requests
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
load_dotenv()

# --- Folder Creator Tool (unchanged) ---

class MakeDirectoryToolSchema(BaseModel):
    path: str = Field(..., description="The directory path to create.")

class MakeDirectoryTool(Tool[str]):
    id: str = "make_directory_tool"
    name: str = "Make Directory Tool"
    description: str = "Creates a directory at the specified path if it doesn't exist."
    args_schema: type[BaseModel] = MakeDirectoryToolSchema
    output_schema: tuple[str, str] = ("str", "A message confirming the directory creation.")

    def run(self, _: ToolRunContext, path: str) -> str:
        Path(path).mkdir(parents=True, exist_ok=True)
        return f"Directory '{path}' is ready."


# --- File Creator Tool (writes JSON if filename ends with .json) ---

class MakeFileInFolderToolSchema(BaseModel):
    folder_path: str = Field(..., description="The folder in which to create the file.")
    filename: str = Field(..., description="The name of the file to create.")
    content: object = Field(..., description="The content to write into the file. If the filename ends with .json, content will be saved as JSON.")

class MakeFileInFolderTool(Tool[str]):
    id: str = "make_file_in_folder_tool"
    name: str = "Make File In Folder Tool"
    description: str = "Creates a file with the given filename and content in the specified folder. If the filename ends with .json, content will be saved as JSON."
    args_schema: type[BaseModel] = MakeFileInFolderToolSchema
    output_schema: tuple[str, str] = ("str", "A message confirming the file creation.")

    def run(self, _: ToolRunContext, folder_path: str, filename: str, content) -> str:
        folder = Path(folder_path)
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / filename
        if filename.lower().endswith('.json'):
            with file_path.open('w', encoding='utf-8') as f:
                json.dump(content, f, ensure_ascii=False, indent=2)
        else:
            file_path.write_text(str(content), encoding="utf-8")
        return f"File '{file_path}' created with provided content."
    


from elevenlabs.client import ElevenLabs

load_dotenv()

class ElevenLabsTTSSchema(BaseModel):
    text: str = Field(..., description="Text to synthesize")
    voice_id: str = Field(..., description="Voice ID for synthesis")
    model_id: str = Field("eleven_multilingual_v2", description="Model ID for TTS")
    output_format: str = Field("mp3_44100_128", description="Audio output format")
    output_path: str = Field("output.mp3", description="Where to save the audio file")

class ElevenLabsTTSTool(Tool[str]):
    id: str = "elevenlabs_tts_tool"
    name: str = "ElevenLabs TTS Tool"
    description: str = "Converts text to speech using the official ElevenLabs Python SDK"
    args_schema: type[BaseModel] = ElevenLabsTTSSchema
    output_schema: tuple[str, str] = ("str", "Path to the generated audio file")

    def run(self, _: ToolRunContext, text: str, voice_id: str, model_id: str, output_format: str, output_path: str) -> str:
        api_key = os.getenv("ELEVEN_LABS_API_KEY")
        elevenlabs = ElevenLabs(api_key=api_key)
        audio = elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            model_id=model_id,
            output_format=output_format,
        )
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_bytes(b"".join(audio))
        return str(Path(output_path).absolute())