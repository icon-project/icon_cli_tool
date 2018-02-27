import argparse


def main():
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

    if command == 'wallet create':
        create_wallet(args.password, *args.command)
    elif command == 'wallet show':
        show_wallet(args.password, *args.command)
    elif command == 'asset list':
        show_asset_list(args.password, *args.command)
    elif command.split(' ')[0] == 'transfer':
        transfer(*args.command, password=args.password, fee=args.fee, decimal_point=args.decimal_point)
    elif command.split(' ')[0] == 'version':
        print("version : 0.0.1")
    elif command.split(' ')[0] == 'help':
        parser.print_help()
    else:
        print(f"Unsupported command {args.command[0]}")
        parser.print_help()


def create_wallet(password, *args):
    """

    :param password:
    :param args:
    :return:
    """
    if check_command_format(4, *args) is True:
        print("yes")
    else:
        print_wrong_command_format_message()


def show_wallet(password, *args):
    if check_command_format(3, *args) is True:
        print("yes")
    else:
        print_wrong_command_format_message()


def show_asset_list(password, *args):
    if check_command_format(3, *args) is True:
        print("yes")
    else:
        print_wrong_command_format_message()


def transfer(*commands, password=None, fee=None, decimal_point=None):
    if check_command_format(4, *commands) is True:
        print("yes")
    else:
        print_wrong_command_format_message()


def check_command_format(correct_length, *command):
    if len(command) == correct_length:
        return True
    else:
        return False


def print_wrong_command_format_message():
    print('Invalid command format check icli.py --help')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exit")
