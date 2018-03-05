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
    FILE_EXISTS = 124
    WALLET_DOES_NOT_HAVE_ENOUGH_BALANCE = 127
    TRANSFER_FEE_IS_INVALID = 128
    TIMESTAMP_IS_NOT_CORRECT = 129
    WALLET_ADDRESS_IS_WRONG = 130
    NO_PERMISSION_TO_WRITE_FILE = 136


def create_wallet(password, file_path) -> int:
    """ Create a wallet file with given password and file path.

    :param password:  Password including alphabet character, number, and special character.
    If the user does not give password with -p, then CLI will show the prompt and user need to type the password.
    type(str)
    :param file_path: File path for the keystore file of the wallet. type(str)
    :return: Predefined exit code
    """
    try:
        wallet_info = wallet.create_wallet(password, file_path)
        print(f"Succeed to create wallet in {file_path}. ")
        print(f"Wallet address : {wallet_info.address} ")
        return ExitCode.SUCCEED.value
    except wallet.PasswordIsNotAcceptable:
        print("Fail: Password is not acceptable. ")
        print("Password including alphabet character, number, and special character.")
        return ExitCode.PASSWORD_IS_WRONG.value
    except wallet.FilePathIsWrong:
        print(f"Fail: Fail to open {file_path}. Change file path.")
        return ExitCode.FILE_PATH_IS_WRONG.value
    except wallet.NoPermissionToWriteFile:
        print(f"Fail: No permission to write {file_path}. Change file path.")
        return ExitCode.NO_PERMISSION_TO_WRITE_FILE.value
    except wallet.FileExists:
        print(f"Fail: {file_path} exists. Change keystore file name.")
        return ExitCode.FILE_EXISTS.value


def show_wallet(password, file_path) -> int:
    """ Shows the all information of wallet

    :param password:  Password including alphabet character, number, and special character. type(str)
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param file_path: File path for the keystore file of the wallet. type(str)
    :return: Predefined exit code
    """
    pass


def show_asset_list(password, file_path) -> int:
    """ Enumerate the list of all the assets of the wallet.

    :param password: Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    type(str)
    :param file_path: File path for the keystore file of the wallet. type(str)
    :return: Predefined exit code
    """
    pass


def transfer_value_with_the_fee(password, fee, decimal_point, to, amount, file_path) -> int:
    """ Transfer the value to the specific address with the fee.

    :param password: Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    type(str)
    :param fee: Transaction fee.
    :param decimal_point: A user can change the decimal point to express all numbers including fee and amount.
    :param to: A user can change the decimal point to express all numbers including fee and amount.
    :param amount: A user can change the decimal point to express all numbers including fee and amount.
    :param file_path: File path for the keystore file of the wallet. type(str)
    :return: Predefined exit code
    """
    print(password, fee, decimal_point, to, amount, file_path)
    pass


def store_wallet(file_path, json_string) -> int:
    """ Store wallet information file in JSON format.
    :param file_path: The path where the file will be saved. type(str)
    :param json_string: Contents of key_store_file. type(str)
    :return: Predefined exit code
    """
    pass


def make_key_store_content(password) -> int:
    """Make a content of key_store.

    :param password: Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    type(str)
    :return:
    key_store_content(dict)
    """
    pass
