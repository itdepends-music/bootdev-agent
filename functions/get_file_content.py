import os

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
