from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, TaskID
from typing import Optional
from datetime import datetime
import os
import json
import time
import psutil
import subprocess
from pathlib import Path
import threading
from queue import Queue
import sys
import traceback
import threading
from queue import Queue

# Initialize rich console
console = Console()

# Size calculation result queue
size_queue = Queue()

def format_size(size_bytes: int) -> str:
    """Format size in bytes to human readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} PB"

def check_git_ls_files(directory: str) -> bool:
    """Check if git ls-files command is available."""
    try:
        subprocess.run(
            ["git", "ls-files", "--version"],
            cwd=directory,
            capture_output=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

# Size related functions
def calculate_git_size(directory: str) -> None:
    """Calculate the size of files tracked by git."""
    try:
        total_size = _get_git_tracked_files_size(directory)
        if total_size == 0:
            # Fallback to calculating size of all files in directory
            total_size = _calculate_directory_size(directory)
        size_queue.put(total_size)
    except Exception as e:
        size_queue.put(None)
        console.print(f"[yellow]⚠[/yellow] Could not calculate directory size: {str(e)}")

def _get_git_tracked_files_size(directory: str) -> int:
    """Calculate total size of git tracked files."""
    total_size = 0
    has_ls_files = check_git_ls_files(directory)
    
    if has_ls_files:
        total_size = _calculate_size_from_ls_files(directory)
    else:
        console.print("[yellow]⚠ Warning: git ls-files not available, falling back to staged files only[/yellow]")
        total_size = _calculate_size_from_staged_files(directory)
    
    return total_size

def _calculate_size_from_ls_files(directory: str) -> int:
    """Calculate size using git ls-files command."""
    total_size = 0
    tracked_files = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=directory,
        capture_output=True,
        text=True,
        check=True
    ).stdout.split('\0')
    
    for file in tracked_files:
        if file:  # Skip empty strings
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def _calculate_size_from_staged_files(directory: str) -> int:
    """Calculate size using git staged files."""
    total_size = 0
    staged_files = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        cwd=directory,
        capture_output=True,
        text=True,
        check=True
    ).stdout.splitlines()
    
    for file in staged_files:
        if file:  # Skip empty strings
            file_path = os.path.join(directory, file)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size

def _calculate_directory_size(directory: str) -> int:
    """Calculate total size of all files in directory (excluding .git)."""
    total_size = 0
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            file_path = os.path.join(root, file)
            try:
                total_size += os.path.getsize(file_path)
            except OSError:
                continue
    return total_size

# Git operations related functions
def handle_git_init(enable_logging: bool) -> None:
    """Initialize git repository if needed."""
    console.print("[yellow]Repository not initialized. Initializing...[/yellow]")
    with console.status("[bold green]Initializing repository...[/bold green]", spinner="dots"):
        # Create logs directory before any logging operations
        if enable_logging:
            LOGS_DIR.mkdir(exist_ok=True)
        run_command(["git", "init"], current_directory, log=enable_logging)
    console.print("[green]✓[/green] Git repository initialized")

def handle_gitignore_creation(enable_logging: bool) -> None:
    """Create .gitignore file if it doesn't exist."""
    if not os.path.exists(".gitignore"):
        with console.status("[bold green]Creating .gitignore...[/bold green]", spinner="dots"):
            with open(".gitignore", "w") as f:
                f.write(GITIGNORE)
            if enable_logging:
                log_git_operation("create_gitignore", {"content": GITIGNORE})
        console.print("[green]✓[/green] Created .gitignore")

def check_for_changes(enable_logging: bool) -> bool:
    """Check if there are any changes to commit."""
    with console.status("[bold green]Checking for changes...[/bold green]", spinner="dots"):
        stdout, _ = run_command(["git", "status", "--porcelain"], current_directory, log=enable_logging)
    return bool(stdout.strip())

def handle_empty_directories() -> None:
    """Handle empty directories check and .gitkeep creation."""
    console.print("\n[yellow]Would you like to check for empty directories?[/yellow]")
    console.print("[blue]This will add .gitkeep files to empty directories so they can be tracked by git[/blue]")
    try:
        choice = input("\nCheck empty directories? (y/N): ").strip().lower()
        console.print()  # Add newline after input
        if choice == 'y':
            add_gitkeep_to_empty_dirs()
    except (EOFError, KeyboardInterrupt):
        console.print("\n[yellow]Skipping empty directory check[/yellow]")

