import unittest
import random
import string
from typing import Callable

from Facade import Facade


class AcceptanceBase(unittest.TestCase):
    lastUserID = 0

    @classmethod
    def setUpClass(cls):
        cls.facade: Facade = Facade()

    @classmethod
    def assertNotThrows(cls, message: str, func: Callable, *kwargs):
        try:
            return func(*kwargs)
        except Exception as e:
            cls.fail(self=cls, msg=message)

    @classmethod
    def _get_user_name(self) -> str:
        output = str(self.lastUserID)
        while len(output) < 9:
            output = "0" + output
        self.lastUserID += 1
        return output

    @classmethod
    def generate_password(self) -> str:
        length = random.randint(8, 20)

        # Generate at least one uppercase letter, one lowercase letter, and one digit
        password = random.choice(string.ascii_uppercase)
        password += random.choice(string.ascii_lowercase)
        password += random.choice(string.digits)

        # Generate the remaining characters
        remaining_length = length - 3
        password += "".join(
            random.choices(string.ascii_letters + string.digits, k=remaining_length)
        )

        # Shuffle the password characters to make it more random
        password = "".join(random.sample(password, len(password)))

        return password

    @classmethod
    def registerUserAndLogin(self, amount: int) -> list[str]:
        output = []
        while len(output) < amount:
            curr_username = self._get_user_name()
            curr_password = self.generate_password()
            self.assertNotThrows(
                "failed to setup test, couldn't register the users!",
                self.facade.register,
                curr_username,
                curr_password,
            )
            self.assertNotThrows(
                "failed to setup test, couldn't login the users!",
                self.facade.login,
                curr_username,
                curr_password,
            )
            output.append(curr_username)
        return output


if __name__ == "__main__":
    unittest.main()
