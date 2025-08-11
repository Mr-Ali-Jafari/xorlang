#!/usr/bin/env python3
import sys
from interpreter import run_program

def main():
    if len(sys.argv) < 2:
        print("Usage: xorlang <sourcefile>")
        sys.exit(1)

    path = sys.argv[1]
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
        sys.exit(1)

    result, err = run_program(path, src)
    if err:
        print(err)
        sys.exit(1)

    if result is not None:
        print(result)

if __name__ == '__main__':
    main()
