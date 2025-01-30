import os
import shutil
import subprocess
import psutil
import time


def force_delete(path):
    # Check if the path is a file
    if os.path.isfile(path):
        try:
            os.remove(path)
            print(f"File '{path}' deleted successfully.")
        except PermissionError:
            print(f"File '{path}' is in use. Attempting to force delete...")
            force_delete_with_psutil(path)
        except Exception as e:
            print(f"Failed to delete file '{path}': {e}")

    # Check if the path is a directory
    elif os.path.isdir(path):
        try:
            shutil.rmtree(path)
            print(f"Directory '{path}' deleted successfully.")
        except PermissionError:
            print(f"Directory '{path}' is in use. Attempting to force delete...")
            force_delete_with_psutil(path)
        except Exception as e:
            print(f"Failed to delete directory '{path}': {e}")

    else:
        print(f"The path '{path}' does not exist.")


def force_delete_with_psutil(path):
    # Attempt to find processes that are using the file or directory
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            # Check if the process has any open files
            for item in proc.open_files():
                if path in item.path:
                    print(f"Terminating process '{proc.name()}' (PID: {proc.pid}) using '{item.path}'...")
                    proc.terminate()  # Or proc.kill() for forceful termination
                    proc.wait()  # Wait for the process to terminate
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Wait a moment for processes to close
    time.sleep(2)

    # Try deleting again
    if os.path.isfile(path):
        try:
            os.remove(path)
            print(f"File '{path}' force deleted.")
        except Exception as e:
            print(f"Error while force deleting '{path}': {e}")
    elif os.path.isdir(path):
        try:
            shutil.rmtree(path)
            print(f"Directory '{path}' force deleted.")
        except Exception as e:
            print(f"Error while force deleting directory '{path}': {e}")


# Example usage
path_to_delete = r"C:\Users\amrmu\Downloads\Programs"  # Change this to your file or directory path
force_delete(path_to_delete)

