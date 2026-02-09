import os
import subprocess


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