def add_and_commit_changes(message: str, enable_logging: bool) -> None:
    """Add and commit changes to git."""
    with console.status("[bold green]Adding files...[/bold green]", spinner="dots"):
        run_command(["git", "add", "."], current_directory, log=enable_logging)
    console.print("[green]✓[/green] Files added")
    
    with console.status("[bold green]Committing changes...[/bold green]", spinner="dots"):
        run_command(["git", "commit", "-m", message], current_directory, log=enable_logging)
    console.print("[green]✓[/green] Changes committed")

def handle_large_repository_warning(total_size: int) -> bool:
    """Handle warning for large repositories and get user confirmation."""
    if total_size > 500 * 1024 * 1024:  # 500 MB
        console.print(Panel(
            "[yellow]⚠ WARNING: Repository size exceeds 500 MB[/yellow]\n"
            "[red]This may cause issues with GitHub's file size limits.[/red]\n"
            "[green]Consider using Git LFS for large files: https://git-lfs.github.com[/green]",
            title="Size Warning"
        ))
        
        try:
            choice = input("\nContinue with push? (y/N): ").strip().lower()
            console.print()  # Add newline after input
            return choice == 'y'
        except (EOFError, KeyboardInterrupt):
            console.print("\n[yellow]Push cancelled by user[/yellow]")
            return False
    return True

