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
from icxcli.icx import wallet, NoEnoughBalanceInWallet, AddressIsWrong, PasswordIsWrong, FilePathIsWrong, \
    AmountIsInvalid, TransferFeeIsInvalid, FeeIsBiggerThanAmount, NotAKeyStoreFile
import json


class ExitCode(Enum):
    """Exit codes for command line interface
    """
    SUCCEED = 0
    FILE_PATH_WITHOUT_FILE_NAME = 121
    FILE_PATH_IS_WRONG = 122
    PASSWORD_IS_WRONG = 123
    FILE_EXISTS = 124
    NETWORK_ID_IS_WRONG = 125
    WALLET_DOES_NOT_HAVE_ENOUGH_BALANCE = 127
    TRANSFER_FEE_IS_INVALID = 128
    TIMESTAMP_IS_NOT_CORRECT = 129
    WALLET_ADDRESS_IS_WRONG = 130
    NO_PERMISSION_TO_WRITE_FILE = 136
    AMOUNT_IS_INVALID = 131
    DECIMAL_POINT_INVALID = 132
    NOT_A_KEY_STORE_FILE = 133


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
        print("Passwords must be at least 8 characters long including alphabet, number, and special character.")
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
    except wallet.FilePathWithoutFileName:
        print(f"Fail: File path needs a file name. Change file path.")
        return ExitCode.FILE_PATH_WITHOUT_FILE_NAME.value


def show_wallet(password, file_path, url) -> int:
    """ Show the all information of wallet. Show the balance and the information in keystore file.

    :param password:  Password including alphabet character, number, and special character. type(str)
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param file_path: File path for the keystore file of the wallet. type(str)
    :param url: api url. type(str)
    :return: Predefined exit code
    """
    try:
        wallet_address, balance, wallet_info = wallet.show_wallet(password, file_path, url)
        print(f"Succeed to show wallet in {file_path}. ")
        print(f"Wallet address : {wallet_address} ")
        print(f"Wallet balance : {balance} ")
        wallet_info = json.dumps(wallet_info, indent=4, sort_keys=True)
        print(f"Wallet keystore_file_info : \n{wallet_info} ")
        return ExitCode.SUCCEED.value
    except wallet.PasswordIsNotAcceptable:
        print("Fail: Password is not acceptable. ")
        print("Password including alphabet character, number, and special character.")
        return ExitCode.PASSWORD_IS_WRONG.value
    except wallet.FilePathIsWrong:
        print(f"Fail: Fail to open {file_path}. Change file path.")
        return ExitCode.FILE_PATH_IS_WRONG.value
    except PasswordIsWrong:
        print("Password is wrong.")
        return ExitCode.PASSWORD_IS_WRONG.value
    except NotAKeyStoreFile:
        print(f"{file_path} is not a Key store File.")
        return ExitCode.NOT_A_KEY_STORE_FILE.value


def show_asset_list(password, file_path, url) -> int:
    """ Enumerate the list of all the assets of the wallet. Show the balance.
    :param password: Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    type(str)
    :param file_path: File path for the keystore file of the wallet. type(str)
    :param url: api url. type(str)
    :return: Predefined exit code
    """
    try:
        wallet_address, balance = wallet.show_asset_list(password, file_path, url)
        print(f"Succeed to show asset list in {file_path}. ")
        print(f"Wallet address : {wallet_address} ")
        print(f"Wallet balance : {balance} ")
        return ExitCode.SUCCEED.value
    except wallet.PasswordIsNotAcceptable:
        print("Fail: Password is not acceptable. ")
        print("Password including alphabet character, number, and special character.")
        return ExitCode.PASSWORD_IS_WRONG.value
    except wallet.FilePathIsWrong:
        print(f"Fail: Fail to open {file_path}. Change file path.")
        return ExitCode.FILE_PATH_IS_WRONG.value
    except PasswordIsWrong:
        print("Password is wrong.")
        return ExitCode.PASSWORD_IS_WRONG.value
    except NotAKeyStoreFile:
        print(f"{file_path} is not a Key store File.")
        return ExitCode.NOT_A_KEY_STORE_FILE.value


def transfer_value_with_the_fee(password, fee, decimal_point, to, amount, file_path, url) -> int:
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
    try:
        transfer_result = wallet.transfer_value_with_the_fee(password, fee, decimal_point, to, amount, file_path, url)
        print("Transaction has been completed successfully.")
        return ExitCode.SUCCEED.value
    except FilePathIsWrong:
        return ExitCode.FILE_PATH_IS_WRONG.value
    except PasswordIsWrong:
        print("Password is wrong.")
        return ExitCode.PASSWORD_IS_WRONG.value
    except AddressIsWrong:
        print("The transaction target address does not have the correct format. please check the address again.")
        return ExitCode.WALLET_ADDRESS_IS_WRONG.value
    except NoEnoughBalanceInWallet:
        print("Wallet does not have enough balance.")
        return ExitCode.WALLET_DOES_NOT_HAVE_ENOUGH_BALANCE.value
    except AmountIsInvalid:
        print("The amount you want to transfer is not valid.")
        return ExitCode.AMOUNT_IS_INVALID.value
    except TransferFeeIsInvalid:
        print("Transaction Fee is invalid.")
        return ExitCode.TRANSFER_FEE_IS_INVALID.value
    except FeeIsBiggerThanAmount:
        print("Fee is bigger than transaction amount. Ple∂ase check your fee again.")
        return ExitCode.TRANSFER_FEE_IS_INVALID.value
    except NotAKeyStoreFile:
        print(f"{file_path} is not a Key store File.")
        return ExitCode.NOT_A_KEY_STORE_FILE.value


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
