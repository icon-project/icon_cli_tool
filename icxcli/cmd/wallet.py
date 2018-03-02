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

from enum import Enum
from icxcli.icx import wallet

class ExitCode(Enum):
    """Exit codes for command line interface
    """
    SUCCEED = 0
    FILE_PATH_IS_WRONG = 122
    PASSWORD_IS_WRONG = 123
    WALLET_DOES_NOT_HAVE_ENOUGH_BALANCE = 127
    TRANSFER_FEE_IS_INVALID = 128
    TIMESTAMP_IS_NOT_CORRECT = 129
    WALLET_ADDRESS_IS_WRONG = 130
    NO_PERMISSION_TO_WRITE_FILE = 136


def create_wallet(password, wallet_name, file_path) -> int:
    """ Create a wallet file with given wallet name, password and file path.

    :param password:  Password including alphabet character, number, and special character.
    If the user does not give password with -p, then CLI will show the prompt and user need to type the password.
    :param wallet_name: Name for wallet.
    :param file_path: File path for the keystore file of the wallet.
    :return: Predefined exit code
    """
    try:
        wallet_info = wallet.create_wallet(password, wallet_name, file_path)
        return ExitCode.SUCCEED.value
    except wallet.PasswordIsNotAcceptable:
        print("Password is not acceptable. ")
        return ExitCode.PASSWORD_IS_WRONG.value
    except wallet.FilePathIsWrong:
        print(f"Fail to open {file_path}. ")
        return ExitCode.FILE_PATH_IS_WRONG.value
    except wallet.NoPermissionToWriteFile:
        print(f"No permission to write {file_path}. ")
        return ExitCode.NO_PERMISSION_TO_WRITE_FILE.value


def show_wallet(password, *args) -> int:
    """ Shows the all information of wallet

    :param password(str):  Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param args:
    :return: Predefined exit code
    """
    pass


def show_asset_list(password, *args) -> int:
    """ Enumerate the list of all the assets of the wallet.

    :param password(str): Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param args:
    :return: Predefined exit code
    """
    pass


def transfer_value_with_the_fee(commands, password=None, fee=None, decimal_point=None) -> int:
    """ Transfer the value to the specific address with the fee.

    :param commands:
    :param password(str): Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param fee: Transaction fee.
    :param decimal_point: A user can change the decimal point to express all numbers including fee and amount.
    :return: Predefined exit code
    """
    pass


def store_wallet(file_path, json_string) -> int:
    """ Store wallet information file in JSON format.
    :param file_path(str): The path where the file will be saved. type: str
    :param json_string(str): Contents of key_store_file
    :return: Predefined exit code
    """
    pass


def make_key_store_content(password) -> int:
    """Make a content of key_store.

    :param password(str): Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :return:
    key_store_content(dict)
    """
    pass
