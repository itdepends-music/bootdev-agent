import os


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
