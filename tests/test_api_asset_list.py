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
    Test that execute the api about asset list operation
    """

    def test_show_asset_list_case0(self):
        """Test for show_asset_list function.
         Case when show asset list successfully.

        """

        # Given
        password = "w3fasd"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:

            print(file_path)
            address, balance = icx.wallet.show_asset_list(password, file_path, url)
            print(address, balance)

            # Then
            prefix = address[0:2]
            self.assertEqual(prefix, "hx")

        except FileNotFoundError:
            self.assertFalse(True)

    def test_show_asset_list_case1(self):
        """Test for show_asset_list function.
        Case when user enters a directory that does not exist.
        """

        # Given
        password = "w3fasd"
        file_path = os.path.join(TEST_DIR, "unknown_folder", "test_keystore.txt")

        # When
        try:
            address, balance = icx.wallet.show_asset_list(password, file_path, url)

        # Then
        except icx.FilePathIsWrong:
            self.assertTrue(True)

    def test_show_asset_list_case2(self):
        """Test for show_asset_list function.
        Case when user enters a invalid password.
        """

        # Given
        password = "123 4"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            address, balance = icx.wallet.show_asset_list(password, file_path, url)

        # Then
        except icx.PasswordIsNotAcceptable:
            self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
