import os
def write_file(working_directory,file_path,content):
    try:
        working_absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_absolute_path, file_path))
        is_valid_target_file = os.path.commonpath([working_absolute_path, target_file]) == working_absolute_path
        if not is_valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'''Error: Cannot write to "{file_path}" as it is a directory'
                            working: {working_directory}
                            working_abs: {working_absolute_path}
                            target file: {file_path}
                            '''
        os.makedirs(working_absolute_path,exist_ok=True)
        with open(target_file,'w') as file:
            file.write(content)
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"