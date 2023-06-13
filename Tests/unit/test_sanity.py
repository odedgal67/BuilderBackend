import unittest

from Config import GLOBAL_CONFIG

GLOBAL_CONFIG.DB_ENABLED = False

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True, "Fail message")  # add assertion here

    def shortDescription(self) -> str | None:
        return "Unit test description to show in case of fail"


if __name__ == "__main__":
    unittest.main()
