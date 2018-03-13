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
import codecs

from eth_keyfile import create_keyfile_json, extract_key_from_keyfile
from icxcli.icx import FilePathIsWrong, PasswordIsNotAcceptable, NoPermissionToWriteFile, FileExists, \
    PasswordIsWrong, FilePathWithoutFileName
from icxcli.icx import WalletInfo
from icxcli.icx import utils
from icxcli.icx import IcxSigner
from icxcli.icx.utils import get_address_by_privkey, icx_to_wei, get_timestamp_us, get_tx_hash, sign, \
    create_jsonrpc_request_content, validate_address, get_payload_of_json_rpc_get_balance, floor_point, \
    check_balance_enough, \
    icx_str_to_wei, get_fee_wei, check_amount_and_fee_is_valid, validate_key_store_file
from icxcli.icx.utils import post
from icxcli.icx.utils import change_hex_balance_to_decimal_balance

import requests
requests.packages.urllib3.disable_warnings()


def create_wallet(password, file_path):

    """ Create a wallet file with given wallet name, password and file path.

    :param password:  Password including alphabet character, number, and special character.
    If the user doesn't give password with -p, then CLI will show the prompt and user need to type the password.
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
    except IsADirectoryError:
        raise FilePathWithoutFileName


def show_wallet(password, file_path, url):
    """ Shows the all information of wallet
    :param password:  Password including alphabet character, number, and special character.
    If the user doesn't give password with -p, then CLI will show the prompt and user need to type the password.
    :param file_path:
    :param url: api url. type(str)
    :return:
    """

    if not utils.validate_password(password):
        raise PasswordIsNotAcceptable

    try:
        validate_key_store_file(file_path)
        private_key_bytes = __key_from_key_store(file_path, bytes(password, 'utf-8'))

        wallet_info = __read_wallet(file_path)
        wallet_address = wallet_info['address']
        balance = __get_balance(wallet_address, url)
        return wallet_address, balance, wallet_info
    except FileNotFoundError:
        raise FilePathIsWrong
    except ValueError:
        raise PasswordIsWrong


def show_asset_list(password, file_path, url):
    """ Enumerate the list of all the assets of the wallet.

    :param password: Password including alphabet character, number, and special character.
    If the user doesn't give password with -p, then CLI will show the prompt and user need to type the password.
    :param file_path:
    :param url:
    :return:
    """
    if not utils.validate_password(password):
        raise PasswordIsNotAcceptable

    try:
        validate_key_store_file(file_path)
        private_key_bytes = __key_from_key_store(file_path, bytes(password, 'utf-8'))
        wallet_info = __read_wallet(file_path)
        wallet_address = wallet_info['address']
        balance = __get_balance(wallet_address, url)
        return wallet_address, balance
    except FileNotFoundError:
        raise FilePathIsWrong
    except ValueError:
        raise PasswordIsWrong


def transfer_value_with_the_fee(password, fee, decimal_point, to, amount, file_path, url):
    """ Transfer the value to the specific address with the fee.

    :param password: Password including alphabet character, number, and special character.
    If the user doesn't give password with -p, then CLI will show the prompt and user need to type the password.
    :param fee: Transaction fee.
    :param decimal_point: A user can change the decimal point to express all numbers including fee and amount.
    :param to: Address of wallet to receive the asset.
    :param amount: Amount of money. *The decimal point number is valid up to tenth power of 18. *
    :param file_path: File path for the keystore file of the wallet.
    :param url: Api url. type(str)
    :return:
    """
    try:
        url = f'{url}v2'
        validate_key_store_file(file_path)
        private_key_bytes = __key_from_key_store(file_path, bytes(password, 'utf-8'))
        user_address = get_address_by_privkey(private_key_bytes)

        validate_address(user_address)
        validate_address(to)

        method = 'icx_sendTransaction'

        amount_wei = icx_str_to_wei(amount)
        fixed_amount = int(floor_point(amount_wei, decimal_point))

        fee_wei = get_fee_wei(fee)
        fixed_fee = int(floor_point(fee_wei, decimal_point))

        check_amount_and_fee_is_valid(fixed_amount, fixed_fee)

        params = __make_params(user_address, to, fixed_amount, fixed_fee, method, private_key_bytes)
        payload = create_jsonrpc_request_content(0, method, params)

        # Request the balance repeatedly until we get the response from ICON network.
        request_gen = request_generator(url)
        balance = __get_balance_after_trasfer(user_address, url, request_gen)
        check_balance_enough(balance, amount, fee)
        next(request_gen)
        response = request_gen.send(payload)
        return response

    except FileNotFoundError:
        print("File does not exists.")
        raise FilePathIsWrong
    except IsADirectoryError:
        print(f"{file_path} is a directory.")
        raise FilePathIsWrong
    except ValueError:
        raise PasswordIsWrong


def __make_params(user_address, to, amount, fee, method, private_key_bytes):
    """Make params for jsonrpc format.

    :param user_address: Address of user's wallet.
    :param to: Address of wallet to receive the asset.
    :param amount: Amount of money.
    :param fee: Transaction fee.
    :param method: Method type. type(str)
    :param private_key_bytes: Private key of user's wallet.
    :return:
    type(dict)
    """
    params = {
        'from': user_address,
        'to': to,
        'value': hex(amount),
        'fee': hex(fee),
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
    """ Make a content of key_store.

    :param password: Password including alphabet character, number, and special character.
    If the user doesn't give password with -p, then CLI will show the prompt and user need to type the password.
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


def __key_from_key_store(file_path, password):
    """

    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as file:
        private_key = extract_key_from_keyfile(file, password)
    return private_key


def __get_balance(address, url):
    """ Get balance of the address indicated by address.

    :param address: icx account address starting with 'hx'
    :param url:
    :return: icx
    """
    url = f'{url}v2'

    method = 'icx_getBalance'
    params = {'address': address}
    payload = create_jsonrpc_request_content(0, method, params)
    response = post(url, payload)
    content = response.json()
    hex_balance = content['result']['response']
    dec_balance = change_hex_balance_to_decimal_balance(hex_balance)

    return dec_balance


def __read_wallet(file_path):
    """Read keystore file

    :param file_path:
    :return: wallet_info
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError
    with codecs.open(file_path, 'r', 'utf-8-sig') as f:
        wallet_info = json.load(f)
        f.close()

    return wallet_info


def request_generator(url):
    while True:
        payload = yield
        yield post(url, payload)


def __get_balance_after_trasfer(address, url, request_gen):
    """ Get balance of the address indicated by address for check balance before transfer icx.

    :param address: Icx account address starting with 'hx'
    :param url: Api url. type(str)
    :param request_gen:
    :return: Balance of the user's wallet.
    """
    payload_for_balance = get_payload_of_json_rpc_get_balance(address, url)

    next(request_gen)
    balance_content = request_gen.send(payload_for_balance).json()

    wei = balance_content['result']['response']
    balance = float(change_hex_balance_to_decimal_balance(wei))

    return balance
