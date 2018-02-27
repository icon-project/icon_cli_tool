import argparse
import sys


def main(argv):
    parser = argparse.ArgumentParser(description="test")
    parser = argparse.ArgumentParser(prog='icli.py', usage='''
    %(prog)s command options
    Normal commands:
      version
      help

    Wallet Commands:
      wallet create <file path> -p <password>
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
        create_wallet(args.password)
    elif command == 'wallet show':
        show_wallet(args.password)
    elif command == 'asset list':
        show_asset_list(args.password)
    elif command.split(' ')[0] == 'transfer':
        transfer(*args.command, password=args.password, fee=args.fee, decimal_point=args.decimal_point)
    elif command.split(' ')[0] == 'version':
        print("version : 0.0.1")
    else:
        print(f"Unsupported command {args.command[0]}")
        parser.print_help()


def create_wallet(password):
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


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except KeyboardInterrupt:
        print("exit")