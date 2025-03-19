class FileWriter:
    def __init__(self, file_name):
        self.file_name = file_name

    def file_write(self, content):
        try:
            with open(self.file_name, 'r+') as file:
                file.write(content)
            return f"content written to {self.file_name} successfully"
        except Exception as e:
            return f"An error occurred:{e}"