def calculate_bundle_size() -> int:
    """Calculate the size of the bundle to be pushed."""
    try:
        # Get the bundle size by dry-running pack-objects
        result = subprocess.run(
            ["git", "pack-objects", "--dry-run", "--stdout", "--all", "--delta-base-offset"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            input=subprocess.run(
                ["git", "rev-list", "--objects", "--all"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            ).stdout
        )
        
        # Parse the last line which contains the total size
        if result.stderr:
            stats = result.stderr.decode('utf-8', errors='replace').splitlines()[-1]
            if 'Total' in stats:
                # Extract size in bytes from format like "Total 1234 bytes"
                size_str = stats.split()[1]
                return int(size_str)
    except (subprocess.CalledProcessError, ValueError, IndexError):
        pass
    return 0

def get_network_usage() -> tuple[float, float]:
    """Get current network I/O counters."""
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent, net_io.bytes_recv

def format_speed(bytes_per_sec: float) -> str:
    """Format network speed in bytes/sec to human readable format."""
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.1f} B/s"
    elif bytes_per_sec < 1024 * 1024:
        return f"{bytes_per_sec / 1024:.1f} KB/s"
    else:
        return f"{bytes_per_sec / (1024 * 1024):.1f} MB/s"

def push_changes_with_progress(total_size: Optional[int], enable_logging: bool) -> None:
    """Push changes to GitHub with progress tracking."""
    try:
        process = subprocess.Popen(
            ["git", "push", "origin", "HEAD"],
            cwd=current_directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=False
        )
        
        # Get initial network counters
        initial_sent, initial_recv = get_network_usage()
        last_update_time = time.time()
        last_sent = initial_sent
        
        with console.status("[bold green]Pushing to GitHub...[/bold green]", spinner="dots") as status:
            while True:
                if process.poll() is not None:
                    break
                
                # Update network stats every second
                current_time = time.time()
                if current_time - last_update_time >= 1.0:
                    current_sent, _ = get_network_usage()
                    bytes_sent = current_sent - last_sent
                    upload_speed = bytes_sent / (current_time - last_update_time)
                    
                    status_msg = f"[bold green]Pushing to GitHub...[/bold green] Upload speed: {format_speed(upload_speed)}"
                    status.update(status_msg)
                    
                    last_update_time = current_time
                    last_sent = current_sent
                
                # Read and display git output
                try:
                    if process.stderr:
                        line = process.stderr.read1(1024)
                        if line:
                            git_msg = line.decode('utf-8', errors='replace').strip()
                            if git_msg:
                                status.update(f"[bold green]Pushing to GitHub...[/bold green] {git_msg}")
                except (IOError, UnicodeDecodeError):
                    pass
                
                time.sleep(0.1)
        
        # Calculate total uploaded size
        final_sent, _ = get_network_usage()
        total_uploaded = final_sent - initial_sent
        console.print(f"[blue]ℹ[/blue] Total data uploaded: {format_size(total_uploaded)}")
        
        # Check final status
        if process.returncode != 0:
            stderr = process.stderr.read().decode('utf-8', errors='replace') if process.stderr else ""
            raise subprocess.CalledProcessError(process.returncode, ["git", "push"], stderr=stderr.encode())
        
        console.print("[green]✓[/green] Changes pushed to GitHub")
        
    except subprocess.CalledProcessError as e:
        if "non-fast-forward" in str(e.stderr):
            console.print("[red]Error:[/red] Remote contains work that you do not have locally. Pull the remote changes first.")
        else:
            raise

def commit_and_push(message: Optional[str] = None, enable_logging: bool = False) -> None:
    """Main function to commit and push changes to GitHub."""
    if not message:
        message = "Update repository"
    
    try:
        initialize_environment(enable_logging)
        needs_repo_creation = handle_repository_setup()
        
        handle_gitignore_creation(enable_logging)
        
        # Check for changes before repository setup
        if not check_for_changes(enable_logging):
            console.print("[blue]ℹ[/blue] No changes to commit")
            return
        
        # Handle empty directories first
        handle_empty_directories()
        
        # Check for changes again after .gitkeep files
        if not check_for_changes(enable_logging):
            console.print("[blue]ℹ[/blue] No changes to commit after adding .gitkeep files")
            return
        
        # Calculate size before adding or committing
        console.print("\n[bold blue]Calculating Changes Size...[/bold blue]")
        total_size = calculate_repository_size()
        if total_size is not None:
            size_str = format_size(total_size)
            console.print(f"[blue]ℹ[/blue] Size of changes to be pushed [before compression]: {size_str}")
            
            if not handle_large_repository_warning(total_size):
                return
        
        # Handle repository creation/configuration before committing
        if needs_repo_creation:
            console.print("\n[bold blue]Configuring GitHub Repository...[/bold blue]")
            if not create_github_repo(directory_name, enable_logging):
                return
        
        console.print("\n[bold blue]Committing Changes...[/bold blue]")
        add_and_commit_changes(message, enable_logging)
        
        console.print("\n[bold blue]Pushing Changes...[/bold blue]")
        push_changes_with_progress(total_size, enable_logging)
        
    except subprocess.CalledProcessError as e:
        handle_subprocess_error(e)
    except Exception as e:
        handle_unexpected_error(e)
    finally:
        wait_for_user_input()

def handle_repository_setup() -> bool:
    """Handle git repository setup and return True if setup is needed."""
    is_initialized, has_origin = check_git_status()
    needs_repo_creation = False
    
    if not is_initialized:
        handle_git_init(True)  # Always enable logging for init
        needs_repo_creation = True
    elif not has_origin:
        needs_repo_creation = True
    
    return needs_repo_creation

def initialize_environment(enable_logging: bool) -> None:
    """Initialize the environment with logging if enabled."""
    if enable_logging:
        ensure_log_directories()
        console.print("[green]✓[/green] Logging enabled")

def calculate_repository_size() -> Optional[int]:
    """Calculate the total size of files to be pushed."""
    try:
        # Get list of modified files (including untracked)
        status_output = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        ).stdout.splitlines()
        
        if not status_output:
            return 0
            
        total_size = 0
        for line in status_output:
            # Status format is "XY PATH" where X is staged status and Y is unstaged
            if len(line) > 3:  # Make sure we have a valid line
                file_path = os.path.join(current_directory, line[3:].strip('"'))
                if os.path.isfile(file_path):
                    total_size += os.path.getsize(file_path)
                    
        return total_size
        
    except subprocess.CalledProcessError:
        return None

def display_size_info(total_size: int) -> None:
    size_str = format_size(total_size)
    console.print(f"[blue]ℹ[/blue] Total size to be pushed: {size_str}")

def handle_subprocess_error(e: subprocess.CalledProcessError) -> None:
    if "no changes added to commit" in str(e.stderr):
        console.print("[blue]ℹ[/blue] No changes to commit")
    else:
        raise

def handle_unexpected_error(e: Exception) -> None:
    console.print(f"[red]An unexpected error occurred: {str(e)}[/red]")
    raise

def wait_for_user_input() -> None:
    try:
        input("\nPress Enter to exit...")
    except (EOFError, ValueError, KeyboardInterrupt):
        pass

