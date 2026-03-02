import os
from config import MAX_CHARS
def get_file_content(working_directory,file_path):

    try:
        working_absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_absolute_path, file_path))
        is_valid_target_file = os.path.commonpath([working_absolute_path, target_file]) == working_absolute_path
        if not is_valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'''Error: "{file_path}" is not a file
                    working: {working_directory}
                    working_abs: {working_absolute_path}
                    target file: {file_path}
                    '''
        with open(target_file,'r') as file:
            file_content_string = file.read(MAX_CHARS)
            if file.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
