import os
import unittest

from icxcli.icx.utils import get_tx_hash, sign
from icxcli.icx import wallet, FilePathIsWrong, PasswordIsWrong, NoEnoughBalanceInWallet, TransferFeeIsInvalid, \
    AddressIsWrong, FeeIsBiggerThanAmount, AmountIsInvalid, AddressIsSame, AmountOrFeeIsNotInteger
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
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        # When
        try:
            ret = bool(wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hxa974f512a510299b53c55535c105ed962fd01ee2",
                amount="1000000000000000000", file_path=file_path, url=url))

            # Then
            self.assertEqual(True, ret)

        except FileNotFoundError:
            self.assertFalse(True)

    def test_transfer_case0_0(self):
        """Test for transfer_value_with_the_fee function.
         Case when transfer 0.1(float) value to a wallet.
        """

        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        # When
        try:
            ret = bool(wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hxa974f512a510299b53c55535c105ed962fd01ee2",
                amount="10000000000000000.755", file_path=file_path, url=url))

            # Then
            self.assertEqual(False, ret)

        except AmountOrFeeIsNotInteger:
            self.assertTrue(True)


    def test_transfer_case1(self):
        """Test for transfer_value_with_the_fee function.
        Case when key_store_file_path is wrong.
        """
        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        # When
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hxa974f512a510299b53c55535c105ed962fd01ee2",
                amount="10000000000000000000", file_path='./wrong_path', url=url)
            # Then

        except FilePathIsWrong:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

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
                password, 10000000000000000, to="hxa974f512a510299b53c55535c105ed962fd01ee2",
                amount="1000000000000000000", file_path=file_path, url=url)
            # Then

        except PasswordIsWrong:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_transfer_case3(self):
        """Test for transfer_value_with_the_fee function.
        Case when wallet does not have enough balance.
        """
        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        # When
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hxa974f512a510299b53c55535c105ed962fd01ee2",
                amount="10000000000000000000000000000000000000000000000000", file_path=file_path, url=url)
            # Then

        except NoEnoughBalanceInWallet:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_transfer_case4(self):
        """Test for transfer_value_with_the_fee function.
        Case when transfer fee is invalid.
        """
        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        # When
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 100000000000, to="hxa974f512a510299b53c55535c105ed962fd01ee2",
                amount="1000000000000000000", file_path=file_path, url=url)
            # Then

        except TransferFeeIsInvalid:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_transfer_case5(self):
        """Test for transfer_value_with_the_fee function.
        Case when wallet address is wrong.
        """
        # Given
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        # When
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hxa974f512a510299b53c55535c105ed9",
                amount="1000000000000000000", file_path=file_path, url=url)
            # Then

        except AddressIsWrong:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_transfer_case6(self):
        """Test for transfer_value_with_the_fee function.
        Case when Fee is not 10000000000000000.
        """
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        print()

        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 100000000000000, to="hxa974f512a510299b53c55535c105ed962fd01ee2",
                amount="11234440000000000000", file_path=file_path, url=url)

        except TransferFeeIsInvalid:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_transfer_case7(self):
        """Test for transfer_value_with_the_fee function.
        Case when Fee is bigger than Amount.
        """

        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hxa974f512a510299b53c55535c105ed962fd01ee2",
                amount="1000000000000000", file_path=file_path, url=url)

        except FeeIsBiggerThanAmount:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_transfer_case8(self):
        """Test for transfer_value_with_the_fee function.
        Case when Amount is 0.
        """
        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hxa974f512a510299b53c55535c105ed962fd01ee2",
                amount="0", file_path=file_path, url=url)

        except AmountIsInvalid:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_transfer_case9(self):
        """Test for transfer_value_with_the_fee function.
        Case when balance is same as sum of Amount and Fee.
        """

        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")

        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hx95e12b1f98f9b847175849f51bed5d121e742f6a",
                amount="1020000000000000000", file_path=file_path, url=url)

            password = "Adas21312**"
            file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer2.txt")
            ret = wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hx66425784bfddb5b430136b38268c3ce1fb68e8c5",
                amount="1000000000000000000", file_path=file_path, url=url)

        except AmountIsInvalid:
            self.assertTrue(False)
        else:
            self.assertTrue(True)

    def test_transfer_case10(self):
        """Test for transfer_value_with_the_fee function.
        Case when wallet address to transfer is same as wallet address to be sent.
        """

        password = "ejfnvm1234*"
        file_path = os.path.join(TEST_DIR, "test_keystore_for_transfer.txt")
        try:
            ret = wallet.transfer_value_with_the_fee(
                password, 10000000000000000, to="hx66425784bfddb5b430136b38268c3ce1fb68e8c5",
                amount="0", file_path=file_path, url=url)

        except AddressIsSame:
            self.assertTrue(True)
        else:
            self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()
