import os, sys, argparse

from command import update
from config import loadConfig, config_file_path

VERSION = '0.2.0'

if __name__ == "__main__":
    # Load Config
    cfg = loadConfig(config_file_path)


    # Load arguments
    ## Top level parser
    parser = argparse.ArgumentParser()

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s '+VERSION)

    ## Subcommands
    subparsers = parser.add_subparsers()

    ### Update subcommand
    parser_update = subparsers.add_parser("update",
                                          help="update packages (default, if non provided)")
    parser_update.add_argument("--dry-run",
                               help="Just list the packages, don't actually run any commands",
                               action="store_true")
    parser_update.add_argument("--verbose", "-v",
                               action="count",
                               default=0,
                               help="The verbosity level")
    parser_update.set_defaults(func=update.command)


    # Execute command
    args = parser.parse_args(sys.argv[1:])
    args.func(args, cfg)
