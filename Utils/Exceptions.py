# Custom Exceptions Implementations
import traceback


class KnownServerException(Exception):
    def __init__(self, *kwargs):
        traceback.print_exc()
        super().__init__(*kwargs)


class UserNotLoggedInException(KnownServerException):
    def __init__(self, username: str):
        self.username = username
        self.message = f"User {self.username} is not logged in"
        super().__init__(self.message)


class UsernameDoesntExistException(KnownServerException):
    def __init__(self, username: str):
        self.username = username
        self.message = f"Username {self.username} doesn't exist"
        super().__init__(self.message)


class ProjectDoesntExistException(KnownServerException):
    def __init__(self):
        self.message = f"Project name doesn't exist"
        super().__init__(self.message)


class TitleDoesntExistException(KnownServerException):
    def __init__(self):
        self.message = f"Title doesn't exist"
        super().__init__(self.message)


class StageDoesntExistException(KnownServerException):
    def __init__(self):
        self.message = f"Stage name doesn't exist"
        super().__init__(self.message)


class MissionDoesntExistException(KnownServerException):
    def __init__(self):
        self.message = f"Mission name doesn't exist"
        super().__init__(self.message)


class IllegalUsernameException(KnownServerException):
    def __init__(self, username: str):
        self.username = username
        self.message = f"Username {self.username} is invalid"
        super().__init__(self.message)


class IllegalProjectNameException(KnownServerException):
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.message = f"Project name {self.project_name} is invalid"
        super().__init__(self.message)


class IllegalStageNameException(KnownServerException):
    def __init__(self, stage_name: str):
        self.stage_name = stage_name
        self.message = f"Stage name {self.stage_name} is invalid"
        super().__init__(self.message)


class IllegalMissionNameException(KnownServerException):
    def __init__(self, mission_name: str):
        self.mission_name = mission_name
        self.message = f"Mission name {self.mission_name} is invalid"
        super().__init__(self.message)


class IllegalPlanNameException(KnownServerException):
    def __init__(self, plan_name: str):
        self.plan_name = plan_name
        self.message = f"Plan name {self.plan_name} is invalid"
        super().__init__(self.message)


class DuplicateUserName(KnownServerException):
    def __init__(self, username: str):
        self.username = username
        self.message = f"Username {self.username} already exists"
        super().__init__(self.message)


class DuplicatePlanNameException(KnownServerException):
    def __init__(self, plan_name: str):
        self.plan_name = plan_name
        self.message = f"Plan name {self.plan_name} already exists"
        super().__init__(self.message)


class DuplicateProjectNameException(KnownServerException):
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.message = f"Project {self.project_name} already exists"
        super().__init__(self.message)


class DuplicateStageNameException(KnownServerException):
    def __init__(self, stage_name: str):
        self.stage_name = stage_name
        self.message = f"Stage {self.stage_name} already exists"
        super().__init__(self.message)


class DuplicateMissionNameException(KnownServerException):
    def __init__(self, mission_name: str):
        self.mission_name = mission_name
        self.message = f"Mission {self.mission_name} already exists"
        super().__init__(self.message)


class DuplicateBuildingFaultException(KnownServerException):
    def __init__(self, build_fault_name: str):
        self.build_fault_name = build_fault_name
        self.message = f"Build Fault {self.build_fault_name} already exists"
        super().__init__(self.message)


class IllegalPasswordException(KnownServerException):
    def __init__(self):
        self.message = "Invalid password"
        super().__init__(self.message)


class IncorrectPasswordException(KnownServerException):
    def __init__(self):
        self.message = "Incorrect password"
        super().__init__(self.message)


class ApartmentNumberNotNeededException(KnownServerException):
    def __init__(self):
        self.message = "Apartment number is provided in a non apartment title"
        super().__init__(self.message)


class ChangeStatusNonEmptyStageException(KnownServerException):
    def __init__(self):
        self.message = "Cant change status for a stage that contains missions"
        super().__init__(self.message)


class ApartmentNotSpecifiedException(KnownServerException):
    def __init__(self):
        self.message = "Apartment number was not specified"
        super().__init__(self.message)


class ApartmentDoesntExistException(KnownServerException):
    def __init__(self):
        self.message = "Apartment number doesnt exist"
        super().__init__(self.message)


class PlanDoesntExistException(KnownServerException):
    def __init__(self):
        self.message = "Plan doesnt exist"
        super().__init__(self.message)


class BuildFaultDoesntExistException(KnownServerException):
    def __init__(self):
        self.message = "Build fault doesnt exist"
        super().__init__(self.message)


class AlreadyLoggedException(KnownServerException):
    def __init__(self, username: str):
        self.username = username
        self.message = f"{self.username} is already logged in"
        super().__init__(self.message)


class MissingUserID(KnownServerException):
    def __init__(self, user_id: int):
        self.user_Id = user_id
        super().__init__(f"Missing userid: {user_id}")


class IllegalFileTypeException(KnownServerException):
    def __init__(self, filename: str):
        super().__init__(f"file has illegal type: {filename}")


class IllegalLink(KnownServerException):
    def __init__(self, link: str):
        super().__init__(f"link doesn't have a valid format: {link}")


class UserPermissionError(KnownServerException):
    def __init__(self, msg: str = "Permission error"):
        super().__init__(msg)
