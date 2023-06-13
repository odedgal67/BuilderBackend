from abc import ABC
from uuid import UUID


class DTO(ABC):
    def to_json(self):
        attributes = vars(self)
        return {key: (value if type(value) != UUID else str(value)) for key, value in attributes.items() if not key.startswith('__')}
