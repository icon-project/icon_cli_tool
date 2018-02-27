from cmd import cmd


def main():
    command, parser = cmd.parse_args()
    cmd.call_method(command, parser)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("exit")
