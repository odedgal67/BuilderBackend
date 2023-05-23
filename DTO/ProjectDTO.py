from DTO.DTO import DTO
from Project import Project


class ProjectDTO(DTO):
    def __init__(self, project: Project):
        self.name = project.name
        self.id = project.id

    def to_json(self):
        return {
            'name': self.name,
            'id': self.id
        }
