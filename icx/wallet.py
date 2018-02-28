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
import hashlib
import json
import os
from secp256k1 import PrivateKey, PublicKey
from eth_keyfile import create_keyfile_json
from . import utils


def create_wallet(password, wallet_name, file_path):

    """ Create a wallet file with given wallet name, password and file path.

    :param password:
    :param wallet_name:
    :param file_path:
    :return:
    """
    return_code = 0

    if os.path.isdir(file_path) is False:
        return 122
    if os.access(file_path, os.W_OK) is False:
        return 136
    if utils.validate_password(password) is False:
        return 123

    priv_key, pub_key = generate_keys()
    get_address(pub_key)
    key_store_contents = create_keyfile_json(priv_key, b'fsfsdf', iterations=262144)
    icx_address = "hx" + key_store_contents["address"]
    key_store_contents['address'] = icx_address

    json_string = json.dumps(key_store_contents)

    store_wallet(file_path, json_string)

    return return_code


def show_wallet(password, *args):

    """ Shows the all information of wallet

    :param password:
    :param args:
    :return:
    """


def show_asset_list(password, *args):

    """ Enumerate the list of all the assets of the wallet.

    :param password:
    :param args:
    :return:
    """


def transfer_value_with_the_fee(*commands, password=None, fee=None, decimal_point=None):

    """ Transfer the value to the specific address with the fee.

    :param commands:
    :param password:
    :param fee:
    :param decimal_point:
    :return:
    """


def generate_keys():
    """generate privkey and pubkey pair.

    Returns:
        tuple: privkey(bytes, 32), pubkey(bytes, 65)
    """
    privkey = PrivateKey()

    privkey_bytes = privkey.private_key
    pubkey_bytes = privkey.pubkey.serialize(False)

    return privkey_bytes, pubkey_bytes


def get_address(pubkey_bytes):
    """generate address from public key.

    Args:
        pubkey_bytes(bytes): public key bytes

    Returns:
        bytes: icx address (20bytes)
    """

    # Remove the first byte(0x04) of pubkey
    print(hashlib.sha3_256(pubkey_bytes[1:]).digest()[-20:].hex())
    return hashlib.sha3_256(pubkey_bytes[1:]).digest()[-20:]


def store_wallet(file_path, json_string):
    """

    :param file_path:
    :param json_string:
    :return:
    """
    full_path = file_path + "file.txt"
    with open(full_path, 'wt') as fout:
        fout.write(json_string)
