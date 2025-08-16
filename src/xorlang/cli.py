#!/usr/bin/env python3
"""
XorLang Command Line Interface

Provides the main command-line entry point for the XorLang interpreter.
"""

import sys
import argparse
from typing import NoReturn
import os

# Add the project root to the Python path
# This is necessary for the executable to find the 'xorlang' package
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from xorlang.core.runner import run_file, run_interactive, run_program
from xorlang import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        prog='xorlang',
        description='XorLang Programming Language Interpreter',
        epilog='For more information, visit: https://github.com/Mr-Ali-Jafari/Xorlang'
    )
    
    parser.add_argument(
        'file',
        nargs='?',
        help='XorLang source file to execute'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'XorLang {__version__}'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Start interactive shell (REPL)'
    )
    
    parser.add_argument(
        '-c', '--command',
        metavar='COMMAND',
        help='Execute XorLang code from command line'
    )
    
    return parser


def main() -> NoReturn:
    """Main entry point for the XorLang CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        if args.command:
            # Execute code from command line
            result, error = run_program('<command>', args.command)
            if error:
                print(error, file=sys.stderr)
                sys.exit(1)
            if result is not None:
                print(result)
        
        elif args.interactive or not args.file:
            # Start interactive shell
            run_interactive()
        
        else:
            # Execute file
            result, error = run_file(args.file)
            if error:
                print(error, file=sys.stderr)
                sys.exit(1)
            if result is not None:
                print(result)
    
    except KeyboardInterrupt:
        print("\nInterrupted", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    
    sys.exit(0)


if __name__ == '__main__':
    main()
