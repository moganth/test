class FileReader:
    def __init__(self,file_name):
        self.file_name = file_name

    def file_read(self):
        try:
            with open(self.file_name, 'r') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            return f"Error:{self.file_name} not found"
        except Exception as e:
            return f"An error occured: {e}"