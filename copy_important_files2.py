import os
import shutil
from tqdm import tqdm
from pathlib import Path
import logging
from datetime import datetime
import concurrent.futures
from typing import List, Set, Tuple


# Configuration
ACCEPTED_FILES_EXTENSIONS = {"txt", "pdf", "docx", "xlsx", "md", "epub", "pptx", "doc", "jpg", "png", "jpeg"}
REFUSED_DIRS = {
        "Archives", "FileHistory", "Kab", "Listen",
        "Projects", "Softwares", "Websites"
    }
ONLY_ALLOWED_DIRS = {"Learnings"}
SRC_DIR = "E:/"

class FileCopier:
    def __init__(
            self,
            source_partition: str,
            destination_base: str,
            accepted_extensions: Set[str],
            refused_dirs: Set[str],
            max_workers: int = 4
    ):
        self.source_partition = Path(source_partition)
        self.destination_base = Path(destination_base) / f"Partition_{self.source_partition.drive[0]}"
        self.accepted_extensions = {ext.lower() for ext in accepted_extensions}
        self.refused_dirs = refused_dirs
        self.max_workers = max_workers
        self.copied_files = 0
        self.failed_operations: List[Tuple[str, str]] = []

        # Setup logging
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging with timestamp and proper formatting."""
        log_dir = self.destination_base / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"copy_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
                logging.StreamHandler()
            ]
        )

    def is_valid_dir(self, path: Path) -> bool:
        """
        Check if the directory is valid for processing.
        Returns False for hidden, system, and refused directories.
        """
        try:
            return (path.is_dir()
                    and not path.is_symlink()
                    and not path.name.startswith((".", "$"))
                    and "node_modules" not in path.parts
                    and "test" not in path.parts
                    and "See" not in path.parts
                    and path.name != "System Volume Information"
                    and path.name not in self.refused_dirs
                    and any(path.iterdir())  # Check if the directory is not empty
                    )
        except (PermissionError, OSError):
            logging.warning(f"Permission denied or error accessing directory: {path}")
            return False

    def copy_file(self, src_file: Path, relative_path: Path) -> bool:
        """Copy a single file maintaining directory structure."""
        try:
            dest_file = self.destination_base / relative_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)

            # Only copy if a source is newer or the destination doesn't exist
            if not dest_file.exists() or src_file.stat().st_mtime > dest_file.stat().st_mtime:
                shutil.copy2(src_file, dest_file)
                self.copied_files += 1
                return True
            return False

        except Exception as e:
            self.failed_operations.append((str(src_file), str(e)))
            logging.error(f"Failed to copy {src_file}: {e}")
            return False

    def process_directory(self, dir_path: Path) -> None:
        """Process all files in a directory."""
        try:
            for root, dirs, files in os.walk(dir_path):
                root_path = Path(root)

                # Filter directories
                dirs[:] = [d for d in dirs if self.is_valid_dir(root_path / d)]

                # Process files with a progress bar
                valid_files = [
                    f for f in files
                    if Path(f).suffix.lower()[1:] in self.accepted_extensions
                       and not f.startswith(("$", "."))
                ]

                with tqdm(total=len(valid_files), desc=f"Copying {root_path.name}", leave=False) as pbar:
                    for file in valid_files:
                        src_file = root_path / file
                        relative_path = src_file.relative_to(self.source_partition)
                        if self.copy_file(src_file, relative_path):
                            pbar.update(1)

        except Exception as e:
            logging.error(f"Error processing directory {dir_path}: {e}")

    def run(self) -> None:
        """Execute the file copying process."""
        logging.info(f"Starting copy process from {self.source_partition} to {self.destination_base}")

        # Create a destination directory if it doesn't exist
        self.destination_base.mkdir(parents=True, exist_ok=True)

        # Get valid top-level directories
        valid_dirs = [
            d for d in self.source_partition.iterdir()
            if self.is_valid_dir(d)
        ]

        # Process directories in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            list(tqdm(
                executor.map(self.process_directory, valid_dirs),
                total=len(valid_dirs),
                desc="Processing directories",
                unit="dir"
            ))

        # Log results
        logging.info(f"Copy process completed. Copied {self.copied_files} files.")
        if self.failed_operations:
            logging.error("Failed operations:")
            for src, error in self.failed_operations:
                logging.error(f"File: {src}, Error: {error}")

def main():
    # Initialize and run copier
    copier = FileCopier(
        source_partition=SRC_DIR,
        destination_base="F:/COPIED",
        accepted_extensions=ACCEPTED_FILES_EXTENSIONS,
        refused_dirs=REFUSED_DIRS
    )
    copier.run()


if __name__ == "__main__":
    main()