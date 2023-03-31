# Custom Exceptions Implementations


class UsernameDoesntExistException(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"Username {self.username} doesn't exist"
        super().__init__(self.message)


class IllegalUsernameException(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"Username {self.username} is invalid"
        super().__init__(self.message)


class DuplicateUserName(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"Username {self.username} already exists"
        super().__init__(self.message)


class IllegalPasswordException(Exception):
    def __init__(self):
        self.message = "Invalid password"
        super().__init__(self.message)


class IncorrectPasswordException(Exception):
    def __init__(self):
        self.message = "Incorrect password"
        super().__init__(self.message)


class AlreadyLoggedException(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"{self.username} is already logged in"
        super().__init__(self.message)


class MissingUserID(Exception):
    def __init__(self, user_id: int):
        self.user_Id = user_id
        super().__init__(f"Missing userid: {user_id}")
