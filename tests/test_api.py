import unittest
from cmd import cmd


class TestAPI(unittest.TestCase):
    """
    Test that execute the api about Wallet
    """

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')


if __name__ == "__main__":
    unittest.main()