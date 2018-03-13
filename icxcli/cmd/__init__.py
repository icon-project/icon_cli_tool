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
import sys
import argparse
import os

from icxcli.cmd import wallet
from icxcli.icx import NonExistKey
from icxcli.cmd.wallet import ExitCode
from icxcli import __version__


def main():
    """
    Main procedure
    :return:
    """
    command, parser = parse_args()
    sys.exit(call_wallet_method(command, parser))


def check_required_argument_in_args(**kwargs):
    """Make sure user has entered all the required arguments.

    :return:
    True when arguments are valid.
    False when arguments are invalid.
    """
    flag = True
    for key, value in kwargs.items():
        flag = flag and bool(value)
    return flag


def parse_args():
    """ Get arguments from CLI and parse the arguments.

    :return: command, parser
    """

    parser = argparse.ArgumentParser(prog='icli.py', usage='''
    
    ==============================
    icli: ICON CLI tool 
    ==============================
        Normal commands:
            version
            help

        Wallet Commands:

            wallet create <file path> -p <password>  
            wallet show <file path> -p <password>    | -n <network id: mainnet | testnet>
            asset list <file path> -p <password>     | -n <network id: mainnet | testnet>
            transfer  <to> <amount> <file path> -p <password> -f <fee=0.01> -d <decimal point=18>  | -n <network id: mainnet | testnet>
            
        WARNING: 
        
            Fee feature is the experimental feature; fee is fixed to 0.01 ICX for now so if you 
            try to make a transaction with the modified fee, which is not 0.01 ICX, then you would 
            not be able to make the transaction. you will be notified 
            when it is possible to make a transaction with the modified fee.

            
        IF YOU MISS -n, icli WILL USE TESTNET.
        
          ''')

    parser.add_argument('command', nargs='*', help='wallet create, wallet show, asset list, transfer')
    parser.add_argument('-p', dest='password'
                        , help='password')
    parser.add_argument('-f', dest='fee'
                        , help='transaction fee', type=float, default=0.01)
    parser.add_argument('-d', dest='decimal_point'
                        , help='decimal point', default=18, type=int)
    parser.add_argument('-n', dest='network_id'
                        , help='which network', default='testnet')

    args = parser.parse_args()

    command = ' '.join(args.command[:2])

    return command, parser


def call_wallet_method(command, parser):
    """ Call the specific wallet method when having right number of arguments.

   :param command: Command part of interface. type: str
   :param parser: ArgumentParser
   """

    args = parser.parse_args()
    url = None
    if args.decimal_point < 1 or args.decimal_point > 18:
        print("Decimal point is invalid.")
        return ExitCode.DECIMAL_POINT_INVALID.value
    try:
        url = get_selected_url(args.network_id)
    except NonExistKey:
        return ExitCode.NETWORK_ID_IS_WRONG.value

    password = args.password
    if command == 'wallet create' and len(args.command) == 3:
        if password is None:
            password = input("You missed your password! input your password : ")
        return wallet.create_wallet(password, args.command[2])
    elif command == 'wallet show' and len(args.command) == 3:
        if password is None:
            password = input("You missed your password! input your password : ")
        return wallet.show_wallet(password, args.command[2], url)
    elif command == 'asset list' and len(args.command) == 3:
        if password is None:
            password = input("You missed your password! input your password : ")
        return wallet.show_asset_list(password, args.command[2], url)
    elif command.split(' ')[0] == 'transfer' and len(args.command) == 4 \
            and check_required_argument_in_args(fee=args.fee, decimal_point=args.decimal_point):
        if password is None:
            password = input("You missed your password! input your password : ")
        return wallet.transfer_value_with_the_fee(
            password, args.fee, args.decimal_point, to=args.command[1],
            amount=args.command[2], file_path=args.command[3], url=url)
    elif command.split(' ')[0] == 'version':
        print(f"icli {__version__}")
    else:
        parser.print_help()
        return 0


def get_selected_url(network_id):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(f"{current_dir}/network_conf.json", 'r') as f:
        network_config_json_str = f.read()
    network_config_json = json.loads(network_config_json_str)

    try:
        return network_config_json["networkid"][network_id]
    except KeyError:
        print(f"{network_id} is not valid network id")
        raise NonExistKey
