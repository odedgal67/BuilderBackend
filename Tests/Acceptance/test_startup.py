import unittest

from Facade import Facade
from Tests.Acceptance.acceptance_base import AcceptanceBase


liron_username = "123456789"
liron_password = "123qweasd"


class Startup(AcceptanceBase):
    def test_liron_exists(self):
        self.assertNotThrows(
            "liron is not registered in the system",
            self.facade.login,
            liron_username,
            liron_password,
        )
        self.facade.login(liron_username, liron_password)


if __name__ == "__main__":
    unittest.main()
