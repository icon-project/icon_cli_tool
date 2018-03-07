import os
import unittest

from icxcli.icx.utils import get_tx_hash, sign

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


class TestAPI(unittest.TestCase):
    """
    Test that execute the api about transfer icx.
    """

    def test_get_tx(self):

        # Given
        method = "method"
        params = {"param1": 1}

        # When
        expect = b'\xc0\x84\x19o\xd3\xe6<\x9e%\xd9\x05\xd4\x8di\x17\xd3\x02<a\xc6\xa2\xb2\xec I-\x12\xe1n\xd5\xac:'
        tx_hash = get_tx_hash(method, params)

        # Then
        self.assertEqual(expect, tx_hash)

    def test_sign(self):

        # Given
        tx_hash = b'\xc0\x84\x19o\xd3\xe6<\x9e%\xd9\x05\xd4\x8di\x17\xd3\x02<a\xc6\xa2\xb2\xec I-\x12\xe1n\xd5\xac:'
        private_key_bytes = b'x\xf3\xda\xdc\x80h\xf3hc`L\x1f\xc4Y\x83z@\xa2Mn$\x94\x16\x01\x83\x9cYp\x1d,\x93\xdd'

        # When
        expect = b'qeTA6B2VssGxrSE+SlOjRm0/RbqB9OKo2VHrgL7kVCUklcltf3AUeiujpWVAZXwZjPWmND1oyFStC00BHbQXVAA='
        signature_bytes = sign(private_key_bytes, tx_hash)

        # Then
        self.assertEqual(expect, signature_bytes)


if __name__ == "__main__":
    unittest.main()
