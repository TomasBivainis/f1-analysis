import os
import json

def save_to_json(data, filename: str, dir:str = "data"):
  """
  Save the data to the specified JSON file in the given directory.

  Args:
      data: The data to be saved to the JSON file.
      filename (str): The name of the JSON file.
      dir (str): The directory where the file is located.

  Returns:
      None
  """
  with open(os.path.join(dir, filename + ".json"), "w") as json_file:
    json.dump(data, json_file)
    
def convert_object_list_to_dict_list(object_list: list[object]):
  """
  Converts a list of objects to a list of dictionaries.

  Args:
      object_list (list): A list of objects. Each object must have a `to_dict` method.

  Returns:
      list[dict]: A list of dictionaries, where each dictionary is the result of calling `to_dict` on an object.
  """
  res = []
  
  for obj in object_list:
    res.append(obj.to_dict())
    
  return res

def convert_dict_list_to_object_list(dict_list: list[dict], object_type):
    """
    Converts a list of dictionaries to a list of objects of the specified type.

    Args:
        dict_list (list[dict]): List of dictionaries to convert.
        object_type (type): The class/type to instantiate for each dictionary.

    Returns:
        list: List of instantiated objects.
    """
    return [object_type(**d) for d in dict_list]

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