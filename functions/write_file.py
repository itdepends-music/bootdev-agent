import os

from google.genai import types


def write_file(working_directory, file_path, content):
    try:
        working_directory = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory, full_file_path]) != working_directory:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(full_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        file_handle = open(full_file_path, mode="w")
        print(content, file=file_handle)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except OSError as e:
        return f"Error: {e}"


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write contents to a file at the given filepath. Filepath is relative to the working directory. Prior contents of the file are overwritten",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Contents to write to file. Prior contents will be overwritten",
            ),
        },
    ),
)
