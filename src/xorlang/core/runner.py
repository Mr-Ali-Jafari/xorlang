"""
XorLang Program Runner

This module provides the main entry point for running XorLang programs.
It coordinates the lexer, parser, and interpreter to execute source code.
"""

import os
import sys
from typing import Tuple, Optional, Any

from .lexer import run as lex_run
from .parser import Parser
from .interpreter import Interpreter
from .errors import ReturnSignal, RuntimeError


def _find_stdlib_path() -> Optional[str]:
    """Find the path to the standard library directory."""
    candidates = []

    # 1) PyInstaller _MEIPASS (for packaged executables)
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        # The path in the bundle is specified in build.py as 'xorlang/stdlib'
        candidates.append(os.path.join(meipass, 'xorlang', 'stdlib'))

    # 2) Next to this file (development setup)
    here = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(here, '..', 'stdlib'))

    # 3) XORLANG_HOME environment variable
    home = os.environ.get('XORLANG_HOME')
    if home:
        candidates.append(os.path.join(home, 'stdlib'))

    # 4) Current working directory stdlib
    candidates.append(os.path.join(os.getcwd(), 'stdlib'))

    for path in candidates:
        if os.path.isdir(path):
            return path

    return None


def _load_and_eval(interpreter: Interpreter, path: str, src: str) -> Tuple[Any, Optional[str]]:
    """Load and evaluate XorLang source code."""
    # Tokenize
    tokens, lex_err = lex_run(path, src)
    if lex_err:
        return None, lex_err.format_error() if hasattr(lex_err, 'format_error') else str(lex_err)
    
    # Parse
    parser = Parser(tokens)
    parse_result = parser.parse()
    if parse_result.error:
        return None, parse_result.error.format_error() if hasattr(parse_result.error, 'format_error') else str(parse_result.error)
    
    # Interpret
    try:
        value = interpreter.eval(parse_result.node, interpreter.env)
        return value, None
    except RuntimeError as e:
        return None, f"RuntimeError: {e}"
    except ReturnSignal:
        return None, "RuntimeError: 'return' used outside of a function"
    except Exception as e:
        return None, f"Unexpected error: {e}"


def run_program(filename: str, source_code: str) -> Tuple[Any, Optional[str]]:
    """
    Run a XorLang program.
    
    Args:
        filename: The filename for error reporting
        source_code: The XorLang source code to execute
        
    Returns:
        Tuple of (result, error_message). If error_message is not None,
        an error occurred during execution.
    """
    stdlib_path = _find_stdlib_path()
    interpreter = Interpreter(stdlib_path=stdlib_path)
    
    # Load and run user program
    return _load_and_eval(interpreter, filename, source_code)


def run_file(filepath: str) -> Tuple[Any, Optional[str]]:
    """
    Run a XorLang file.
    
    Args:
        filepath: Path to the XorLang file to execute
        
    Returns:
        Tuple of (result, error_message)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_code = f.read()
        return run_program(filepath, source_code)
    except FileNotFoundError:
        return None, f"File not found: {filepath}"
    except Exception as e:
        return None, f"Error reading file {filepath}: {e}"


def run_interactive():
    """Run XorLang in interactive mode (REPL)."""
    print("XorLang Interactive Shell")
    print("Type 'exit' or press Ctrl+C to quit")
    print()
    
    stdlib_path = _find_stdlib_path()
    interpreter = Interpreter(stdlib_path=stdlib_path)
    
    while True:
        try:
            source = input("xor> ")
            if source.strip().lower() in ('exit', 'quit'):
                break
            
            if not source.strip():
                continue
            
            result, error = _load_and_eval(interpreter, "<interactive>", source)
            if error:
                print(error)
            elif result is not None:
                print(result)
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break
