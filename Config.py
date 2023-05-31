from abc import ABC
from dataclasses import dataclass
import sys


@dataclass(init=True, repr=True)
class AbstractConfig(ABC):
    SERVER_FILE_DIRECTORY: str
    DATABASE_ENABLED: bool
    IP: str
    PORT: int

    def __post_init__(self):
        if self.IP is None:
            self.IP = "0.0.0.0"
        if self.PORT is None:
            self.PORT = 80


@dataclass()
class RemoteConfig(AbstractConfig):
    def __init__(self):
        super().__init__(SERVER_FILE_DIRECTORY="/home/ec2-user/server_files", DATABASE_ENABLED=False, IP=None,
                         PORT=None)


@dataclass()
class LocalConfig(AbstractConfig):
    def __init__(self):
        super().__init__(SERVER_FILE_DIRECTORY="server_files", DATABASE_ENABLED=False, IP=None, PORT=None)


GLOBAL_CONFIG = LocalConfig() if sys.platform.startswith('win') else RemoteConfig()
