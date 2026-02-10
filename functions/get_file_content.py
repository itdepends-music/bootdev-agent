import os

from google.genai import types

MAX_CHARS = 10_000


def get_file_content(working_directory, file_path):
    try:
        working_directory = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory, full_file_path]) != working_directory:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(full_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        with open(full_file_path) as file_handle:
            content = file_handle.read(MAX_CHARS)
            if file_handle.read(1):
                content += (
                    f'\n\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return content
    except OSError as e:
        return f"error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Cat the contents of a file with a specified file path relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to read from, relative to the working directory",
            ),
        },
    ),
)
