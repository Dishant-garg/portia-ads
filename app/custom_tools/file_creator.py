from pathlib import Path
from pydantic import BaseModel, Field
from portia.tool import Tool, ToolRunContext

# --- Folder Creator Tool ---

class MakeDirectoryToolSchema(BaseModel):
    """Schema defining the inputs for the MakeDirectoryTool."""
    path: str = Field(..., description="The directory path to create.")

class MakeDirectoryTool(Tool[str]):
    """Creates a directory if it doesn't exist."""
    id: str = "make_directory_tool"
    name: str = "Make Directory Tool"
    description: str = "Creates a directory at the specified path if it doesn't exist."
    args_schema: type[BaseModel] = MakeDirectoryToolSchema
    output_schema: tuple[str, str] = ("str", "A message confirming the directory creation.")

    def run(self, _: ToolRunContext, path: str) -> str:
        Path(path).mkdir(parents=True, exist_ok=True)
        return f"Directory '{path}' is ready."


# --- File Creator Tool ---

class MakeFileInFolderToolSchema(BaseModel):
    """Schema defining the inputs for the MakeFileInFolderTool."""
    folder_path: str = Field(..., description="The folder in which to create the file.")
    filename: str = Field(..., description="The name of the file to create.")
    content: str = Field("", description="The content to write into the file.")

class MakeFileInFolderTool(Tool[str]):
    """Creates a file with the given filename and content in the specified folder."""
    id: str = "make_file_in_folder_tool"
    name: str = "Make File In Folder Tool"
    description: str = "Creates a file with the given filename and content in the specified folder."
    args_schema: type[BaseModel] = MakeFileInFolderToolSchema
    output_schema: tuple[str, str] = ("str", "A message confirming the file creation.")

    def run(self, _: ToolRunContext, folder_path: str, filename: str, content: str = "") -> str:
        folder = Path(folder_path)
        folder.mkdir(parents=True, exist_ok=True)
        file_path = folder / filename
        file_path.write_text(content)
        return f"File '{file_path}' created with provided content."