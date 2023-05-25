from DTO.DTO import DTO
from User import User


class UserDTO(DTO):
    def __init__(self, user: User):
        self.username: str = user.username
        self.logged_in: bool = user.logged_in
        self.name = user.name

    def to_json(self):
        return {
            'username': self.username,
            'logged_in': self.logged_in,
            'name': self.name
        }
