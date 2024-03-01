import os 
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

list_of_files = [
    "src/__init__.py",
    "src/helpers.py",
    "src/prompts.py",
    "src/exceptions.py",
    "src/logger.py",
    "app.py",
    "static",
    "templates/chat.html",
]


for file_path in list_of_files:
    path = Path(file_path)
    # file_dir, file_path = os.path.split(file_path)

    if path.exists():
        logging.info(f"{file_path} exists")
    else:
        logging.error(f"{file_path} does not exist. Creating {file_path}")
        with open(file_path, "w") as f:
            f.write("")