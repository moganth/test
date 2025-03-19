from file_reader import FileReader
from file_writer import FileWriter

class FileConvertor:
    def __init__(self, input_file, output_file, input_format, output_format):
        if input_format.lower() == output_format.lower():
            raise ValueError("Input and output formats are the same. No conversion needed.")
        self.reader = FileReader(input_file, input_format)
        self.writer = FileWriter(output_file, output_format)

    def convert(self):
        data = self.reader.read_file()
        if data is not None:
            self.writer.write_file(data)