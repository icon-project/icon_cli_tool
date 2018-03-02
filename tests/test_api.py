import json
import os
import unittest

from icxcli import icx
from icxcli.icx import wallet,utils


TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestAPI(unittest.TestCase):
    """
    Test that execute the api about Wallet
    """

    def test_create_wallet_case0(self):
        """Test for create_wallet function.
        Case when created wallet successfully.
        """
        # Given
        password="w3fasd"
        wallet_name="Avmasd"
        file_path=os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            wallet_info = icx.wallet.create_wallet(password, wallet_name, file_path)

            # Then
            prefix = wallet_info.address[0:2]
            self.assertEqual(prefix, "hx")

        except icx.FilePathIsWrong:
            self.assertFalse(True)
        except icx.PasswordIsNotAcceptable:
            self.assertFalse(True)
        except icx.NoPermissionToWriteFile:
            self.assertFalse(True)

    def test_create_wallet_case1(self):
        """Test for create_wallet function.
        Case when user enters a directory that does not exist.
        """
        # Given
        password = "w3fasd"
        wallet_name = "wname"
        file_path=os.path.join(TEST_DIR,"unknown_folder" ,"test_keystore.txt")

        # When
        try:
            wallet_info = icx.wallet.create_wallet(password, wallet_name, file_path)

        # Then
        except icx.FilePathIsWrong:
            self.assertTrue(True)

    def test_create_wallet_case2(self):
        """Test for create_wallet function.
        Case when user enters a invalid password.
        """
        # Given
        password = "123 4"
        wallet_name = "wname"
        file_path=os.path.join(TEST_DIR,"unknown_folder" ,"test_keystore.txt")

        # When
        try:
            wallet_info = icx.wallet.create_wallet(password, wallet_name, file_path)

        # Then
        except icx.PasswordIsNotAcceptable:
            self.assertTrue(True)

    def test_create_wallet_case3(self):
        """Test for create_wallet function.
        Case when user enters a directory without permission to write file.
        """
        # Given
        password = "Adas2131231"
        wallet_name = "wname"
        file_path=os.path.join("/", "test_keystore.txt")

        # When
        try:
            wallet_info = icx.wallet.create_wallet(password, wallet_name, file_path)
        # Then
        except icx.NoPermissionToWriteFile:
            self.assertTrue(True)

    def test_created_store_key_file(self):
        """Check the file is saved in the correct format.
        """
        # Given
        password = "Adas2131231"
        wallet_name = "wname"
        file_path=os.path.join(TEST_DIR, "test_keystore.txt")

        # When
        try:
            wallet_info = icx.wallet.create_wallet(password, wallet_name, file_path)

        # Then
            self.assertTrue(utils.validate_key_store_file(file_path))
        except:
            self.assertTrue(False) # Never happen this case.

if __name__ == "__main__":
    unittest.main()
