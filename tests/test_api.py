import json
import os
import unittest

from icxcli.icx import wallet
from icxcli.icx import utils
from icxcli.icx import ErrorCode

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

        # When
        ret = wallet.create_wallet(password="w3fasd", wallet_name="Avmasd", file_path=TEST_DIR + '/')

        # Then
        self.assertEqual(ErrorCode.SUCCEED, ret)

    def test_create_wallet_case1(self):
        """Test for create_wallet function.
        Case when user enters a directory that does not exist.
        """
        # Given

        # When
        ret = wallet.create_wallet(password="1234", wallet_name="wname", file_path='/non_exists_directory')

        # Then
        self.assertEqual(ErrorCode.FILE_PATH_IS_WRONG, ret)

    def test_create_wallet_case2(self):
        """Test for create_wallet function.
        Case when user enters a invalid password.
        """
        # Given

        # When
        ret = wallet.create_wallet(password="123 4", wallet_name="wname", file_path=TEST_DIR)

        # Then
        self.assertEqual(ErrorCode.PASSWORD_IS_WRONG, ret)

    def test_create_wallet_case3(self):
        """Test for create_wallet function.
        Case when user enters a directory that she does not have write permission to.
        """
        # Given

        # When
        ret = wallet.create_wallet(password="1234", wallet_name="wname", file_path='/')

        # Then
        self.assertEqual(ErrorCode.NO_PERMISSION_TO_WRITE_FILE, ret)

    def test_created_store_key_file(self):
        """Check the file is saved in the correct format.
        """
        # Given
        # When

        key_store_contents = wallet.make_key_store_content("yourpassword")

        json_string = json.dumps(key_store_contents)

        file_path = TEST_DIR + "/"

        wallet.store_wallet(file_path, json_string)
        ret = utils.validate_key_store_file(file_path+'file.txt')

        self.assertTrue(ret)

if __name__ == "__main__":
    unittest.main()
