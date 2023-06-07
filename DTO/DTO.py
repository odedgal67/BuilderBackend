from abc import ABC, abstractmethod


class DTO(ABC):
    def to_json(self):
        attributes = vars(self)
        return {key: value for key, value in attributes.items() if not key.startswith('__')}
