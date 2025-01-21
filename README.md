# Azure DevOps Pipeline Documentation Generator

This script processes an Azure DevOps pipeline YAML file and generates markdown documentation for the pipeline parameters. It is useful for creating human-readable documentation from pipeline configurations.

## Features

- Parses Azure DevOps pipeline YAML files.
- Generates markdown tables with parameter details.
- Supports optional output to a markdown file or console.

## Error Handling

The script includes custom error handling to manage various exceptions that may occur during execution. The primary custom exception used is `ADOPipelineDocException`, which is raised in the following scenarios:

- If the input YAML file is not provided.
- If the YAML file is empty or contains null data.
- If the YAML file has no parameters.
- If there is an error in parsing the YAML content.
- If a parameter is missing required fields such as 'name' or 'type'.
- If the output markdown file exists but lacks the necessary start or end comments.

# For the above, explain that having one or the other comment, but not both, causes an error. Otherwise, the table is appended to the end of the file, AI!

## Requirements

- Python 3.x
- PyYAML

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. It is recommended to use a virtual environment to manage dependencies. You can create and activate a virtual environment with the following commands:

   ### Windows (PowerShell)
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

   ### Linux (bash) / macOS (zsh)
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the path to the YAML file as a required argument. Optionally, specify an output markdown file.

```bash
python ado-pipeline-doc <YAMLFILE> [--mdfile <MARKDOWNFILE>]
```

- `YAMLFILE`: The path to the YAML file containing pipeline parameters.
- `--mdfile` or `--markdown-file`: The path to the output markdown file. If not provided, the output will be printed to the console.

## License

This project is licensed under the Unlicense. See the [LICENSE](LICENSE) file for more details.
