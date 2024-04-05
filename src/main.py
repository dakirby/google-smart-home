import argparse
from scripts import debug


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_debug = subparsers.add_parser("debug")
    parser_debug.set_defaults(func=debug)

    args = parser.parse_args()

    args.func(args)
