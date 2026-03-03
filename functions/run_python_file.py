import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute Python files with optional arguments. returns a string of stdout/stderr.  ",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to python file, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Arguments for running the python file command, will be used for functions arguments."
            )
        },
    ),
)

def run_python_file(working_directory,file_path,args=None):
    try:
        working_absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_absolute_path, file_path))
        is_valid_target_file = os.path.commonpath([working_absolute_path, target_file]) == working_absolute_path
        if not is_valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'''Error: "{file_path}" does not exist or is not a regular file
                    working: {working_directory}
                    working_abs: {working_absolute_path}
                    target file: {file_path}
                    '''
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python",target_file]
        if args:
            command.extend(args)

        completed_process = subprocess.run(command,text=True,capture_output=True,timeout=30.0)
        string_process = ""
        if completed_process.returncode != 0:
            string_process += f"\n Process exited with code {completed_process.returncode}"
        if not completed_process.stdout and not completed_process.stderr:
            string_process += "\n No output produced"
        else:
            if completed_process.stdout:
                string_process += f"\n STDOUT: {completed_process.stdout}"
            if completed_process.stderr:
                string_process += f"\n STDERR: {completed_process.stderr}"
        return string_process
    except Exception as e:
        return f"Error: executing Python file: {e}"