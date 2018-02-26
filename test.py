import argparse
import sys


def main(arg_arr):
    """main function
    """

    parser = argparse.ArgumentParser(description='Normal commands: \
                                                 version \
                                                 help \
                                                 ')

    parser.add_argument('command', help='wallet_create, wallet_show, asset_list, transfer')

    parser.add_argument("-wallet_name",
                        dest="wallet_name",
                        required=False, type=str,
                        help="input user's wallet name", metavar="WALLETNAME")
    parser.add_argument("-file_path",
                        dest="file_path",
                        required=False, type=str,
                        help="input wallet file path", metavar="FILEPATH")
    parser.add_argument("-p",
                        dest="password",
                        required=False, type=str,
                        help="input user's password", metavar="PASSWORD")

    parser.add_argument("-f",
                        dest="fee",
                        required=False, type=int,
                        help="input fee", metavar="FEE")

    parser.add_argument("-to",
                        dest="to",
                        required=False, type=str,
                        help="icx address", metavar="to address")

    parser.add_argument("-amount",
                        dest="amount",
                        required=False, type=str,
                        help="amount of icx", metavar="amount of ICX")

    parser.add_argument("-d",
                        dest="decimal_point",
                        required=False, type=int,
                        help="input decimal point", metavar="DECIMALPOINT")

    args = parser.parse_args()
    if args.command == "wallet_create":
        create_wallet(args.wallet_name, args.file_path, args.password)
    elif args.command == "wallet_show":
        show_wallet(args.password)
    elif args.command == "asset_list":
        asset_list(args.password)
    elif args.command == "transfer":
        transfer(args.to, args.amount, args.file_path, args.password, args.fee, args.decimal_point)
    else:
        print(f'Unsupported command {args.command}')


def create_wallet(wallet_name, file_path, password):
    print(wallet_name, file_path, password)


def show_wallet(password):
    print(password)


def asset_list(password):
    print(password)


def transfer(to, amount, file_path, password, fee, decimal_point):
    print(to, amount, file_path, password, fee, decimal_point)


if __name__ == '__main__':
    try:
        main(sys.argv[2:])
    except KeyboardInterrupt:
        print('Exit')
