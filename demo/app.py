import gradio as gr
from repo2txt.decoder import (
    clone_repo,
    get_directory_structure,
    extract_all_files_contents,
    write_output_file,
    cleanup,
)


def process_repository(repo_url_or_shorthand):
    """Process the GitHub repository and return the content of the output file."""
    # Define the directory to clone into
    clone_dir = "temp_repo"
    output_file = "output.txt"

    try:
        # Clone the repository
        clone_repo(repo_url_or_shorthand, clone_dir)

        # Get directory structure and file contents
        directory_structure = get_directory_structure(clone_dir)
        file_contents = extract_all_files_contents(clone_dir)

        # Write output to file
        write_output_file(output_file, directory_structure, file_contents)

        # Read the content of the output file
        with open(output_file, "r", encoding="utf-8") as file:
            output_content = file.read()

        # Cleanup
        cleanup(clone_dir)
        # Return the output file path for Gradio
        return output_content, output_file

    except Exception as e:
        return f"An error occurred: {e}", None


# Define Gradio interface
with gr.Blocks(title="repo2txt") as demo:
    gr.Markdown("# repo2txt")

    with gr.Row():
        repo_url_input = gr.Textbox(
            label="GitHub Repository URL or Shorthand",
            placeholder="e.g., user/repo or https://github.com/user/repo",
        )

    process_button = gr.Button("Process Repository")
    txt_output = gr.File(label="Download txt file")
    result_output = gr.Textbox(
        label="Result",
        lines=1,
        placeholder="Processing result will be shown here",
    )

    process_button.click(
        process_repository, inputs=repo_url_input, outputs=[result_output, txt_output]
    )

# Launch the interface
if __name__ == "__main__":
    demo.launch()
