import json
import yaml
import xmltodict

class FileReader:
    def __init__(self, input_file, input_format):
        self.input_file = input_file
        self.input_format = input_format.lower()

    def read_file(self):
        try:
            with open(self.input_file, "r") as file:
                if self.input_format == "json":
                    return json.load(file)
                elif self.input_format == "yaml":
                    return yaml.safe_load(file)
                elif self.input_format == "xml":
                    return xmltodict.parse(file.read())
                else:
                    raise ValueError("Unsupported input format")
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: Input file '{self.input_file}' not found.")
        except json.JSONDecodeError:
            raise ValueError(f"Error: Invalid JSON format in '{self.input_file}'.")
        except yaml.YAMLError as e:
            raise ValueError(f"Error: Invalid YAML format in '{self.input_file}': {e}")
        except Exception as e:
            raise Exception(f"Error reading file '{self.input_file}': {e}")