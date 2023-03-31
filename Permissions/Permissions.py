from abc import ABC, abstractmethod


class AbstractPermission(ABC):
    @abstractmethod
    def register(self) -> bool:
        pass


class WorkManagerPermission(AbstractPermission):
    def register(self) -> bool:
        return False


class ProjectManagerPermission(WorkManagerPermission):
    def register(self) -> bool:
        return True


class ContractorPermission(ProjectManagerPermission):
    pass
