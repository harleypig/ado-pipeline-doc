#!/usr/bin/env python

# Parameter and Types:
#  https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/parameters-parameter

# Parameter Keys:
# Required: name, type
# Optional: displayName, default, values

# Data Types:
# string, number, boolean, object

# Note: There is no native way in azure pipelines to enforce an object's
#       structure.

import argparse
import yaml
import sys
import os
import tempfile


##############################################################################
class ADOPipelineDocException(Exception):
  pass


##############################################################################
class ADOPipelineDoc:
  #---------------------------------------------------------------------------
  def __init__(self, yamlFile=None, mdFile=None):
    """    
    Initializes the ADOPipelineDoc with a given YAML input file and an
    optional output file.

    Args:
      yamlFile (str): The path to the YAML file containing pipeline parameters.
      mdFile (str, optional): The path to the output file where the processed
                              data will be saved. If not provided, the output
                              will be printed to the console.

    Raises:
      ADOPipelineDocException: If no input file is provided.
    """
    self.data = None
    self.mdEnd = 'ADOPipelineDoc End'
    self.mdFile = mdFile
    self.mdStart = 'ADOPipelineDoc Start'
    self.yamlFile = yamlFile

    if self.yamlFile is None:
      raise ADOPipelineDocException(
        "Input file must be provided to ADOPipelineDoc.")

    self.parseYAML()
    self.processData()
    self.writeFile()

  #---------------------------------------------------------------------------
  def mdStartStr(self):
    """
    Returns the markdown start string used to denote the beginning of the
    ADOPipelineDoc section in the markdown file.

    Returns:
      str: The markdown start string.
    """
    return f"<!-- {self.mdStart} -->"

  def mdEndStr(self):
    """
    Returns the markdown end string used to denote the end of the
    ADOPipelineDoc section in the markdown file.

    Returns:
      str: The markdown end string.
    """
    return f"<!-- {self.mdEnd} -->"

  def printTable(self):
    """
    Prints the markdown table of pipeline parameters to the console.

    This function outputs the processed markdown table, which includes
    parameter details such as name, type, and any optional fields, to the
    console. It is used when no markdown file is specified for output.
    """
    print("\n".join(self.table_rows))

  #---------------------------------------------------------------------------
  def readFile(self, file_path):
    """
    Reads the content of a file.

    Args:
      file_path (str): The path to the file to be read.

    Returns:
      str: The content of the file.

    Raises:
      ADOPipelineDocException: If the file cannot be accessed.
    """
    try:
      with open(file_path, 'r') as file:
        return file.read()

    except FileNotFoundError:
      raise ADOPipelineDocException(f"The file {file_path} was not found.")

    except PermissionError:
      raise ADOPipelineDocException(
        f"Permission denied for file {file_path}.")

  #---------------------------------------------------------------------------
  def prettyObject(self, obj, key=None):
    """
    Converts a given object to a pretty-printed string format.

    Args:
      obj (any): The object to be converted to a string.
      key (str, optional): The key associated with the object.

    Returns:
      str: A pretty-printed string representation of the object suitable for use
           in a markdown table.

    Raises:
      ADOPipelineDocException:
        - If a key is passed and the object is not a dictionary.
        - If the key is not found in the object.
    """
    if key is not None:
      if not isinstance(obj, dict):
        raise ADOPipelineDocException(
          "Object must be a dictionary if a key is provided.")

      if key not in obj:
        raise ADOPipelineDocException(f"Key '{key}' not found in the object.")

      pretty = yaml.dump(obj[key], default_flow_style=False)

    else:
      pretty = yaml.dump(obj, default_flow_style=False)

    return pretty.strip().replace('\n', '<br/>')

  #---------------------------------------------------------------------------
  def parseYAML(self):
    """
    Loads the YAML file specified by the filename attribute and stores its
    parsed contents in the data attribute.

    Raises:
      ADOPipelineDocException:
        - If the YAML file is empty or contains null data.
        - If the YAML file has no parameters.
        - If there is an error in parsing the YAML content.
    """
    try:
      content = self.readFile(self.yamlFile)
      self.data = yaml.safe_load(content)

      if self.data is None:
        raise ADOPipelineDocException(
          "YAML file is empty or contains null data.")

      params = self.data.get('parameters', [])

      if not params:
        raise ADOPipelineDocException("YAML file has no parameters.")

      self.parameters = params

    except yaml.YAMLError as e:
      raise ADOPipelineDocException(f"Error parsing YAML file: {e}")

  #---------------------------------------------------------------------------
  def processData(self):
    """
    Processes the YAML parameters and converts them into a markdown table
    format.

    This method checks each parameter for required fields and optional fields
    like displayName, values, and default. It creates each row in the table and
    stores them in the table_rows attribute as an array. The table includes
    headers and rows representing each parameter's details.

    Raises:
      ADOPipelineDocException: If a parameter is missing 'name' or 'type'.
    """
    heading_order = [
      'required', 'name', 'type', 'displayName', 'values', 'default'
    ]

    heading_separator = {
      "required": ":-:",
      "name": ":--",
      "type": ":--",
      "displayName": ":--",
      "values": ":--",
      "default": ":--"
    }

    object_template = {
      "required": "Yes",
      "name": '',
      "type": '',
      "displayName": '',
      "values": '',
      "default": ''
    }

    use_col = {"displayName": False, "values": False, "default": False}

    rows = []

    for param in self.parameters:
      if not param.get('name') or not param.get('type'):
        raise ADOPipelineDocException(
          f"Parameter missing 'name' or 'type': {param}")

      if param.get('displayName', ''):
        use_col["displayName"] = True

      if param.get('values', ''):
        use_col["values"] = True

      row_object = object_template.copy()
      row_object.update(param)

      if param.get('default', ''):
        use_col["default"] = True
        row_object["required"] = ''

      if param.get('type') == 'object' and param.get('default'):
        row_object['default'] = self.prettyObject(param, key='default')

      if param.get('values'):
        row_object['values'] = self.prettyObject(param, key='values')

      rows.append(row_object)

    for key, value in use_col.items():
      if not value:
        heading_order.remove(key)
        for row in rows:
          row.pop(key, None)

    table_rows = []
    if self.mdFile is not None: table_rows.append(f"{self.mdStartStr()}")

    # Build the markdown header row
    header_row = "| " + " | ".join(heading_order) + " |"
    separator_row = "| " + " | ".join(heading_separator[key]
                                      for key in heading_order) + " |"

    # Add header and separator to table_rows
    table_rows.append(header_row)
    table_rows.append(separator_row)

    # Add parameter rows to table_rows
    for row in rows:
      row_data = [str(row.get(key, '')) for key in heading_order]
      row_text = "| " + " | ".join(row_data) + " |"
      table_rows.append(row_text)

    if self.mdFile is not None: table_rows.append(f"{self.mdEndStr()}")

    self.table_rows = table_rows

  #---------------------------------------------------------------------------
  def writeFile(self):
    """
    Writes the markdown table to the specified markdown file or prints it to
    the console if no file is specified. If the file exists, it updates the
    content between the start and end comments. If the file doesn't exist, it
    creates a new one. Raises an exception if the file exists but lacks the
    necessary comments.

    Raises:
      ADOPipelineDocException: If the file exists and lacks start or end
      comments.
    """
    if self.mdFile is None:
      self.printTable()
      return

    try:
      content = self.readFile(self.mdFile)

      start_index = content.find(self.mdStartStr())
      end_index = content.find(self.mdEndStr())

      if start_index == -1 and end_index > -1:
        raise ADOPipelineDocException(
          f"No start comment found in {self.mdFile}.")

      if start_index > -1 and end_index == -1:
        raise ADOPipelineDocException(
          f"No end comment found in {self.mdFile}.")

      # Create a temporary file
      with tempfile.NamedTemporaryFile('w', delete=False) as temp_file:
        temp_file_name = temp_file.name

        # No start or end comments, append to end of file
        if start_index == -1 and end_index == -1:
          temp_file.write(content + "\n" + "\n".join(self.table_rows))

        else:
          end_index += len(self.mdEndStr())
          new_content = (content[:start_index] + "\n".join(self.table_rows) +
                         content[end_index:])
          temp_file.write(new_content)

      os.replace(temp_file_name, self.mdFile)

    except FileNotFoundError:
      with open(self.mdFile, 'w') as file:
        file.write("\n".join(self.table_rows) + "\n")


##############################################################################
def parse_arguments():
  """
  Parses command line arguments for the script.

  Returns:
    Namespace: The parsed arguments as a namespace object.
  """
  parser = argparse.ArgumentParser(
    description=
    'Process Azure DevOps pipeline YAML file and generate markdown documentation.'
  )

  parser.add_argument(
    'yamlFile',
    metavar='YAMLFILE',
    type=str,
    help='The path to the YAML file containing pipeline parameters.')

  parser.add_argument(
    '--mdfile',
    '--markdown-file',
    type=str,
    metavar='MARKDOWNFILE',
    help=
    'The path to the output markdown file. If not provided, output will be printed to the console.'
  )

  return parser.parse_args()


##############################################################################
if __name__ == "__main__":
  args = parse_arguments()

  try:
    ADOPipelineDoc(args.yamlFile, args.mdfile)

  except ADOPipelineDocException as e:
    print(f"Error: {e}")
