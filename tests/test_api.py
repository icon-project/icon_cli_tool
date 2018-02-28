import os
import unittest
from icx import wallet

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestAPI(unittest.TestCase):
    """
    Test that execute the api about Wallet
    """

    def test_create_wallet_case0(self):
        """

        :return:
        """

        # Given

        # When
        ret = wallet.create_wallet(password="w3fasd", wallet_name="Avmasd", file_path=TEST_DIR)

        # Then
        self.assertEqual(0, ret)

    def test_create_wallet_case1(self):
        """

        :return:
        """
        # Given

        # When
        ret = wallet.create_wallet(password="1234", wallet_name="wname", file_path=TEST_DIR+'/non_exists_directory')

        # Then
        self.assertEqual(122, ret)

    def test_create_wallet_case2(self):
        """

                :return:
                """
        # Given

        # When
        ret = wallet.create_wallet(password="123 4", wallet_name="wname", file_path=TEST_DIR )

        # Then
        self.assertEqual(123, ret)

    def test_create_wallet_case3(self):
        """

                :return:
                """
        # Given

        # When
        ret = wallet.create_wallet(password="1234", wallet_name="wname", file_path=TEST_DIR+'/unaccessible')

        # Then
        self.assertEqual(136, ret)


if __name__ == "__main__":
    unittest.main()
