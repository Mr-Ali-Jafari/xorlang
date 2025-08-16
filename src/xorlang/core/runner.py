"""
XorLang Program Runner

This module provides the main entry point for running XorLang programs.
It coordinates the lexer, parser, and interpreter to execute source code.
"""

from typing import Tuple, Any, Optional

from .lexer import run as lex_run
from .parser import Parser
from .interpreter import Interpreter
from .errors import ReturnSignal

def run_file(file_path: str, stdlib_path: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """
    Run a XorLang program from a file.

    Args:
        file_path: Path to the XorLang source file.
        stdlib_path: Optional path to the standard library.

    Returns:
        A tuple containing the result of the execution (or None) and an error
        message (or None).
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        return run_program(file_path, source, stdlib_path)
    except Exception as e:
        return None, f"Error reading file {file_path}: {str(e)}"


def run_interactive() -> None:
    """
    Start an interactive XorLang REPL (Read-Eval-Print Loop).
    """
    interpreter = Interpreter()
    print("XorLang REPL (type 'exit' or press Ctrl+C to quit)")
    
    while True:
        try:
            source = input(">>> ")
            if source.strip().lower() in ('exit', 'quit'):
                break
                
            result, error = run_program('<stdin>', source)
            if error:
                print(f"Error: {error}")
            elif result is not None:
                print(result)
                
        except KeyboardInterrupt:
            print("\nUse 'exit' or Ctrl+D to quit")
        except EOFError:
            print()
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


def run_program(file_path: str, source: str, stdlib_path: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """
    Run a XorLang program from source code.

    Args:
        file_path: Path to the source file, used for error reporting.
        source: The source code to run.
        stdlib_path: Optional path to the standard library.

    Returns:
        A tuple containing the result of the execution (or None) and an error
        message (or None).
    """
    print(f"[DEBUG] Running program from file: {file_path}")
    print(f"[DEBUG] Using stdlib path: {stdlib_path}")
    
    # 1. Initialize the interpreter
    interpreter = Interpreter(stdlib_path=stdlib_path)

    # 2. Lex the source code
    tokens, lex_err = lex_run(file_path, source)
    if lex_err:
        return None, lex_err.format_error()

    # 3. Parse the tokens into an AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error.format_error()

    # 4. Evaluate the AST with the interpreter
    try:
        result = interpreter.eval(ast.node)
        return result, None
    except ReturnSignal:
        return None, "RuntimeError: 'return' used outside of a function."
    except Exception as e:
        # Catch any other unexpected errors during interpretation.
        return None, f"An unexpected error occurred: {e}"
