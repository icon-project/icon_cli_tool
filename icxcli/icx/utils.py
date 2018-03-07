#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 theloop Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import base64
import hashlib
import re

import eth_keyfile
import time

from icxcli.icx import IcxSigner, WalletAddressIsInvalid


def validate_password(password) -> bool:
    """Verify the entered password.

    :param password: The password the user entered. type(str)
    :return: bool
    True: When the password is valid format
    False: When the password is invalid format
    """
    password_regular_expression = re.compile(r'[a-zA-Z0-9\'";:/.,<>?!@#$%^&*()_+=-\]\\[{}]+$')
    return bool(password_regular_expression.match(password))


def hex_to_bytes(value):
    return bytes.fromhex(value)


def bytes_to_hex(value):
    return value.hex()


def get_timestamp_us():
    """Get epoch time in us.
    """
    return int(time.time() * 10 ** 6)


def icx_to_wei(icx):
    """Convert amount in icx unit to wei unit.

    Args:
        icx(float): float value in icx unit

    Returns:
        int: int value in wei unit
    """
    return int(icx * 10 ** 18)


def validate_address(address) -> bool:
    try:
        int(address, 16)
        if len(address) == 42:
            return True
        raise WalletAddressIsInvalid
    except ValueError:
        raise WalletAddressIsInvalid


def validate_key_store_file(key_store_file_path: object) -> bool:
    """Check key_store file was saved in the correct format.

    :return: bool
    True: When the key_store_file was saved in valid format.
    False: When the key_store_file was saved in invalid format.
    """
    is_valid = True

    # The key values ​​that should be in the root location.
    root_keys = ["version", "id", "address", "crypto"]
    crypto_keys = ["ciphertext", "cipherparams", "cipher", "kdf", "kdfparams", "mac"]
    crypto_cipherparams_keys = ["iv"]
    crypto_kdfparams_keys = ["dklen", "salt", "c", "prf"]

    keyfile = eth_keyfile.load_keyfile(key_store_file_path)
    is_valid = has_keys(keyfile, root_keys) and has_keys(keyfile["crypto"], crypto_keys) and has_keys(keyfile["crypto"]["cipherparams"], crypto_cipherparams_keys) and has_keys(keyfile["crypto"]["kdfparams"], crypto_kdfparams_keys)
    return is_valid


def has_keys(data, key_array):
    for key in key_array:
        if key in data is False:
            return False
    return True


def sha3_256(data):
    """Get hash value using sha3_256 hash function

    Args:
        data(bytes): data to hash

    Returns:
        bytes: 256bit hash value (32 bytes)
    """
    return hashlib.sha3_256(data).digest()


def get_address_by_privkey(privkey_bytes):
    """Get address by Private key.

    Args:
        privkey(str): hex string without '0x'
    """
    account = IcxSigner.from_bytes(privkey_bytes)
    return f'hx{bytes_to_hex(account.address)}'


def get_tx_hash(method, params):
    """Create tx_hash from params object.

    Args:
        params(dict): the value of 'params' key in jsonrpc
        method(str): Method name.

    Returns:
        bytes: sha3_256 hash value
    """
    tx_phrase = get_tx_phrase(method, params)
    return sha3_256(tx_phrase.encode())


def get_tx_phrase(method, params):
    """Create tx phrase from method and params.
    tx_phrase means input text to create tx_hash.

    Args:
        params(dict): The value of 'params' key in jsonrpc
        method(str): Method name.
    Returns:
        str: sha3_256 hash format without '0x' prefix
    """
    keys = [key for key in params]

    key_count = len(keys)
    if key_count == 0:
        return method

    phrase = get_params_phrase(params)

    return f'{method}.{phrase}'


def get_params_phrase(params):
    """Create params phrase recursively
    """
    keys = [key for key in params]
    keys.sort()
    key_count = len(keys)
    if key_count == 0:
        return ""
    phrase = ""

    if isinstance(params[keys[0]], dict) is not True:
        phrase += f'{keys[0]}.{params[keys[0]]}'
    elif bool(params[keys[0]]) is not True:
        phrase += f'{keys[0]}'
    else:
        phrase += f'{keys[0]}.{get_params_phrase(params[keys[0]])}'

    for i in range(1, key_count):
        key = keys[i]

        if isinstance(params[key], dict) is not True:
            phrase += f'.{key}.{params[key]}'
        elif bool(params[key]) is not True:
            phrase += f'.{key}'
        else:
            phrase += f'.{key}.{get_params_phrase(params[key])}'

    return phrase


def sign_recoverable(private_key_bytes, tx_hash_bytes):
    """
    Args:
        tx_hash_bytes: 32byte tx_hash data. type(bytes)
        private_key_bytes:

    Returns:
        bytes: signature_bytes + recovery_id(1)
    """
    signer = IcxSigner.from_bytes(private_key_bytes)
    signature_bytes, recovery_id = signer.sign_recoverable(tx_hash_bytes)

    # append recover_id(1 byte) to signature_bytes.
    return bytes(bytearray(signature_bytes) + recovery_id.to_bytes(1, 'big'))


def sign(private_key_bytes, tx_hash_bytes):
    """
    Args:
        private_key_bytes(bytes)
        tx_hash_bytes(bytes)

    Returns:
        str: base64-encoded string of recoverable signature data
    """
    recoverable_sig_bytes = sign_recoverable(private_key_bytes, tx_hash_bytes)
    return base64.b64encode(recoverable_sig_bytes)


def create_jsonrpc_request_content(_id, method, params):
    content = {
        'jsonrpc': '2.0',
        'method': method,
        'id': _id
    }

    if params is not None:
        content['params'] = params

    return content
