import os
from io import BytesIO
import uuid
import traceback

from Utils.Exceptions import IllegalFileTypeException


class FileSystemController:
    def __init__(self, directory: str):
        self.directory = directory
        pass

    def add_file(self, data, original_file_name: str):
        file_type = original_file_name.rsplit('.', 1)
        if len(file_type) == 1:
            raise IllegalFileTypeException(original_file_name)
        file_type = file_type[1]
        new_file_name = str(uuid.uuid1()) + "." + file_type
        try:
            blob = BytesIO(data)
            if not not os.path.isfile(self.directory):
                os.mkdir(self.directory)
            file_path = os.path.join(self.directory, new_file_name)
            with open(file_path, 'wb') as f:
                f.write(blob.getvalue())
            return new_file_name
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Error processing the file: {new_file_name}\n{str(e)}")
