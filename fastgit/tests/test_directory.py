import unittest
from unittest.mock import patch

def verify_directory_name(_directory_name):
    if " " in _directory_name:
        print("Invalid directory name.")
        print("Directory name should not contain any spaces.")
        print("Trying to fix it...")
        _directory_name = _directory_name.replace(" ", "-")
        print(f"Directory name: {_directory_name}")
        return _directory_name
    return _directory_name

def get_username():
    return "testuser"

class TestVerifyDirectoryName(unittest.TestCase):

    @patch("builtins.input", return_value="test-directory")
    def test_valid_directory_name(self, mock_input):
        directory_name = "my-directory"
        result = verify_directory_name(directory_name)
        self.assertEqual(result, directory_name)

    @patch("builtins.input", return_value="test directory")
    def test_directory_name_with_spaces(self, mock_input):
        directory_name = "directory with spaces"
        result = verify_directory_name(directory_name)
        self.assertEqual(result, "directory-with-spaces")

    @patch("builtins.input", return_value="testuser")
    def test_repo_url_creation(self, mock_input):
        directory_name = "test-directory"
        repo_url = (f"https://github.com/{get_username()}/"
                    f"{verify_directory_name(directory_name)}.git")
        print(repo_url)
        self.assertEqual(repo_url, "https://github.com/testuser/test-directory.git")

if __name__ == "__main__":
    unittest.main()
