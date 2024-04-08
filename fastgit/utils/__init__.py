import subprocess
import os

# Get the current directory name
current_directory = os.getcwd()
directory_name = os.path.basename(current_directory)
def get_username():
    _result = subprocess.run(["gh", "auth", "status"], check=True, cwd=current_directory, capture_output=True,
                             text=True)
    first_index = _result.stdout.find("account") + len("account") + 1
    last_index = _result.stdout.find("(") - 1
    return _result.stdout[first_index:last_index]

def r_process(_command, check=True, cwd=current_directory, capture_output=True, text=True):
    return subprocess.run(_command, check=check, cwd=cwd, capture_output=capture_output, text=text)