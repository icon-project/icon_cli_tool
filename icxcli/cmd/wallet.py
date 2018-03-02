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


from icxcli.cmd import ErrorCode
from icxcli.icx import wallet


def create_wallet(password, wallet_name, file_path):
    """ Create a wallet file with given wallet name, password and file path.

    :param password(str):  Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param wallet_name(str): Name for wallet.
    :param file_path(str): File path for the keystore file of the wallet.

    :return:
    0: Succeed to create keystore file.
    122: When file_path does not exists.
    123: When password is not correct format.
    """

    return_code = ErrorCode.SUCCEED


    try:
        create_wallet(password



def show_wallet(password, *args):
    """ Shows the all information of wallet

    :param password(str):  Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param args:
    :return:
    """
    pass


def show_asset_list(password, *args):
    """ Enumerate the list of all the assets of the wallet.

    :param password(str): Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param args:
    :return:
    """
    pass


def transfer_value_with_the_fee(commands, password=None, fee=None, decimal_point=None):
    """ Transfer the value to the specific address with the fee.

    :param commands:
    :param password(str): Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :param fee: Transaction fee.
    :param decimal_point: A user can change the decimal point to express all numbers including fee and amount.
    :return:
    """
    pass


def store_wallet(file_path, json_string):
    """ Store wallet information file in JSON format.
    :param file_path(str): The path where the file will be saved. type: str
    :param json_string(str): Contents of key_store_file
    """
    pass


def make_key_store_content(password):
    """Make a content of key_store.

    :param password(str): Password including alphabet character, number, and special character.
    If the user doesn’t give password with -p, then CLI will show the prompt and user need to type the password.
    :return:
    key_store_content(dict)
    """
    pass
