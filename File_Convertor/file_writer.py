from dicttoxml import dicttoxml
import json
import yaml

class FileWriter:
    def __init__(self, output_file, output_format):
        self.output_file = output_file
        self.output_format = output_format.lower()

    def write_file(self, data):
        try:
            with open(self.output_file, "w") as file:
                if self.output_format == "json":
                    json.dump(data, file, indent=4)
                elif self.output_format == "yaml":
                    yaml.dump(data, file)
                elif self.output_format == "xml":
                    xml_data = dicttoxml(data, custom_root='root', attr_type=False).decode()
                    file.write(xml_data)
                else:
                    raise ValueError("Unsupported output format")
        except Exception as e:
            raise Exception(f"Error writing to file '{self.output_file}': {e}")

