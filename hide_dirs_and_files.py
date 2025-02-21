import os
import ctypes



# Specify the directory name
dir_name = 'F/test/hidden_dir2'
file_name = 'hidden_file.txt'

# Create the directory
os.makedirs(dir_name, exist_ok=True)

# Create a hidden file in the directory
with open(os.path.join(dir_name, file_name), 'w') as f:
    f.write("This is a hidden file.")

# Set the directory to be hidden and a system folder
def hide_directory(dir_path):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    FILE_ATTRIBUTE_SYSTEM = 0x04
    ctypes.windll.kernel32.SetFileAttributesW(dir_path, FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM)

# Hide the directory
hide_directory(dir_name)

# Hide the file
def hide_file(file_path):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    ctypes.windll.kernel32.SetFileAttributesW(file_path, FILE_ATTRIBUTE_HIDDEN)

def hide_and_protect_file(file_path):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    FILE_ATTRIBUTE_READONLY = 0x01

    # Set the attributes to hidden and read-only
    ctypes.windll.kernel32.SetFileAttributesW(
        file_path, FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_READONLY
    )

def hide_and_protect_directory(dir_path):
    FILE_ATTRIBUTE_HIDDEN = 0x02
    FILE_ATTRIBUTE_SYSTEM = 0x04
    FILE_ATTRIBUTE_READONLY = 0x01

    # Set the attributes to hidden, system, and read-only
    ctypes.windll.kernel32.SetFileAttributesW(
        dir_path, FILE_ATTRIBUTE_HIDDEN | FILE_ATTRIBUTE_SYSTEM | FILE_ATTRIBUTE_READONLY
    )

# Hide the file in the hidden directory
hide_file(os.path.join(dir_name, file_name))

# Check if the directory and file exist
print(os.path.isdir(dir_name))  # True
print(os.path.isfile(os.path.join(dir_name, file_name)))  # True