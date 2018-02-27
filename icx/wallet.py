def create_wallet(password, *args):
    print(args, password)


def show_wallet(password, *args):
    print(args, password)


def show_asset_list(password, *args):
    print(args, password)


def transfer(*commands, password=None, fee=None, decimal_point=None):
    print(commands, password, fee, decimal_point)