def run_command(command: list[str], cwd: str = None, log: bool = False) -> tuple[str, str]:
    """Run a command and return its output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=False,  # Use binary mode
            check=True
        )
        
        # Decode output using utf-8 with error handling
        stdout = result.stdout.decode('utf-8', errors='replace')
        stderr = result.stderr.decode('utf-8', errors='replace')
        
        if log:
            log_git_operation(command[0], {
                "command": command,
                "cwd": cwd,
                "stdout": stdout,
                "stderr": stderr
            })
        
        return stdout, stderr
    except subprocess.CalledProcessError as e:
        # Decode error output using utf-8 with error handling
        stdout = e.stdout.decode('utf-8', errors='replace') if e.stdout else ""
        stderr = e.stderr.decode('utf-8', errors='replace') if e.stderr else ""
        
        console.print(f"[red]Error running command:[/red] {' '.join(command)}")
        if stderr:
            console.print(f"[red]Error message:[/red] {stderr}")
        
        if log:
            log_git_operation(f"{command[0]}_error", {
                "command": command,
                "cwd": cwd,
                "error": str(e),
                "stdout": stdout,
                "stderr": stderr
            })
        
        raise

def get_username() -> str:
    """Get GitHub username from auth status."""
    try:
        stdout, _ = run_command(["gh", "auth", "status"], cwd=current_directory)
        first_index = stdout.find("account") + len("account") + 1
        last_index = stdout.find("(") - 1
        username = stdout[first_index:last_index].strip()
        console.print(f"[green]✓[/green] Logged in as: [bold blue]{username}[/bold blue]")
        return username
    except subprocess.CalledProcessError:
        console.print("[red]❌ Not logged in to GitHub. Please run 'gh auth login' first.[/red]")
        raise

def verify_directory_name(directory_name: str) -> str:
    """Verify and fix directory name if needed."""
    if " " in directory_name:
        console.print("[yellow]⚠ Warning: Directory name contains spaces[/yellow]")
        with console.status("[bold yellow]Fixing directory name..."):
            fixed_name = directory_name.replace(" ", "-")
        console.print(Panel(
            f"[green]Directory name fixed:[/green]\n[red]{directory_name}[/red] → [green]{fixed_name}[/green]",
            title="Directory Name Update"
        ))
        return fixed_name
    return directory_name

def check_repo_exists(repo_name: str) -> bool:
    """Check if repository already exists on GitHub."""
    try:
        result = subprocess.run(
            ["gh", "repo", "view", repo_name],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def create_github_repo(repo_name: str, enable_logging: bool = False) -> bool:
    """Create a new GitHub repository."""
    try:
        # First check if repo exists
        if check_repo_exists(repo_name):
            return handle_existing_repo(repo_name, enable_logging)
        
        console.print("[yellow]Creating new repository...[/yellow]")
        visibility = get_repository_visibility()
        create_repo(repo_name, visibility, enable_logging)
        return True
    except subprocess.CalledProcessError as e:
        return handle_repo_creation_error(e)

def handle_existing_repo(repo_name: str, enable_logging: bool) -> bool:
    """Handle case when repository already exists."""
    try:
        # Check if we have a remote configured
        current_remote = get_current_remote(enable_logging)
        expected_remote = f"https://github.com/{get_username()}/{repo_name}.git"
        
        if current_remote.strip() == expected_remote.strip():
            console.print("[blue]ℹ[/blue] Repository is already properly configured")
            return True
        else:
            console.print(Panel(
                f"[yellow]Remote configuration mismatch:[/yellow]\n" +
                f"[blue]Current:[/blue] {current_remote}\n" +
                f"[green]Expected:[/green] {expected_remote}",
                title="⚠ Remote Configuration"
            ))
            return handle_remote_mismatch(enable_logging, expected_remote)
    except subprocess.CalledProcessError:
        return configure_existing_remote(repo_name, enable_logging)

def handle_remote_mismatch(enable_logging: bool, expected_remote: str) -> bool:
    """Handle case when remote URL doesn't match expected URL."""
    console.print("\nChoose how to handle the remote configuration:")
    console.print("[1] [green]Update remote[/green] (point to existing repository)")
    console.print("[2] [blue]Keep current[/blue] (use current remote)")
    
    try:
        choice = input("\nEnter your choice (1-2): ").strip()
        console.print()  # Add newline after input
        
        if choice == "1":
            with console.status("[yellow]Updating remote...[/yellow]", spinner="dots"):
                run_command(["git", "remote", "set-url", "origin", expected_remote], 
                          current_directory, log=enable_logging)
            console.print("[green]✓[/green] Remote updated")
            return True
        elif choice == "2":
            console.print("[blue]ℹ[/blue] Keeping current remote")
            return True
        else:
            console.print("[red]Invalid choice. Keeping current remote.[/red]")
            return False
    except (EOFError, KeyboardInterrupt):
        console.print("\n[yellow]Operation cancelled[/yellow]")
        return False

