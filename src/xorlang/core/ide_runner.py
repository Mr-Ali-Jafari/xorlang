"""
IDE-specific runner for XorLang programs.
Handles input/output in the IDE environment.
"""

import io
import sys
from typing import Tuple, Optional, Any
from .lexer import Lexer
from .parser import Parser
from .interpreter import Interpreter
from .errors import XorLangError, ReturnSignal

class IDERunner:
    def __init__(self, input_callback=None, output_callback=None):
        self.input_callback = input_callback or input
        self.output_callback = output_callback or print
        self._stdout = io.StringIO()
        self._output_buffer = []

    def _custom_print(self, *args):
        """Custom print function that redirects output to the IDE."""
        output = " ".join(str(arg) for arg in args)
        self._output_buffer.append(output)
        if self.output_callback:
            self.output_callback(output)

    def _custom_input(self, prompt=None):
        """Custom input function that uses IDE's input mechanism."""
        if prompt:
            self._custom_print(prompt)
        if self.input_callback:
            return self.input_callback()
        return ""

    def run_program(self, filename: str, code: str) -> Tuple[Optional[Any], Optional[str]]:
        """
        Run a XorLang program with IDE-specific input/output handling.
        
        Args:
            filename: Name of the file being executed
            code: Source code to execute
        
        Returns:
            Tuple of (result, error)
        """
        # Clear previous output
        self._output_buffer.clear()
        
        try:
            # Create interpreter with custom IO functions
            interpreter = Interpreter()
            
            # Override built-in print and input
            def builtin_print(*args):
                self._custom_print(*args)
            
            def builtin_input(prompt=None):
                return self._custom_input(prompt)
            
            interpreter.globals.define('print', ('builtin', 'print', builtin_print))
            interpreter.globals.define('input', ('builtin', 'input', builtin_input))
            
            # Lex the code
            lexer = Lexer(filename, code)
            tokens, error = lexer.make_tokens()
            if error:
                return None, str(error)
                
            # Parse the tokens
            parser = Parser(tokens)
            result = parser.parse()
            if result.error:
                return None, str(result.error)
            
            # Run the program
            try:
                result = interpreter.eval(result.node)
                return result, None
            except ReturnSignal as ret:
                return ret.value, None
            
        except XorLangError as e:
            return None, str(e)
        except Exception as e:
            return None, f"Runtime error: {str(e)}"

    @property
    def output(self) -> str:
        """Get all accumulated output."""
        return "\n".join(self._output_buffer)
