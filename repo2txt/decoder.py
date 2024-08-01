import os
import shutil
import zipfile
import wget
from tqdm import tqdm
import requests


def convert_to_full_url(repo_url_or_shorthand):
    """Convert shorthand 'user/repo' format to full URL format."""
    if repo_url_or_shorthand.startswith("http"):
        return repo_url_or_shorthand  # Already a full URL
    return f"https://github.com/{repo_url_or_shorthand}"


def extract_repo_name_from_url(repo_url):
    """Extract the repository name from the GitHub URL."""
    repo_name = repo_url.rstrip("/").split("/")[-1]
    return repo_name.split(".")[0] if "." in repo_name else repo_name


def download_repo(repo_url_or_shorthand, download_dir, branch="main"):
    """Download the GitHub repository as a ZIP file and extract it."""
    repo_url = convert_to_full_url(repo_url_or_shorthand)
    repo_name = extract_repo_name_from_url(repo_url)
    zip_url = f"{repo_url}/archive/refs/heads/{branch}.zip"
    zip_path = os.path.join(download_dir, f"{repo_name}.zip")

    # Ensure the download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Check if the branch exists by sending a head request
    response = requests.head(zip_url)
    if response.status_code == 404:
        raise ValueError(
            f"The branch '{branch}' does not exist for the repository '{repo_url}'."
        )

    print(f"Downloading {zip_url} to {zip_path}")
    wget.download(zip_url, zip_path)

    extract_dir = os.path.join(download_dir, repo_name)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        for file in tqdm(zip_ref.namelist(), desc="Extracting files"):
            zip_ref.extract(file, extract_dir)

    os.remove(zip_path)  # Clean up the ZIP file
    return extract_dir


def should_ignore(path, ignore_patterns):
    """Determine if a file or directory should be ignored based on patterns."""
    if not ignore_patterns:
        return False
    for pattern in ignore_patterns.get("ignore", []):
        if pattern.startswith("*.") and path.endswith(pattern[1:]):
            return True
        if pattern in path:
            return True
    return False


def get_directory_structure(root_dir, ignore_patterns=None):
    """Get the directory structure in a tree format, ignoring .git directory and specified patterns."""
    lines = []
    for root, dirs, files in os.walk(root_dir):
        if should_ignore(root, ignore_patterns):
            continue
        level = root.replace(root_dir, "").count(os.sep)
        indent = " " * 4 * level
        lines.append(f"{indent}├── {os.path.basename(root)}/")

        subindent = " " * 4 * (level + 1)
        for file in files:
            file_path = os.path.join(root, file)
            if should_ignore(file_path, ignore_patterns):
                continue
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


def extract_all_files_contents(root_dir, ignore_patterns=None):
    """Extract contents of all files in the directory, ignoring .git directory and specified patterns."""
    file_contents = {}
    all_files = []
    for root, _, files in os.walk(root_dir):
        if should_ignore(root, ignore_patterns):
            continue
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if should_ignore(file_path, ignore_patterns):
                continue
            relative_path = os.path.relpath(file_path, root_dir)
            all_files.append((relative_path, file_path))

    for relative_path, file_path in tqdm(all_files, desc="Reading file contents"):
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

        for file_path, content in tqdm(
            file_contents.items(), desc="Writing file contents"
        ):
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
