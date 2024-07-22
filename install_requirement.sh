
### `install_requirements.sh`

Here is the updated `install_requirements.sh` script to automate the installation process with conda:

```bash
#!/bin/bash

# From the directory /topic_matching_project it creates a conda environment
conda create --name topic_matching_env python=3.9 -y
source activate topic_matching_env

# Install dependencies
pip install -r requirements.txt

echo "Installation complete. You can now run the Flask backend and Streamlit frontend as described in the README.md."
