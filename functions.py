import os
import subprocess

from config import MAX_CHARS


def get_files_info(working_directory, directory="."):
    header = (
        f"Result for {'current' if directory == '.' else f"'{directory}'"} directory"
    )
    try:
        working_directory = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(working_directory, directory))
        if (
            os.path.commonpath([working_directory, target_directory])
            != working_directory
        ):
            return f'{header}\n    Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_directory):
            return f'{header}\n    Error: "{target_directory}" is not a directory'

        output = [header]

        for file in os.scandir(target_directory):
            output.append(
                f"  - {file.name}: file_size={os.path.getsize(file)} bytes, is_dir={file.is_dir()}"
            )

        return "\n".join(output)
    except OSError as e:
        return f"{header}\n    Error: {e}"


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


def run_python_file(working_directory, file_path, args=None):
    try:
        working_directory = os.path.abspath(working_directory)
        full_file_path = os.path.normpath(os.path.join(working_directory, file_path))

        if os.path.commonpath([working_directory, full_file_path]) != working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(full_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not full_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", full_file_path]
        if args is not None:
            command.extend(args)

        process = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []
        if process.returncode != 0:
            output.append(f"Process exited with code {process.returncode}")

        if len(process.stdout) == 0 and len(process.stderr) == 0:
            output.append("No output produced")
        else:
            output.append("STDOUT:")
            output.append(process.stdout)
            output.append("STDERR:")
            output.append(process.stderr)

        return "\n".join(output)
    except (OSError, subprocess.SubprocessError) as e:
        return f"Error: executing Python file: {e}"


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
