"""
XorLang Programming Language

A modern, interpreted programming language with Persian documentation support.
Features include variables, functions, classes, control flow, and built-in libraries.
"""

__version__ = "2.0.0"
__author__ = "Ali Jafari"

import os
import sys
from typing import Optional

from .core.interpreter import Interpreter
from .core.lexer import Lexer
from .core.parser import Parser
from .core.errors import XorLangError, LexError, ParseError, RuntimeError

def _find_stdlib_path() -> Optional[str]:
    """Find the path to the standard library directory."""
    # Path relative to this file (development setup)
    here = os.path.dirname(os.path.abspath(__file__))
    dev_path = os.path.join(here, 'stdlib')
    if os.path.isdir(dev_path):
        return dev_path

    # Path for PyInstaller bundles
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        bundle_path = os.path.join(sys._MEIPASS, 'stdlib')
        if os.path.isdir(bundle_path):
            return bundle_path

    return None

# Public API
def run_code(source_code: str, filename: str = "<string>"):
    """
    Execute XorLang source code and return the result.
    
    Args:
        source_code: The XorLang source code to execute
        filename: Optional filename for error reporting
        
    Returns:
        Tuple of (result, error_message)
    """
    from .core.runner import run_program
    stdlib_path = _find_stdlib_path()
    return run_program(filename, source_code, stdlib_path)

def tokenize(source_code: str, filename: str = "<string>"):
    """
    Tokenize XorLang source code.
    
    Args:
        source_code: The source code to tokenize
        filename: Optional filename for error reporting
        
    Returns:
        Tuple of (tokens, error)
    """
    from .core.lexer import run as lex_run
    return lex_run(filename, source_code)

def parse(tokens):
    """
    Parse tokens into an AST.
    
    Args:
        tokens: List of tokens from the lexer
        
    Returns:
        ParseResult containing the AST or error
    """
    parser = Parser(tokens)
    return parser.parse()

__all__ = [
    'run_code',
    'tokenize', 
    'parse',
    'Interpreter',
    'Lexer',
    'Parser',
    'XorLangError',
    'LexError',
    'ParseError',
    'RuntimeError',
]
