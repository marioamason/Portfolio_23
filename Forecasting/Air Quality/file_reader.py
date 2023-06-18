class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
    
    def read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = file.read()
            return self.data
        except FileNotFoundError:
            print("File not found. Please provide the correct file path.")
            return None