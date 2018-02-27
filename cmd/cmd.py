import argparse
from icx import wallet


def check_command_format(correct_length, *command):
    if len(command) == correct_length:
        return True
    else:
        return False


def print_wrong_command_format_message():
    print('Invalid command format check icli.py --help')


def parse_args():
    parser = argparse.ArgumentParser(description="test", prog='icli.py', usage='''
        %(prog)s command options
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


def call_method(command, parser):
    args = parser.parse_args()
    if command == 'wallet create' and len(args.command) == 4:
        wallet.create_wallet(args.password, *args.command)
    elif command == 'wallet show' and len(args.command) == 3:
        wallet.show_wallet(args.password, *args.command)
    elif command == 'asset list' and len(args.command) == 3:
        wallet.show_asset_list(args.password, *args.command)
    elif command.split(' ')[0] == 'transfer' and len(args.command) == 4:
        wallet.transfer(*args.command, password=args.password, fee=args.fee, decimal_point=args.decimal_point)
    elif command.split(' ')[0] == 'version':
        print("version : 0.0.1")
    elif command.split(' ')[0] == 'help':
        parser.print_help()
    else:
        parser.print_help()