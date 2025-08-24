from portia import InMemoryToolRegistry
from app.custom_tools.file_creator import MakeDirectoryTool, MakeFileInFolderTool, ElevenLabsTTSTool

custom_tool_registry = InMemoryToolRegistry.from_local_tools(
    [MakeDirectoryTool(), MakeFileInFolderTool(), ElevenLabsTTSTool()],
)