def configure_existing_remote(repo_name: str, enable_logging: bool) -> bool:
    """Configure remote for existing repository."""
    try:
        remote_url = f"https://github.com/{get_username()}/{repo_name}.git"
        with console.status("[yellow]Configuring remote...[/yellow]", spinner="dots"):
            run_command(["git", "remote", "add", "origin", remote_url], 
                       current_directory, log=enable_logging)
        console.print("[green]✓[/green] Remote configured")
        return True
    except subprocess.CalledProcessError as e:
        if "remote origin already exists" in str(e.stderr):
            return handle_existing_repo(repo_name, enable_logging)
        console.print(f"[red]Failed to configure remote: {str(e.stderr)}[/red]")
        return False

def get_repository_visibility() -> str:
    """Prompt user for repository visibility."""
    console.print("\n[yellow]Choose repository visibility:[/yellow]")
    console.print("[P] [blue]Private[/blue] (default)")
    console.print("[U] [green]Public[/green]")
    
    try:
        choice = input("\nEnter your choice (P/u): ").strip().lower()
        console.print()  # Add newline after input
    except (EOFError, KeyboardInterrupt):
        choice = 'p'  # Default to private if interrupted
        console.print("\n[blue]Defaulting to private repository[/blue]")
    
    return "--public" if choice == 'u' else "--private"

def create_repo(repo_name: str, visibility: str, enable_logging: bool) -> None:
    """Create the GitHub repository."""
    with console.status(f"[bold green]Creating {visibility.replace('--', '')} GitHub repository...[/bold green]", spinner="dots"):
        run_command(["gh", "repo", "create", repo_name, visibility, "--source=.", "--remote=origin"], 
                   current_directory, log=enable_logging)
    console.print(f"[green]✓[/green] GitHub repository created ({visibility.replace('--', '')})")

def handle_repo_creation_error(e: subprocess.CalledProcessError) -> bool:
    """Handle errors during repository creation."""
    if "already exists" in e.stderr:
        console.print("[yellow]⚠[/yellow] Repository already exists")
        return False
    raise

def handle_existing_remote(enable_logging: bool = False) -> bool:
    """Handle existing remote origin with user choices."""
    try:
        current_remote = get_current_remote(enable_logging)
        display_remote_info(current_remote)
        display_options()
        choice = get_user_choice()
        return process_user_choice(choice, current_remote, enable_logging)
    except subprocess.CalledProcessError:
        return True  # No remote exists, need to create one

def get_current_remote(enable_logging: bool) -> str:
    stdout, _ = run_command(["git", "remote", "get-url", "origin"], current_directory, log=enable_logging)
    return stdout.strip()

def display_remote_info(current_remote: str) -> None:
    console.print(Panel(
        f"[yellow]Remote origin already exists:[/yellow]\n[blue]{current_remote}[/blue]",
        title="⚠ Existing Remote"
    ))

def display_options() -> None:
    console.print("\nChoose how to handle the existing remote:")
    console.print("[1] [green]Safe remove[/green] (remove remote only, keep repo)")
    console.print("[2] [red]Hard remove[/red] (remove remote and delete repo)")
    console.print("[3] [blue]Skip[/blue] (keep current remote)")

def get_user_choice() -> str:
    choice = input("\nEnter your choice (1-3): ").strip()
    console.print()  # Add newline after input
    return choice

def process_user_choice(choice: str, current_remote: str, enable_logging: bool) -> bool:
    if choice == "1":
        return safe_remove_remote(enable_logging)
    elif choice == "2":
        return hard_remove_remote(current_remote, enable_logging)
    elif choice == "3":
        return skip_remote_removal()
    else:
        return invalid_choice()

def safe_remove_remote(enable_logging: bool) -> bool:
    with console.status("[yellow]Removing remote...[/yellow]", spinner="dots"):
        run_command(["git", "remote", "remove", "origin"], current_directory, log=enable_logging)
    console.print("[green]✓[/green] Remote origin safely removed")
    return True

def hard_remove_remote(current_remote: str, enable_logging: bool) -> bool:
    delete_remote_repo(current_remote, enable_logging)
    remove_remote(enable_logging)
    return True

