import os
from io import BytesIO
import uuid
import traceback

from Utils.Exceptions import IllegalFileTypeException


class FileSystemController:
    def __init__(self, directory: str):
        self.directory = directory

    def add_image(self, data, original_file_name: str):
        allowed_image_type = ['jpeg', 'png', 'bmp']
        return self.__add_file_of_type(data, original_file_name, allowed_image_type)

    def add_doc(self, data, original_file_name: str):
        allowed_docs_types = ['pdf']
        return self.__add_file_of_type(data, original_file_name, allowed_docs_types)

    def __get_file_type(self, original_file_name: str):
        file_type = original_file_name.rsplit('.', 1)
        if len(file_type) == 1:
            raise IllegalFileTypeException(original_file_name)
        else:
            return file_type[1]

    def __add_file_of_type(self, data, original_file_name: str, allowed_types: list[str]):
        file_type = self.__get_file_type(original_file_name)
        if file_type not in allowed_types:
            raise IllegalFileTypeException(original_file_name)
        return self.add_file(data, file_type)

    def add_file(self, data, file_type: str):
        new_file_name = str(uuid.uuid1()) + "." + file_type
        try:
            blob = BytesIO(data)
            if not os.path.isdir(self.directory):
                os.mkdir(self.directory)
            file_path = os.path.join(self.directory, new_file_name)
            with open(file_path, 'wb') as f:
                f.write(blob.getvalue())
            return new_file_name
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Error processing the file: {new_file_name}\n{str(e)}")
