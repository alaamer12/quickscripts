import subprocess
import os
from fastgit.constants import GITIGNORE

PATH = "F:\Projects\Python"


class UpdateNow:

    def __init__(self, path):
        self.path = path
        self.gitignore = GITIGNORE

    @staticmethod
    def get_username():
        _result = subprocess.run(["gh", "auth", "status"], check=True, capture_output=True,
                                 text=True)
        first_index = _result.stdout.find("account") + len("account") + 1
        last_index = _result.stdout.find("(") - 1
        return _result.stdout[first_index:last_index]

    def verify_directory_name(self):
        valid_dirs = []
        for _directory_name in os.listdir(self.path):
            if " " in _directory_name:
                print("Invalid directory name.")
                print("Directory name should not contain any spaces.")
                print("Trying to fix it...")
                _directory_name = _directory_name.replace(" ", "_")
                print(f"Directory name: {_directory_name}")
                valid_dirs.append(_directory_name)
            valid_dirs.append(_directory_name)
        return valid_dirs

    # Get all subdirectories
    def _get_paths(self):
        return [os.path.join(self.path, path) for path in os.listdir(self.path) if
                os.path.isdir(os.path.join(self.path, path))]

    # Check if it has .git directory
    def _check_git(self):
        for path in self._get_paths():
            if os.path.join(path, ".git"):
                continue
            else:
                subprocess.run(["git", "init"], shell=True, cwd=os.path.join(path, ".git"))

    # Check if it has .gitignore file
    def _check_gitignore(self):
        for path in self._get_paths():
            if os.path.join(path, ".gitignore"):
                continue
            else:
                with open(os.path.join(path, ".gitignore"), "w") as f:
                    f.write(self.gitignore)


    def _create_repo(self):
        try:
            pass
            # subprocess.run(["gh", "repo", "create", verify_directory_name(), "--public"], cwd=current_directory)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create repo on GitHub: {e}")
            # pass
    def update(self):
        # First step check
        self._check_git()
        self._check_gitignore()

        # Second step create Github repo

        for path in self._get_paths():
            subprocess.run(["git", "add", "."], shell=True, cwd=path)
            subprocess.run(["git", "commit", "-m", "update"], shell=True, cwd=path)
            subprocess.run(["git", "push"], shell=True, cwd=path)

    repo_url = (f"https://github.com/{get_username()}/"
                f"{verify_directory_name()}.git")
