import os
import subprocess
import schedule

class GitHubRepoManager:
    GITIGNORE = """
    # Operating System Files
    .DS_Store
    Thumbs.db
    desktop.ini

    # IDE/Editor Files
    .idea/
    .vscode/
    *.suo
    *.ntvs*
    *.njsproj
    *.sln
    *.swp
    *~

    # Build Output
    node_modules/
    dist/
    build/
    *.o
    *.obj
    *.class

    # Dependency Directories
    vendor/
    jspm_packages/
    typings/
    *.jar
    *.war

    # Logs and Temporary Files
    *.log
    *.tmp
    *.temp

    # System Files
    *.dll
    *.exe
    *.pdb
    *.lib
    *.so
    *.dylib

    # Configuration Files
    .env
    .DS_Store
    .project
    .classpath
    .settings/

    # IDE/Editor Specific
    .idea/
    .vscode/
    *.sublime-project
    *.sublime-workspace
    *.idea/

    # Miscellaneous
    .dockerignore
    .npmignore
    .babelrc
    .eslintrc
    .gitattributes

    # Custom Logs or Data Files
    # Add any other file or directory specific to your project
    """

    def __init__(self):
        self.current_directory = os.getcwd()
        self.directory_name = os.path.basename(self.current_directory)
        self.username = self.get_username()
        self.repo_url = f"https://github.com/{self.username}/{self.verify_directory_name(self.directory_name)}.git"

    def get_username(self):
        _result = subprocess.run(["gh", "auth", "status"], check=True, cwd=self.current_directory, capture_output=True,
                                 text=True)
        first_index = _result.stdout.find("account") + len("account") + 1
        last_index = _result.stdout.find("(") - 1
        return _result.stdout[first_index:last_index]

    def verify_directory_name(self, directory_name):
        if " " in directory_name:
            print("Invalid directory name.")
            print("Directory name should not contain any spaces.")
            print("Trying to fix it...")
            directory_name = directory_name.replace(" ", "-")
            print(f"Directory name: {directory_name}")
        return directory_name

    def check_logged_in(self):
        try:
            _result = subprocess.run(["gh", "auth", "status"], check=True, cwd=self.current_directory,
                                     capture_output=True, text=True)
            if not _result.stdout.find("Logged in to github.com account"):
                print("You are not logged in to GitHub.")
                print("Please log in and try again.")
                exit()
        except subprocess.CalledProcessError:
            pass

    def init_git_repo(self):
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], cwd=self.current_directory)

    def create_gitignore(self):
        if not os.path.exists("../.gitignore"):
            with open("../.gitignore", "w") as f:
                f.write(self.GITIGNORE)

    def create_github_repo(self):
        try:
            subprocess.run(["gh", "repo", "create", self.directory_name, "--public"], cwd=self.current_directory)
        except subprocess.CalledProcessError as e:
            print(f"Failed to create repo on GitHub: {e}")
            # pass

    def commit_and_push(self, message):
        try:
            subprocess.run(["git", "add", "."], cwd=self.current_directory)
            subprocess.run(["git", "commit", "-m", message], cwd=self.current_directory)
            subprocess.run(["git", "branch", "-M", "main"], cwd=self.current_directory)
            subprocess.run(["git", "remote", "add", "origin", self.repo_url], cwd=self.current_directory)
            subprocess.run(["git", "push", "-u", "origin", "main"], cwd=self.current_directory)
        except subprocess.CalledProcessError as e:
            print(f"Failed to commit and push: {e}")

    def main(self):
        print("Committing and pushing...")
        message = input("Enter commit message: {or go with the default message} :")
        if message.strip() == "":
            message = "Initial commit"
        self.check_logged_in()
        self.init_git_repo()
        self.create_gitignore()
        self.create_github_repo()
        self.commit_and_push(message)
        print("[OK]")
        exit()


if __name__ == "__main__":
    GitHubRepoManager().main()
