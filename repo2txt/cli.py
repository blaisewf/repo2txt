import os
import click
import json
from repo2txt.decoder import (
    download_repo,
    extract_repo_name_from_url,
    get_directory_structure,
    extract_all_files_contents,
    write_output_file,
    cleanup,
)

def load_config(config_file):
    """Load ignore patterns from the config file."""
    if config_file and os.path.exists(config_file):
        with open(config_file, 'r') as file:
            return json.load(file)
    return {}

@click.command()
@click.option(
    "--repo-url",
    prompt="Repository URL",
    help="URL of the GitHub repository to process.",
)
@click.option(
    "--output-file", prompt="Output file path", help="Path to the output text file."
)
@click.option(
    "--branch", default="main", help="Branch name to download. Defaults to 'main'."
)
@click.option(
    "--config", default=None, help="Path to the config.json file for ignoring files/folders."
)
def cli(repo_url, output_file, branch, config):
    """CLI entry point for generating a text file with repository structure and all file contents."""
    try:
        repo_name = extract_repo_name_from_url(repo_url)
        clone_dir = repo_name

        ignore_patterns = load_config(config)
        download_repo(repo_url, clone_dir, branch)

        directory_structure = get_directory_structure(clone_dir, ignore_patterns)
        file_contents = extract_all_files_contents(clone_dir, ignore_patterns)

        write_output_file(output_file, directory_structure, file_contents)
        print(f"Output file generated at {output_file}")
    except ValueError as e:
        print(e)
    finally:
        cleanup(clone_dir)


if __name__ == "__main__":
    cli()
