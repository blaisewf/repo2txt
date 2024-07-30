import os
import shutil
import subprocess


def is_git_installed():
    """Check if Git is installed."""
    try:
        subprocess.run(
            ["git", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return True
    except FileNotFoundError:
        return False


def clone_repo(repo_url, clone_dir):
    """Clone the GitHub repository into the specified directory."""
    if is_git_installed():
        subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
    else:
        raise RuntimeError(
            "Git is not installed. Please install Git to clone repositories."
        )


def extract_repo_name_from_url(repo_url):
    """Extract the repository name from the GitHub URL."""
    repo_name = repo_url.rstrip("/").split("/")[-1]
    return repo_name.split(".")[0] if "." in repo_name else repo_name


def get_directory_structure(root_dir):
    """Get the directory structure in a tree format, ignoring .git directory."""
    lines = []
    for root, dirs, files in os.walk(root_dir):
        if ".git" in dirs:
            dirs.remove(".git")  # Avoid walking into .git directory

        level = root.replace(root_dir, "").count(os.sep)
        indent = " " * 4 * level
        lines.append(f"{indent}├── {os.path.basename(root)}/")

        subindent = " " * 4 * (level + 1)
        for file in files:
            lines.append(f"{subindent}├── {file}")
    return "\n".join(lines)


def read_file_contents(file_path):
    """Read the contents of a file, ignore if in .git directory."""
    if ".git" in file_path:
        return "[Ignored .git directory]"

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except (UnicodeDecodeError, OSError) as e:
        return f"[Error reading file: {e}]"


def extract_all_files_contents(root_dir):
    """Extract contents of all files in the directory, ignoring .git directory."""
    file_contents = {}
    for root, _, files in os.walk(root_dir):
        if ".git" in root:
            continue

        for file_name in files:
            file_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(file_path, root_dir)
            file_contents[relative_path] = read_file_contents(file_path)
    return file_contents


def count_tokens(text):
    """Count the number of tokens in a given text."""
    return len(text.split())


def write_output_file(output_file, directory_structure, file_contents):
    """Write the directory structure and file contents to the output file with metadata."""
    total_lines = directory_structure.count("\n") + sum(
        content.count("\n") for content in file_contents.values()
    )
    total_chars = len(directory_structure) + sum(
        len(content) for content in file_contents.values()
    )

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"Lines: {total_lines}\nCharacters: {total_chars}\n\n")
        file.write("Directory Structure:\n```\n")
        file.write(directory_structure)
        file.write("\n```\n")

        for file_path, content in file_contents.items():
            file.write(f"\nContents of {file_path}:\n```\n")
            file.write(content)
            file.write("\n```\n")


def cleanup(clone_dir):
    """Remove the cloned repository directory with error handling."""
    if os.path.exists(clone_dir):
        try:
            shutil.rmtree(clone_dir, onerror=handle_remove_error)
        except Exception as e:
            print(f"An error occurred while cleaning up: {e}")


def handle_remove_error(func, path, exc_info):
    """Error handler for shutil.rmtree to handle permission errors."""
    import stat

    if isinstance(exc_info[1], PermissionError):
        os.chmod(path, stat.S_IWRITE)
        func(path)
    else:
        print(f"Error removing {path}: {exc_info[1]}")
