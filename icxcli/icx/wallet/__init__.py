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
import json
import os

import requests
from eth_keyfile import create_keyfile_json, extract_key_from_keyfile

from icxcli.icx import FilePathIsWrong, PasswordIsNotAcceptable, NoPermissionToWriteFile, FileExists, \
    PasswordIsIncorrect, WalletAddressIsInvalid
from icxcli.icx import WalletInfo
from icxcli.icx import utils
from icxcli.icx import IcxSigner
from icxcli.icx.utils import get_address_by_privkey, icx_to_wei, get_timestamp_us, get_tx_hash, sign, \
    create_jsonrpc_request_content


def create_wallet(password, file_path):

    """ Create a wallet file with given wallet name, password and file path.

    :param password:  Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param file_path: File path for the keystore file of the wallet.

    :return: Instance of WalletInfo class.
    """

    if not utils.validate_password(password):
        raise PasswordIsNotAcceptable

    key_store_contents = __make_key_store_content(password)
    json_string = json.dumps(key_store_contents)

    try:
        __store_wallet(file_path, json_string)
        w = WalletInfo(json_string)
        return w
    except FileExistsError:
        raise FileExists
    except PermissionError:
        raise NoPermissionToWriteFile
    except FileNotFoundError:
        raise FilePathIsWrong


def show_wallet(password, *args):

    """ Shows the all information of wallet

    :param password(str):  Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param args:
    :return:
    """


def show_asset_list(password, *args):

    """ Enumerate the list of all the assets of the wallet.

    :param password(str): Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param args:
    :return:
    """


def transfer_value_with_the_fee(password, fee, decimal_point, url, to, amount, file_path):
    """ Transfer the value to the specific address with the fee.

    :param password: Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param fee: Transaction fee.
    :param decimal_point: A user can change the decimal point to express all numbers including fee and amount.
    :param to: Address of wallet to receive the asset.
    :param amount: Amount of money. *The decimal point number is valid up to tenth power of 18. *
    :param file_path: File path for the keystore file of the wallet.
    :param url:
    :return:
    """
    try:
        url = f'{url}v2'
        private_key_bytes = key_from_key_store(file_path, bytes(password, 'utf-8'))
        user_address = get_address_by_privkey(private_key_bytes)
        method = 'icx_sendTransaction'
        params = make_params(user_address, to, amount, fee, method, private_key_bytes)

        payload = create_jsonrpc_request_content(0, method, params)
        response = requests.post(url, json=payload, verify=False)

    except FileNotFoundError:
        print("File does not exists.")
        raise FilePathIsWrong
    except IsADirectoryError:
        print(f"{file_path} is a directory.")
        raise FilePathIsWrong
    except ValueError:
        print("Incorrect password.")
        raise PasswordIsIncorrect
    except WalletAddressIsInvalid:
        print("Wallet address is invalid.")


def make_params(user_address, to, amount, fee, method, private_key_bytes):
    params = {
        'from': user_address,
        'to': to,
        'value': hex(icx_to_wei(amount)),
        'fee': hex(icx_to_wei(fee)),
        'timestamp': str(get_timestamp_us())
    }
    tx_hash_bytes = get_tx_hash(method, params)
    signature_bytes = sign(private_key_bytes, tx_hash_bytes)
    params['tx_hash'] = tx_hash_bytes.hex()
    params['signature'] = signature_bytes.decode()

    return params


def __store_wallet(file_path, json_string):
    """ Store wallet information file in JSON format.
    :param file_path: The path where the file will be saved. type: str
    :param json_string: Contents of key_store_file
    """
    if os.path.isfile(file_path):
        raise FileExistsError

    with open(file_path, 'wt') as f:
            f.write(json_string)


def __make_key_store_content(password):
    """Make a content of key_store.

    :param password: Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :return:
    key_store_content(dict)
    """
    signer = IcxSigner()
    private_key = signer.private_key
    key_store_contents = create_keyfile_json(private_key, bytes(password, 'utf-8'), iterations=262144)
    icx_address = "hx" + signer.address.hex()
    key_store_contents['address'] = icx_address
    key_store_contents['coinType'] = 'icx'
    return key_store_contents


def key_from_key_store(file_path, password):
    """

    :param file_path:
    :return:
    """
    private_key = extract_key_from_keyfile(file_path, password)
    return private_key
