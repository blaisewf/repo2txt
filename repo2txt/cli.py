import click
from repo2txt.decoder import (
    download_repo,
    extract_repo_name_from_url,
    get_directory_structure,
    extract_all_files_contents,
    write_output_file,
    cleanup,
)


@click.command()
@click.option(
    "--repo-url",
    prompt="Repository URL",
    help="URL of the GitHub repository to process.",
)
@click.option(
    "--output-file", prompt="Output file path", help="Path to the output text file."
)
def cli(repo_url, output_file):
    """CLI entry point for generating a text file with repository structure and all file contents."""
    repo_name = extract_repo_name_from_url(repo_url)
    clone_dir = repo_name

    download_repo(repo_url, clone_dir)

    directory_structure = get_directory_structure(clone_dir)
    file_contents = extract_all_files_contents(clone_dir)

    write_output_file(output_file, directory_structure, file_contents)
    cleanup(clone_dir)
    print(f"Output file generated at {output_file}")


if __name__ == "__main__":
    cli()
