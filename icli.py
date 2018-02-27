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
    args = parser.parse_args()
    command = ' '.join(args.command[:2])

    if command == 'wallet create':
        # print("wallet name: ", args.command[2])
        create_wallet("kim", "./keystore/", args.password)
    elif command == 'wallet show':
        show_wallet(args.password)
    elif command == 'asset list':
        show_asset_list(args.password)
    elif command.split(' ')[0] == 'transfer':
        transfer(*args.command, password=args.password, fee=args.fee, decimal_point=args.decimal_point)
    elif command.split(' ')[0] == 'version':
        print("version : 0.0.1")
    elif command.split(' ')[0] == 'help':
        parser.print_help()
    else:
        print(f"Unsupported command {args.command[0]}")
        parser.print_help()


def create_wallet(wallet_name, file_path, password):
    """
    create wallet file with given wallet name, password and file path.
    :param wallet_name: name for wallet
    :param file_path: File path for the keystore file of the wallet
    :param password: password including alphabet character, number, and special character.
    :return:
    """
    print(password)


def show_wallet(password):
    print(password)


def show_asset_list(password):
    print(password)


def transfer(*commands, password=None, fee=None, decimal_point=None):
    if len(commands) < 4:
        print("Invalid command")
        pass
    else:
        print(commands[0], commands[1], commands[2], commands[3], password, fee, decimal_point)


def check_command_format(*command, correct_length):

    return True


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exit")
