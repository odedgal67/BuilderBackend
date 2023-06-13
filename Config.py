from abc import ABC
from dataclasses import dataclass
import configparser
import sys

@dataclass(init=True, repr=True)
class AbstractConfig(ABC):
    SERVER_FILE_DIRECTORY: str
    IP: str = None
    PORT: int = None
    SECRET_CONFIG: dict = None
    LIRON_ID: str = None
    MONGO_URL: str = "mongodb://localhost:27017"
    DB_NAME: str = "Builder"
    COLLECTION_NAME: str = "builder"
    SECRET_CONFIG_FILE_PATH: str = "config_example.ini"

    def __post_init__(self):
        config_obj = configparser.ConfigParser()
        config_obj.read(self.SECRET_CONFIG_FILE_PATH)
        self.SECRET_CONFIG = config_obj['Credentials']
        self.DB_ENABLED = config_obj['DB']['enabled'] == 'True'
        if self.IP is None:
            self.IP = "0.0.0.0"
        if self.PORT is None:
            self.PORT = 80


@dataclass()
class RemoteConfig(AbstractConfig):
    def __init__(self):
        super().__init__(SERVER_FILE_DIRECTORY="/home/ec2-user/server_files",
                         MONGO_URL="mongodb+srv://odedgal67:o95r88i84D@cluster0.qesnyur.mongodb.net/")


@dataclass()
class DebugConfig(AbstractConfig):
    def __init__(self):
        super().__init__(SERVER_FILE_DIRECTORY="server_files", MONGO_URL="mongodb+srv://odedgal67:o95r88i84D@cluster0.qesnyur.mongodb.net/")


@dataclass()
class LocalConfig(AbstractConfig):
    def __init__(self):
        super().__init__(SERVER_FILE_DIRECTORY="server_files")


GLOBAL_CONFIG = DebugConfig()
