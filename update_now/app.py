import shutil
import os
import subprocess
from tqdm import tqdm
import contextlib

PATH = "F:\Projects\Python"
COMMIT_MESSAGE = "update\n"


def _get_paths():
    return [os.path.join(PATH, path) for path in os.listdir(PATH) if
            os.path.isdir(os.path.join(PATH, path))]


def copy(source, destination):
    shutil.copy(source, destination)


def cleanup(path: str):
    if os.path.exists(path):
        os.remove(path)


if __name__ == "__main__":
    for i, path in tqdm(enumerate(_get_paths()), total=len(_get_paths()), desc="Updating", unit="files"):
        if not os.path.exists(os.path.join(path, "x.py")):
            copy("x.py", path)

        print(f"Updating {path}...")
        print(f"({i + 1}) {path}")
        with contextlib.suppress(Exception):
            process = subprocess.Popen(["python", "x.py"], cwd=path, shell=True, stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Send 'y' as input
            process.stdin.write(COMMIT_MESSAGE)
            process.stdin.flush()

            print("[OK]")
            # Get the output
            output, _ = process.communicate()
            if output:
                pass

            print(f"\nCleaning up {path}...")
            cleanup(os.path.join(path, "x.py"))
