import argparse
import sys
from .namespace import RecursiveNamespace
from .converter import Recurser
from decimal import Decimal
from os.path import join as pjoin
from pathlib import Path
from typing import Tuple
from yaml import safe_load

_CONFIG = "config/config.yml"


def appconfig() -> Tuple[RecursiveNamespace, RecursiveNamespace]:
    """Parse config and cli options for script control"""

    def prompter(message: str) -> Decimal:
        """Prompt user for numeric and convert to Decimal"""
        # Build Prompt Message
        prompt = f"> Enter {message}: "

        # Prompt Until Input is a Int/Float
        while True:
            try:
                value = float(input(prompt))
            except ValueError:
                print("ERROR> given value must be a numeric value")
            except KeyboardInterrupt:
                print("\nexiting")
                sys.exit(255)
            else:
                break

        return Decimal(float(value))

    # Get Configuration File
    path = pjoin(Path(__file__).parent, _CONFIG)
    with open(path, "r") as cfg_file:
        cfg = RecursiveNamespace(**Recurser.rsnaked(safe_load(cfg_file)))

    # Create Parser
    parser = argparse.ArgumentParser(
        add_help=True,
        description=("Utilities Calculator Tool"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add Arguments to Parser
    for bill in cfg.bills:
        arg_flag = bill.lower()
        arg_help = f"amount of {arg_flag} bill"
        parser.add_argument(
            f"-{arg_flag[0]}",
            f"--{arg_flag}",
            help=arg_help,
            required=False,
            type=Decimal,
        )

    # Argparse to Namespace
    args = RecursiveNamespace(**vars(parser.parse_args()))

    # Prompt for Value on Empty Flags
    seen = {"help": True}
    for key, value in parser._option_string_actions.items():
        argdest = value.dest
        if seen.get(argdest) is None:
            seen[argdest] = True
            if getattr(args, argdest) is None:
                setattr(args, argdest, prompter(value.help))

    return args, cfg
