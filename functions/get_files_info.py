import os
import traceback
from google.genai import types
def get_files_info(working_directory, directory="."):
    try:
        working_absolute_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_absolute_path,directory))

        is_valid_target_dir = os.path.commonpath([working_absolute_path, target_dir]) == working_absolute_path
        if not is_valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'''Error: "{directory}" is not a directory
                    working: {working_directory}
                    working_abs: {working_absolute_path}
                    target dir: {target_dir}
                    '''

        directory_list = os.listdir(target_dir)
        details_files_list = map(
            lambda item:  f"- {item}: file_size={os.path.getsize(f"{target_dir}/{item}")}, is_dir={os.path.isdir(f"{target_dir}/{item}")} ",directory_list
        )
        details_files_string = '\n'.join(details_files_list)
        return details_files_string
    except Exception as e:
        tb = traceback.format_exc()
        return f'''Error: {e}
        directory : {directory}
        working: {working_directory}
        working_abs: {working_absolute_path}
        target dir: {target_dir}
        directory list: {directory_list}
        {tb}
'''
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


