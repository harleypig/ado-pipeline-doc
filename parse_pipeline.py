import yaml

def parse_yaml_to_markdown(yaml_file_path):
    # Load the YAML file
    with open(yaml_file_path, 'r') as file:
        yaml_content = yaml.safe_load(file)

    # Extract parameters
    parameters = yaml_content.get('parameters', [])

    # Prepare markdown table
    markdown_table = "| Name | Type | Default | Description |\n"
    markdown_table += "|------|------|---------|-------------|\n"

    for param in parameters:
        name = param.get('name', '')
        param_type = param.get('type', '')
        default = param.get('default', '')
        description = param.get('description', '')

        markdown_table += f"| {name} | {param_type} | {default} | {description} |\n"

    return markdown_table

# Example usage
yaml_file_path = 'azure-pipelines.yml'  # Replace with your YAML file path
markdown_output = parse_yaml_to_markdown(yaml_file_path)
print(markdown_output)
