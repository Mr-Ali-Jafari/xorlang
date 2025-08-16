"""
XorLang Core Components

This module contains the core interpreter components:
- Lexer: Tokenization and lexical analysis
- Parser: Syntax analysis and AST generation  
- Interpreter: Runtime execution and evaluation
- Errors: Exception classes for error handling
"""

from .lexer import Lexer, run as lex_run
from .parser import Parser
from .interpreter import Interpreter
from .errors import XorLangError, LexError, ParseError, RuntimeError
from .runner import run_program

__all__ = [
    'Lexer',
    'Parser', 
    'Interpreter',
    'XorLangError',
    'LexError',
    'ParseError',
    'RuntimeError',
    'lex_run',
    'run_program',
]
