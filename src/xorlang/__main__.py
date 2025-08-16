"""
XorLang main module for running XorLang files
"""

import sys
from xorlang.core.runner import run_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m xorlang <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    print(f"[DEBUG] Running file: {filename}")
    result, error = run_file(filename)
    if error:
        print(f"Error: {error}")
        sys.exit(1)

if __name__ == "__main__":
    main()
