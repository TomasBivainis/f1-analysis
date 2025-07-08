import os
import json

def load_json(filename: str, dir: str = "data"):
    """
    Loads and parses a JSON file from the specified directory.

    Args:
        filename (str): The name of the JSON file.
        dir (str): The directory where the file is located.

    Returns:
        object: The parsed Python object (dict or list) from the JSON file.
    """
    filepath = os.path.join(dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)