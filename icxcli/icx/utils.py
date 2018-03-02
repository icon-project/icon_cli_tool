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
import re
import eth_keyfile


def validate_password(password) -> bool:
    """Verify the entered password.

    :param password(str): The password the user entered.
    :return: bool
    True: When the password is valid format
    False: When the password is invalid format
    """
    password_regular_expression = re.compile(r'[a-zA-Z0-9\'";:/.,<>?!@#$%^&*()_+=-\]\\[{}]+$')
    return bool(password_regular_expression.match(password))


def hex_to_bytes(value):
    return bytes.fromhex(value)


def validate_key_store_file(key_store_file_path: object) -> bool:
    """Check key_store file was saved in the correct format.

    :param(str) Key_store_file_path.
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