def delete_remote_repo(current_remote: str, enable_logging: bool) -> None:
    parts = current_remote.split("/")
    if len(parts) >= 2:
        repo_path = "/".join(parts[-2:]).replace(".git", "")
        try:
            with console.status("[red]Deleting remote repository...[/red]", spinner="dots"):
                run_command(["gh", "repo", "delete", repo_path, "--yes"], current_directory, log=enable_logging)
            console.print("[green]✓[/green] Remote repository deleted")
        except subprocess.CalledProcessError:
            console.print("[yellow]⚠[/yellow] Failed to delete remote repository, but continuing...")

def remove_remote(enable_logging: bool) -> None:
    with console.status("[yellow]Removing remote...[/yellow]", spinner="dots"):
        run_command(["git", "remote", "remove", "origin"], current_directory, log=enable_logging)
    console.print("[green]✓[/green] Remote origin removed")

def skip_remote_removal() -> bool:
    console.print("[blue]ℹ[/blue] Keeping current remote")
    return False

def invalid_choice() -> bool:
    console.print("[red]Invalid choice. Keeping current remote.[/red]")
    return False

def add_gitkeep_to_empty_dirs(base_dir: str = None) -> None:
    """Add .gitkeep files to empty directories."""
    if base_dir is None:
        base_dir = current_directory
    
    empty_dirs = find_empty_directories(base_dir)
    
    if empty_dirs:
        display_empty_directories(empty_dirs, base_dir)
        if user_confirms_add_gitkeep():
            add_gitkeep_files(empty_dirs, base_dir)
    else:
        console.print("\n[blue]ℹ[/blue] No empty directories found")

def find_empty_directories(base_dir: str) -> list:
    """Find all empty directories in the given base directory."""
    empty_dirs = []
    for root, dirs, files in os.walk(base_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if is_directory_empty(dir_path):
                empty_dirs.append(dir_path)
    return empty_dirs

def is_directory_empty(dir_path: str) -> bool:
    """Check if a directory is empty (excluding .gitkeep)."""
    dir_contents = [f for f in os.listdir(dir_path) if f != '.gitkeep']
    return not dir_contents

def display_empty_directories(empty_dirs: list, base_dir: str) -> None:
    """Display the list of empty directories."""
    console.print(f"\nFound [yellow]{len(empty_dirs)}[/yellow] empty directories:")
    for dir_path in empty_dirs:
        rel_path = os.path.relpath(dir_path, base_dir)
        console.print(f"  [blue]• {rel_path}[/blue]")

def user_confirms_add_gitkeep() -> bool:
    """Ask user for confirmation to add .gitkeep files."""
    choice = input("\nAdd .gitkeep to empty directories? (y/N): ").strip().lower()
    return choice == 'y'

def add_gitkeep_files(empty_dirs: list, base_dir: str) -> None:
    """Add .gitkeep files to the specified empty directories."""
    with console.status("[green]Adding .gitkeep files...[/green]", spinner="dots") as status:
        for dir_path in empty_dirs:
            add_gitkeep_to_directory(dir_path, base_dir)
    console.print("\n[green]✓[/green] Finished adding .gitkeep files")

def add_gitkeep_to_directory(dir_path: str, base_dir: str) -> None:
    """Add a .gitkeep file to a specific directory."""
    gitkeep_path = os.path.join(dir_path, '.gitkeep')
    if not os.path.exists(gitkeep_path):
        with open(gitkeep_path, 'w') as f:
            pass  # Create empty file
        rel_path = os.path.relpath(dir_path, base_dir)
        console.print(f"[green]✓[/green] Added .gitkeep to: {rel_path}")

def is_git_repo(directory: str) -> bool:
    """Check if directory is a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=directory,
            capture_output=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False

def check_git_status() -> tuple[bool, bool]:
    """
    Check git repository status.
    Returns: (is_initialized, has_origin)
    """
    is_initialized = is_git_repo(current_directory)
    has_origin = False
    
    if is_initialized:
        try:
            run_command(["git", "remote", "get-url", "origin"], current_directory)
            has_origin = True
        except subprocess.CalledProcessError:
            has_origin = False
    
    return is_initialized, has_origin

def ensure_log_directories():
    """Create log directories if they don't exist."""
    LOGS_DIR.mkdir(exist_ok=True)
    CRASH_LOGS_DIR.mkdir(exist_ok=True)

def log_crash(exc_type, exc_value, exc_traceback):
    """Log any unhandled exceptions to a crash log file."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    ensure_crash_log_directory()
    crash_file = create_crash_log_file()
    
    try:
        write_crash_log(crash_file, exc_type, exc_value, exc_traceback)
        console.print(f"\n[red]❌ Script crashed! Crash log saved to:[/red] {crash_file}")
    except Exception as e:
        console.print(f"[red]Failed to write crash log: {str(e)}[/red]")
    
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

def ensure_crash_log_directory():
    """Ensure the crash log directory exists."""
    CRASH_LOGS_DIR.mkdir(exist_ok=True)

def create_crash_log_file():
    """Create and return the path for a new crash log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return CRASH_LOGS_DIR / f"log-crash-{timestamp}.log"

def write_crash_log(crash_file, exc_type, exc_value, exc_traceback):
    """Write crash information to the log file."""
    with open(crash_file, "w") as f:
        write_crash_header(f)
        write_exception_info(f, exc_type, exc_value, exc_traceback)
        write_system_info(f)
        write_git_info(f)

def write_crash_header(f):
    """Write the crash report header."""
    f.write("=== Crash Report ===\n")
    f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}\n")

