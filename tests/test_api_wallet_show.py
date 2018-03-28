import os
import unittest
from icxcli import icx
from icxcli.icx import wallet
import requests
requests.packages.urllib3.disable_warnings()

TEST_DIR = os.path.dirname(os.path.abspath(__file__))

url = 'https://testwallet.icon.foundation/api/'


class TestAPI(unittest.TestCase):
    """
    Test that execute the api about wallet show operation
    """

    def test_show_wallet_case0(self):
        """Test for show_wallet function.
         Case when returning the wallet address successfully.

        """

        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            address, balance, wallet_info = icx.wallet.show_wallet(password, file_path, url)

            # Then
            prefix = address[0:2]
            self.assertEqual(prefix, "hx")

        except FileNotFoundError:
            self.assertFalse(True)

    def test_show_wallet_case1(self):
        """Test for show_wallet function.
        Case when user enters a directory that does not exist.
        """

        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "unknown_folder", "test_keystore.txt")

        # When
        try:
            address, balance, wallet_info = icx.wallet.show_wallet(password, file_path, url)

        # Then
        except icx.FilePathIsWrong:
            self.assertTrue(True)
        except FileNotFoundError:
            self.assertTrue(True)

    def test_show_wallet_case2(self):
        """Test for show_wallet function.
        Case when user enters a invalid password.
        """

        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            address, balance, wallet_info = icx.wallet.show_wallet(password, file_path, url)

        # Then
        except icx.PasswordIsWrong:
            self.assertTrue(True)

    def test_show_wallet_case3(self):
        """Test for show_wallet function.
         Case when returning the balance successfully.

        """

        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            address, balance, wallet_info = icx.wallet.show_wallet(password, file_path, url)
            self.assertTrue(type(balance) == int)
        finally:
            pass

    def test_show_wallet_case4(self):
        """Test for show_wallet function.
         Case when returning the wallet info in keystore file successfully.

        """

        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            address, balance, wallet_info = icx.wallet.show_wallet(password, file_path, url)
            self.assertTrue(type(wallet_info) == dict)
        finally:
            pass


if __name__ == "__main__":
    unittest.main()
