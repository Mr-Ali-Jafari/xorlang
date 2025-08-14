"""
XorLang Programming Language

A modern, interpreted programming language with Persian documentation support.
Features include variables, functions, classes, control flow, and built-in libraries.
"""

__version__ = "1.0.0"
__author__ = "Ali Jafari"

from .core.interpreter import Interpreter
from .core.lexer import Lexer
from .core.parser import Parser
from .core.errors import XorLangError, LexError, ParseError, RuntimeError

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
    return run_program(filename, source_code)

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
