import os
import unittest
from icxcli import icx
from icxcli.icx import wallet, utils

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
         Case when returning the wallet address successfully.

        """

        # Given
        password = "Adas21312**"
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
        password = "Adas21312**"
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
        password = "wrongPassword123**"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            address, balance = icx.wallet.show_asset_list(password, file_path, url)

        # Then
        except icx.PasswordIsWrong:
            self.assertTrue(True)

    def test_change_hex_balance_to_decimal_balance_case1(self):
        """Test for change_hex_balance_to_decimal_balance function.
        Case when returning the right balance.

        """

        # Given
        hex_balance = '0x10e8205bae65f770000'
        dec_balance = '4989.990000000000000000'

        # When
        try:
            result_dec_balance = utils.change_hex_balance_to_decimal_balance(hex_balance)
            self.assertEqual(result_dec_balance, dec_balance)
        finally:
            pass

    def test_change_hex_balance_to_decimal_balance_case2(self):
        """Test for change_hex_balance_to_decimal_balance function.
        Case when returning the wrong balance.

        """

        # Given
        hex_balance = '0x10e8205bae65f770000'
        dec_balance = '4989.9900000000000001235'

        # When
        try:
            result_dec_balance = utils.change_hex_balance_to_decimal_balance(hex_balance)
            self.assertNotEqual(result_dec_balance, dec_balance)
        finally:
            pass

    def test_show_asset_list_case3(self):
        """Test for show_asset_list function.
         Case when show asset list's balance successfully.

        """

        # Given
        password = "Adas21312**"
        file_path = os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            address, balance = icx.wallet.show_asset_list(password, file_path, url)
            self.assertTrue(type(balance) == str)
        finally:
            pass


if __name__ == "__main__":
    unittest.main()
