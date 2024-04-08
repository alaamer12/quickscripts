import shutil
import os
import subprocess
PATH = "F:\Projects\Python"
COMMIT_MESSAGE = "update\n"

def _get_paths():
    return [os.path.join(PATH, path) for path in os.listdir(PATH) if
            os.path.isdir(os.path.join(PATH, path))]


def copy(source, destination):
    shutil.copy(source, destination)

if __name__ == "__main__":
    for i, path in enumerate(_get_paths()):
        print(f"({i + 1}) {path}")
        process = subprocess.Popen(["python", "x.py"], cwd=path, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Send 'y' as input
        process.stdin.write(COMMIT_MESSAGE)
        process.stdin.flush()

        print("[OK]")
        # Get the output
        output, _ = process.communicate()
        if output:
            pass


