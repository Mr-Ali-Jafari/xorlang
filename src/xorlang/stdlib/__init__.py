"""
XorLang Standard Library

This module contains the XorLang standard library components.
"""

import os

def get_stdlib_path():
    """Get the path to the XorLang standard library directory."""
    return os.path.dirname(os.path.abspath(__file__))

def get_prelude_path():
    """Get the path to the prelude.xor file."""
    return os.path.join(get_stdlib_path(), 'prelude.xor')
