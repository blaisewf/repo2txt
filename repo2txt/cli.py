import click
from repo2txt.decoder import (
    clone_repo,
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

    click.echo(f"Cloning repository {repo_url} into directory {clone_dir}...")
    clone_repo(repo_url, clone_dir)

    click.echo("Generating directory structure...")
    directory_structure = get_directory_structure(clone_dir)

    click.echo("Extracting file contents...")
    file_contents = extract_all_files_contents(clone_dir)

    click.echo(f"Writing output to {output_file}...")
    write_output_file(output_file, directory_structure, file_contents)

    click.echo("Cleaning up...")
    cleanup(clone_dir)

    click.echo("Process completed successfully.")


if __name__ == "__main__":
    cli()
