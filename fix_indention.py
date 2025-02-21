def fix_indentation(file_path, current_indent='  ', new_indent='    '):
    """Fix indentation in a Python file."""
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()

        # Replace current indentation with new indentation
        fixed_content = [
            line.replace(current_indent, new_indent) for line in content
        ]

        with open(file_path, 'w') as file:
            file.writelines(fixed_content)

        print(f"Indentation in '{file_path}' has been changed from '{current_indent}' to '{new_indent}'.")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file_path = 'your_script.py'  # Replace with your file path
fix_indentation(file_path, current_indent='  ', new_indent='    ')  # Change 2 spaces to 4 spaces
