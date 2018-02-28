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

import argparse
from icxcli.icx import wallet


def main():
    """
    Main procedure
    :return:
    """
    command, parser = parse_args()
    call_wallet_method(command, parser)
    return 0



def check_required_argument(*args):
    """

    :param args:
    :return:
    """
    flag = True
    for arg in args:
        flag = flag and bool(arg)
    print(flag)
    return flag


def parse_args():
    """ Get arguments from CLI and parse the arguments.

    :return: command, parser
    """

    parser = argparse.ArgumentParser(prog='icli.py', usage='''
        Normal commands:
          version
          help

        Wallet Commands:
          wallet create <wallet name> <file path> -p <password>
          wallet show <file path> -p <password>
          asset list <file path> -p <password>
          transfer  <to> <amount> <file path> -p <password> -f <fee> -d <decimal point=18>

          ''')

    parser.add_argument('command', nargs='*', help='wallet create, wallet show, asset list, transfer')
    parser.add_argument('-p', dest='password'
                        , help='password')
    parser.add_argument('-f', dest='fee'
                        , help='transaction fee')
    parser.add_argument('-d', dest='decimal_point'
                        , help='decimal point')
    parser.add_argument('-n', dest='network_id'
                        , help='which network', default='main_net_network')

    args = parser.parse_args()

    command = ' '.join(args.command[:2])

    return command, parser


def call_wallet_method(command, parser):
    """ Call the specific wallet method when having right number of arguments.

    :param command:
    :param parser:
    :return:
    """

    args = parser.parse_args()

    if command == 'wallet create' and len(args.command) == 4 and check_required_argument(args.password):
        wallet.create_wallet(args.password, *args.command)
    elif command == 'wallet show' and len(args.command) == 3 and check_required_argument(args.password):
        wallet.show_wallet(args.password, *args.command)
    elif command == 'asset list' and len(args.command) == 3 and check_required_argument(args.password):
        wallet.show_asset_list(args.password, *args.command)
    elif command.split(' ')[0] == 'transfer' and len(args.command) == 4 \
            and check_required_argument(args.password, args.fee, args.decimal_point):
        wallet.transfer(*args.command, password=args.password, fee=args.fee, decimal_point=args.decimal_point)
    elif command.split(' ')[0] == 'version':
        print("version : 0.0.1") # TODO: Read the value from external configure file.
    else:
        parser.print_help()
