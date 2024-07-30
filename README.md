# repo2txt

`repo2txt` is a Python package that clones a GitHub repository, generates a text file containing the repository's directory structure and the contents of all its files, and handles cleanup.

## Installation

You can install `repo2txt` using pip:

```sh
pip install git+https://github.com/blaisewf/repo2txt.git
```

Alternatively, you can clone the repository and install it locally:

```sh
git clone https://github.com/blaisewf/repo2txt.git
cd repo2txt
pip install .
```

> [!WARNING]  
> Git is required to clone the repository. If you don't have Git installed, you can download it from [git-scm.com](https://git-scm.com/).

## Usage

Once installed, you can use the CLI command `repo2txt` to process a GitHub repository. Here’s the basic syntax:

```sh
repo2txt --repo-url <repository_url> --output-file <output_file_path>
```

### Example

```sh
repo2txt --repo-url https://github.com/example/repository.git --output-file output.txt
```

This command will:

1. Clone the repository from `https://github.com/example/repository.git`.
2. Generate a text file `output.txt` containing the directory structure and contents of all files in the repository.
3. Clean up the cloned repository directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## References
- https://github.com/kirill-markin/repo-to-text
