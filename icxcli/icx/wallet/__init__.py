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
from eth_keyfile import create_keyfile_json
from icxcli.icx import FilePathIsWrong, PasswordIsNotAcceptable, NoPermissionToWriteFile, FileExists
from icxcli.icx import WalletInfo
from icxcli.icx import utils
from icxcli.icx import IcxSigner


def create_wallet(password, wallet_name, file_path):

    """ Create a wallet file with given wallet name, password and file path.

    :param password:  Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param wallet_name: Name for wallet.
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


def transfer_value_with_the_fee(commands, password=None, fee=None, decimal_point=None):

    """ Transfer the value to the specific address with the fee.

    :param commands:
    :param password: Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param fee: Transaction fee.
    :param decimal_point: A user can change the decimal point to express all numbers including fee and amount.
    :return:
    """


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
