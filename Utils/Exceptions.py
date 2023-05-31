# Custom Exceptions Implementations


class UserNotLoggedInException(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"User {self.username} is not logged in"
        super().__init__(self.message)


class UsernameDoesntExistException(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"Username {self.username} doesn't exist"
        super().__init__(self.message)


class ProjectDoesntExistException(Exception):
    def __init__(self):
        self.message = f"Project name doesn't exist"
        super().__init__(self.message)


class TitleDoesntExistException(Exception):
    def __init__(self):
        self.message = f"Title doesn't exist"
        super().__init__(self.message)


class StageDoesntExistException(Exception):
    def __init__(self):
        self.message = f"Stage name doesn't exist"
        super().__init__(self.message)


class MissionDoesntExistException(Exception):
    def __init__(self):
        self.message = f"Mission name doesn't exist"
        super().__init__(self.message)


class IllegalUsernameException(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"Username {self.username} is invalid"
        super().__init__(self.message)


class IllegalProjectNameException(Exception):
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.message = f"Project name {self.project_name} is invalid"
        super().__init__(self.message)


class IllegalStageNameException(Exception):
    def __init__(self, stage_name: str):
        self.stage_name = stage_name
        self.message = f"Stage name {self.stage_name} is invalid"
        super().__init__(self.message)


class IllegalMissionNameException(Exception):
    def __init__(self, mission_name: str):
        self.mission_name = mission_name
        self.message = f"Mission name {self.mission_name} is invalid"
        super().__init__(self.message)


class DuplicateUserName(Exception):
    def __init__(self, username: str):
        self.username = username
        self.message = f"Username {self.username} already exists"
        super().__init__(self.message)


class DuplicateProjectNameException(Exception):
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.message = f"Project {self.project_name} already exists"
        super().__init__(self.message)


class DuplicateStageNameException(Exception):
    def __init__(self, stage_name: str):
        self.stage_name = stage_name
        self.message = f"Stage {self.stage_name} already exists"
        super().__init__(self.message)


class DuplicateMissionNameException(Exception):
    def __init__(self, mission_name: str):
        self.mission_name = mission_name
        self.message = f"Mission {self.mission_name} already exists"
        super().__init__(self.message)


class DuplicateBuildingFaultException(Exception):
    def __init__(self, build_fault_name: str):
        self.build_fault_name = build_fault_name
        self.message = f"Build Fault {self.build_fault_name} already exists"
        super().__init__(self.message)


class IllegalPasswordException(Exception):
    def __init__(self):
        self.message = "Invalid password"
        super().__init__(self.message)


class IncorrectPasswordException(Exception):
    def __init__(self):
        self.message = "Incorrect password"
        super().__init__(self.message)


class ApartmentNumberNotNeededException(Exception):
    def __init__(self):
        self.message = "Apartment number is provided in a non apartment title"
        super().__init__(self.message)


class ChangeStatusNonEmptyStageException(Exception):
    def __init__(self):
        self.message = "Cant change status for a stage that contains missions"
        super().__init__(self.message)


class ApartmentNotSpecifiedException(Exception):
    def __init__(self):
        self.message = "Apartment number was not specified"
        super().__init__(self.message)


class ApartmentDoesntExistException(Exception):
    def __init__(self):
        self.message = "Apartment number doesnt exist"
        super().__init__(self.message)


class BuildFaultDoesntExistException(Exception):
    def __init__(self):
        self.message = "Build fault doesnt exist"
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

class IllegalFileTypeException(Exception):
    def __init__(self, filename: str):
        super().__init__(f"file has illegal type: {filename}")