def write_exception_info(f, exc_type, exc_value, exc_traceback):
    """Write exception information to the log file."""
    f.write(f"Exception Type: {exc_type.__name__}\n")
    f.write(f"Exception Message: {str(exc_value)}\n")
    f.write("\nTraceback:\n")
    traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)

def write_system_info(f):
    """Write system information to the log file."""
    f.write("\nSystem Information:\n")
    f.write(f"Python Version: {sys.version}\n")
    f.write(f"Platform: {sys.platform}\n")
    f.write(f"Current Directory: {os.getcwd()}\n")

def write_git_info(f):
    """Write git information to the log file if available."""
    try:
        stdout = subprocess.run(["git", "rev-parse", "HEAD"], 
                                capture_output=True, text=True, check=True).stdout.strip()
        f.write(f"Git Commit: {stdout}\n")
    except:
        f.write("Git information not available\n")

# Set up the global exception handler
sys.excepthook = log_crash

def log_git_operation(operation: str, data: dict) -> None:
    """Log git operations to a log file."""
    try:
        # Ensure logs directory exists
        LOGS_DIR.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_file = LOGS_DIR / f"log-{timestamp}.json"
        
        with open(log_file, "w") as f:
            json.dump({
                "timestamp": timestamp,
                "operation": operation,
                "data": data
            }, f, indent=4)
    except Exception as e:
        # Don't fail the main operation if logging fails
        console.print(f"[yellow]⚠[/yellow] Failed to write log: {str(e)}")

# Define log directories
LOGS_DIR = Path("logs")
CRASH_LOGS_DIR = Path("log-crash")

# Get the current directory name
current_directory = os.getcwd()
directory_name = os.path.basename(current_directory)

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

# Src files
get_to_repo.py
git_to_repo.py

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


def display_welcome_message():
    console.print(Panel.fit(
        "[bold blue]GitHub Repository Setup[/bold blue]",
        subtitle="[italic]Automated with ♥[/italic]"
    ))

def prompt_for_logging():
    console.print("\n[yellow]Would you like to enable detailed operation logging?[/yellow]")
    console.print("[blue]This will log all git operations for debugging purposes.[/blue]")
    enable_logging = input("Enable logging? (y/N): ").strip().lower() == 'y'
    if enable_logging:
        console.print("[green]✓[/green] Logging enabled")
    return enable_logging

def setup_repository():
    """Setup repository and return necessary information."""
    global directory_name
    directory_name = verify_directory_name(directory_name)
    username = get_username()
    return f"https://github.com/{username}/{directory_name}.git"

def handle_commit_and_push(enable_logging):
    commit_msg = input("\nEnter commit message (press Enter for default): ").strip()
    commit_and_push(commit_msg if commit_msg else None, enable_logging=enable_logging)

def handle_error(e):
    console.print("\n[red]Process failed. Please fix the errors above and try again.[/red]")
    exit(1)

def display_completion_message():
    console.print("\n[bold green]✨ Process completed successfully![/bold green]")


if __name__ == "__main__":
    display_welcome_message()
    
    try:
        enable_logging = prompt_for_logging()
        repo_url = setup_repository()
        handle_commit_and_push(enable_logging)
    except Exception as e:
        handle_error(e)
    finally:
        display_completion_message()
