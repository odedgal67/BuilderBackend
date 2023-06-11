from abc import ABC, abstractmethod


class DTO(ABC):
    def to_json(self):
        attributes = vars(self)
        return {key: (str(value) if type(value) != int and type(value) != str else value) for key, value in attributes.items() if not key.startswith('__')}
