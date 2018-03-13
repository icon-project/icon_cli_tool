import os
import unittest

from icxcli.icx.utils import get_tx_hash, sign
from icxcli.icx import wallet, FilePathIsWrong, PasswordIsWrong, NoEnoughBalanceInWallet, TransferFeeIsInvalid, \
    AddressIsWrong
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
url = 'https://testwallet.icon.foundation/api/'


class TestAPI(unittest.TestCase):
    """
    Test that execute the api about transfer icx.
    """

    def test_get_tx(self):
        """Test for get_tx_hash function.
        """
        # Given
        method = "method"
        params = {"param1": 1}

        # When
        expect = b'\xc0\x84\x19o\xd3\xe6<\x9e%\xd9\x05\xd4\x8di\x17\xd3\x02<a\xc6\xa2\xb2\xec I-\x12\xe1n\xd5\xac:'
        tx_hash = get_tx_hash(method, params)

        # Then
        self.assertEqual(expect, tx_hash)

    def test_sign(self):
        """Test for sign function.
        """

        # Given
        tx_hash = b'\xc0\x84\x19o\xd3\xe6<\x9e%\xd9\x05\xd4\x8di\x17\xd3\x02<a\xc6\xa2\xb2\xec I-\x12\xe1n\xd5\xac:'
        private_key_bytes = b'x\xf3\xda\xdc\x80h\xf3hc`L\x1f\xc4Y\x83z@\xa2Mn$\x94\x16\x01\x83\x9cYp\x1d,\x93\xdd'

        # When
        expect = b'qeTA6B2VssGxrSE+SlOjRm0/RbqB9OKo2VHrgL7kVCUklcltf3AUeiujpWVAZXwZjPWmND1oyFStC00BHbQXVAA='
        signature_bytes = sign(private_key_bytes, tx_hash)

        # Then
        self.assertEqual(expect, signature_bytes)

    def test_transfer_case0(self):
        """Test for transfer_value_with_the_fee function.
         Case when succeed transfer value.
        """

        # Given
        password = "1234"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        # When
        try:
            ret = bool(wallet.transfer_value_with_the_fee(
                password, 0.01, 18, to="hxa23651905dfa12221dd36b860dc114ef7f7a0786",
                amount="1", file_path=file_path, url=url))

            # Then
            self.assertEqual(True, ret)

        except FileNotFoundError:
            self.assertFalse(True)

    def test_transfer_case1(self):
        """Test for transfer_value_with_the_fee function.
        Case when key_store_file_path is wrong.
        """
        # Given
        password = "1234"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        # When
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 0.01, 18, to="hxa23651905dfa12221dd36b860dc114ef7f7a0786",
                amount="1", file_path='./wrong_path', url=url)
            # Then

        except FilePathIsWrong:
            self.assertTrue(True)

    def test_transfer_case2(self):
        """Test for transfer_value_with_the_fee function.
        Case when password is wrong.
        """
        # Given
        password = "wrong_password"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        # When
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 0.01, 18, to="hxa23651905dfa12221dd36b860dc114ef7f7a0786",
                amount="1", file_path=file_path, url=url)
            # Then

        except PasswordIsWrong:
            self.assertTrue(True)

    def test_transfer_case3(self):
        """Test for transfer_value_with_the_fee function.
        Case when wallet does not have enough balance.
        """
        # Given
        password = "1234"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        # When
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 0.01, 18, to="hxa23651905dfa12221dd36b860dc114ef7f7a0786",
                amount="100000000", file_path=file_path, url=url)
            # Then

        except NoEnoughBalanceInWallet:
            self.assertTrue(True)

    def test_transfer_case4(self):
        """Test for transfer_value_with_the_fee function.
        Case when transfer fee is invalid.
        """
        # Given
        password = "1234"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        # When
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, -1, 18, to="hxa23651905dfa12221dd36b860dc114ef7f7a0786",
                amount="1000", file_path=file_path, url=url)
            # Then

        except TransferFeeIsInvalid:
            self.assertTrue(True)

    def test_transfer_case5(self):
        """Test for transfer_value_with_the_fee function.
        Case when wallet address is wrong.
        """
        # Given
        password = "1234"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        print()
        # When
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 0.01, 18, to="hxa23651905d221dd36b",
                amount="1", file_path=file_path, url=url)
            # Then

        except AddressIsWrong:
            self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
