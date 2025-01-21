# Azure DevOps Pipeline Documentation Generator

This script processes an Azure DevOps pipeline YAML file and generates markdown documentation for the pipeline parameters. It is useful for creating human-readable documentation from pipeline configurations.

## Features

- Parses Azure DevOps pipeline YAML files.
- Generates markdown tables with parameter details.
- Supports optional output to a markdown file or console.

## Requirements

- Python 3.x
- PyYAML

## Installation

1. Clone the repository:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required Python packages:

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
