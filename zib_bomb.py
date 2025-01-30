import shutil
import os


def compress_file(file_path):
    # Get the directory and the file name
    directory = os.path.dirname(file_path)
    base_name = os.path.splitext(file_path)[0]  # Remove the file extension for archive name

    # Create a tar archive
    shutil.make_archive(base_name, 'tar', directory, os.path.basename(file_path))

    # Create a zip archive
    shutil.make_archive(base_name, 'zip', directory, os.path.basename(file_path))


if __name__ == "__main__":
    cwd = os.getcwd()
    file_name = os.path.join(cwd,"file.txt")

    # Optionally, create a larger file to compress
    with open(file_name, 'w') as f:
        for i in range(1000000):  # 1 million iterations for a larger file
            f.write("A" * 1000)  # 1000 'A's per iteration, highly compressible

    # Compress the file
    compress_file(file_name)
