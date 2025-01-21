#!/bin/bash

# Check if the virtual environment directory exists
if [ ! -d "venv" ]; then
  # Create a virtual environment
  python -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install/upgrade packages from requirements.txt
pip install --upgrade pip -q
pip install --upgrade -r requirements.txt -q

# Run the ado-pipeline-doc script with any passed arguments
python ado-pipeline-doc "$@"
