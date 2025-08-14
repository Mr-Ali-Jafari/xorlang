"""
XorLang Error Classes

Centralized error handling for the XorLang interpreter.
All errors inherit from XorLangError for consistent error handling.
"""

from typing import Optional


class XorLangError(Exception):
    """Base class for all XorLang errors."""
    
    def __init__(self, message: str, pos_start=None, pos_end=None):
        super().__init__(message)
        self.message = message
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def format_error(self) -> str:
        """Format error with position information if available."""
        if self.pos_start and self.pos_end:
            result = f"{self.__class__.__name__}: {self.message}\n"
            result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}\n"
            
            if self.pos_start.ftext:
                line_text = self.pos_start.ftext.split('\n')[self.pos_start.ln]
                result += line_text + '\n'
                result += ' ' * self.pos_start.col + '^'
            
            return result
        return f"{self.__class__.__name__}: {self.message}"


class LexError(XorLangError):
    """Lexical analysis errors (tokenization)."""
    pass


class IllegalCharError(LexError):
    """Illegal character encountered during lexing."""
    
    def __init__(self, pos_start, pos_end, details):
        super().__init__(f"Illegal character: {details}", pos_start, pos_end)


class UnterminatedStringError(LexError):
    """String literal not properly terminated."""
    
    def __init__(self, pos_start, pos_end, details="Unterminated string"):
        super().__init__(details, pos_start, pos_end)


class ExpectedCharError(LexError):
    """Expected specific character not found."""
    
    def __init__(self, pos_start, pos_end, details="Expected character"):
        super().__init__(details, pos_start, pos_end)


class ParseError(XorLangError):
    """Syntax analysis errors (parsing)."""
    
    def __init__(self, pos_start, pos_end, details):
        super().__init__(f"Syntax error: {details}", pos_start, pos_end)


class RuntimeError(XorLangError):
    """Runtime execution errors."""
    
    def __init__(self, message: str, pos_start=None, pos_end=None):
        super().__init__(f"Runtime error: {message}", pos_start, pos_end)


class ImportError(XorLangError):
    """Import-related errors."""
    
    def __init__(self, message: str, pos_start=None, pos_end=None):
        super().__init__(f"Import error: {message}", pos_start, pos_end)


class ReturnSignal(Exception):
    """Internal exception for handling return statements."""
    
    def __init__(self, value):
        self.value = value
        super().__init__("Return signal")
