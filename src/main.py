import argparse
from scripts import debug


def main(args):
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_debug = subparsers.add_parser("debug")
    parser_debug.set_defaults(func=debug)

    parser.set_defaults(func=main)

    args = parser.parse_args()

    args.func(args)
