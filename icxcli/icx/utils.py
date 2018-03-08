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
import requests


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


def create_jsonrpc_request_content(_id, method, params):
    content = {
        'jsonrpc': '2.0',
        'method': method,
        'id': _id
    }

    if params is not None:
        content['params'] = params

    return content


def post(url, payload):
    return requests.post(url, json=payload, verify=False)


def make_payload_for_get_balance(address, url):

    url = f'{url}v2'

    method = 'icx_getBalance'
    params = {'address': address}
    payload = create_jsonrpc_request_content(0, method, params)
    return payload


def check_balance_enough(balance, amount, fee):
    """Check if the user has enough balance to transfer.

    :param balance: Balance of the user's wallet.
    :param amount: Amount of money. type(str)
    :param fee: Transfer fee.
    :return:
    True when the user has enough balance.
    """
    if balance > float(amount) + fee:
        return True
    else:
        raise NoEnoughBalanceInWallet
    pass


def floor_point(amount_wei, decimal_point):
    """To process up to 'decimal_point' decimal places, change it backwards to 0 by (18-decimal_point).

    :param amount_wei: Wei value of amount. type(int)
    :param decimal_point: A user can change the decimal point to express all numbers including fee and amount.
    :return:
    """
    str_amount = str(amount_wei)
    if len(str_amount) < 18:
        return amount_wei
    if decimal_point == 18:
        return amount_wei
    return f'{str_amount[0:-(18-decimal_point)]}{"0"*(18-decimal_point)}'


def change_hex_balance_to_decimal_balance(hex_balance, place=18):
    """Change hex balance to decimal decimal icx balance
    :param: hex_balance
    :return: result_decimal_icx: string decimal icx
    """
    dec_balance = int(hex_balance, 16)
    str_dec_balance = str(dec_balance)
    if dec_balance >= 10 ** place:
        str_int = str_dec_balance[:len(str_dec_balance) - place]
        str_decimal = str_dec_balance[len(str_dec_balance) - place:]
        result_decimal_icx = f'{str_int}.{str_decimal}'
        return result_decimal_icx

    else:
        zero = "0."
        val_point = len(str_dec_balance)
        point_difference = place - val_point
        str_zero = "0" * point_difference
        result_decimal_icx = f'{zero}{str_zero}{dec_balance}'
        return result_decimal_icx