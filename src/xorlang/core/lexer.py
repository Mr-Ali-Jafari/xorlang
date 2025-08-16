# XorLang Lexer
# Supports: numbers, strings, identifiers, keywords, operators, delimiters, comments, and import

import os
from typing import List, Optional, Tuple, Union
from .errors import IllegalCharError, UnterminatedStringError, ExpectedCharError, ImportError


class Position:
    """Tracks position in source code for error reporting."""
    
    def __init__(self, idx: int, ln: int, col: int, fn: str, ftext: str):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftext = ftext

    def advance(self, current_char: Optional[str] = None) -> 'Position':
        """Advance position by one character."""
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self) -> 'Position':
        """Create a copy of this position."""
        return Position(self.idx, self.ln, self.col, self.fn, self.ftext)


# Token Types
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'

TT_PLUS = 'PLUS'
TT_MINUS = 'MINUS'
TT_MUL = 'MUL'
TT_DIV = 'DIV'
TT_MOD = 'MOD'

TT_EQ = 'EQ'     # '='
TT_EE = 'EE'     # '=='
TT_NE = 'NE'     # '!='
TT_LT = 'LT'
TT_GT = 'GT'
TT_LTE = 'LTE'
TT_GTE = 'GTE'

TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LBRACE = 'LBRACE'
TT_RBRACE = 'RBRACE'
TT_COMMA = 'COMMA'
TT_SEMI = 'SEMI'
TT_DOT = 'DOT'
TT_EOF = 'EOF'

DIGITS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_DIGITS = LETTERS + DIGITS + '_'

KEYWORDS = [
    'var', 'func', 'return', 'if', 'else', 'while', 'for', 'true', 'false', 'null',
    'import', 'class', 'new', 'this'
]


class Token:
    """Represents a token in the source code."""
    
    def __init__(self, type_: str, value=None, pos_start: Optional[Position] = None, pos_end: Optional[Position] = None):
        self.type = type_
        self.value = value
        self.pos_start = pos_start.copy() if pos_start else None
        self.pos_end = pos_end.copy() if pos_end else None

    def __repr__(self) -> str:
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

    def matches(self, type_: str, value: any) -> bool:
        """Check if the token matches a given type and value."""
        return self.type == type_ and self.value == value


class Lexer:
    """Lexical analyzer for XorLang source code."""
    
    def __init__(self, fn: str, text: str):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, 0, fn, text)
        self.current_char: Optional[str] = None
        self.advance()

    def advance(self) -> None:
        """Move to the next character in the source."""
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def peek(self) -> Optional[str]:
        """Look at the next character without advancing."""
        nxt = self.pos.idx + 1
        if nxt < len(self.text):
            return self.text[nxt]
        return None

    def make_tokens(self) -> Tuple[List[Token], Optional[Exception]]:
        """Tokenize the entire source code."""
        tokens = []
        
        while self.current_char is not None:
            if self.current_char in ' \t\r':
                self.advance()
            elif self.current_char == '\n':
                self.advance()
            elif self.current_char == '/' and self.peek() == '/':
                self.skip_line_comment()
            elif self.current_char == '/' and self.peek() == '*':
                err = self.skip_block_comment()
                if err:
                    return [], err
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS + '_':
                tokens.append(self.make_identifier_or_keyword())
            elif self.current_char in '"\'':
                tok_or_err = self.make_string()
                if isinstance(tok_or_err, Exception):
                    return [], tok_or_err
                tokens.append(tok_or_err)
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MUL, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(TT_MOD, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_LBRACE, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_RBRACE, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(TT_COMMA, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_SEMI, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '.':
                tokens.append(Token(TT_DOT, pos_start=self.pos.copy()))
                self.advance()
            elif self.current_char == '=':
                start_pos = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_EE, pos_start=start_pos, pos_end=self.pos.copy()))
                    self.advance()
                else:
                    tokens.append(Token(TT_EQ, pos_start=start_pos))
            elif self.current_char == '!':
                start_pos = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_NE, pos_start=start_pos, pos_end=self.pos.copy()))
                    self.advance()
                else:
                    return [], IllegalCharError(start_pos, self.pos.copy(), "'!' must be followed by '='")
            elif self.current_char == '<':
                start_pos = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_LTE, pos_start=start_pos, pos_end=self.pos.copy()))
                    self.advance()
                else:
                    tokens.append(Token(TT_LT, pos_start=start_pos))
            elif self.current_char == '>':
                start_pos = self.pos.copy()
                self.advance()
                if self.current_char == '=':
                    tokens.append(Token(TT_GTE, pos_start=start_pos, pos_end=self.pos.copy()))
                    self.advance()
                else:
                    tokens.append(Token(TT_GT, pos_start=start_pos))
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos.copy(), f"'{char}'")
        
        tokens.append(Token(TT_EOF, pos_start=self.pos.copy()))
        return tokens, None

    def skip_line_comment(self) -> None:
        """Skip a single-line comment."""
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.advance()

    def skip_block_comment(self) -> Optional[Exception]:
        """Skip a multi-line comment."""
        self.advance()  # skip '/'
        self.advance()  # skip '*'
        
        while self.current_char is not None:
            if self.current_char == '*' and self.peek() == '/':
                self.advance()  # skip '*'
                self.advance()  # skip '/'
                return None
            self.advance()
        
        pos_start = self.pos.copy()
        return IllegalCharError(pos_start, self.pos.copy(), 'Unterminated block comment')

    def make_number(self) -> Token:
        """Parse a number token (int or float)."""
        num = ''
        dot_count = 0
        start = self.pos.copy()
        
        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
            num += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(TT_INT, int(num), pos_start=start, pos_end=self.pos.copy())
        else:
            return Token(TT_FLOAT, float(num), pos_start=start, pos_end=self.pos.copy())

    def make_identifier_or_keyword(self) -> Token:
        """Parse an identifier or keyword token."""
        s = ''
        start = self.pos.copy()
        
        while self.current_char is not None and self.current_char in LETTERS_DIGITS:
            s += self.current_char
            self.advance()
        
        t = TT_KEYWORD if s in KEYWORDS else TT_IDENTIFIER
        return Token(t, s, pos_start=start, pos_end=self.pos.copy())

    def make_string(self) -> Union[Token, Exception]:
        """Parse a string literal token."""
        quote = self.current_char
        start = self.pos.copy()
        self.advance()
        
        s = ''
        escape = False
        
        while self.current_char is not None and (self.current_char != quote or escape):
            if escape:
                if self.current_char == 'n':
                    s += '\n'
                elif self.current_char == 't':
                    s += '\t'
                elif self.current_char == 'r':
                    s += '\r'
                elif self.current_char == '"':
                    s += '"'
                elif self.current_char == "'":
                    s += "'"
                elif self.current_char == '\\':
                    s += '\\'
                else:
                    s += self.current_char
                escape = False
            else:
                if self.current_char == '\\':
                    escape = True
                else:
                    s += self.current_char
            self.advance()
        
        if self.current_char is None:
            return UnterminatedStringError(start, self.pos.copy())
        
        self.advance()  # skip closing quote
        return Token(TT_STRING, s, pos_start=start, pos_end=self.pos.copy())

    def handle_import(self, tokens: List[Token]) -> Optional[Exception]:
        """Handle import statement by including tokens from imported file."""
        # Skip whitespace/comments
        while True:
            if self.current_char is None:
                break
            if self.current_char in ' \t\r\n':
                self.advance()
                continue
            if self.current_char == '/' and self.peek() == '/':
                self.skip_line_comment()
                continue
            if self.current_char == '/' and self.peek() == '*':
                err = self.skip_block_comment()
                if err:
                    return err
                continue
            break
        
        if self.current_char not in ('"', "'"):
            pos = self.pos.copy()
            return ExpectedCharError(pos, pos, 'Expected string literal after import')
        
        path_tok_or_err = self.make_string()
        if isinstance(path_tok_or_err, Exception):
            return path_tok_or_err
        
        import_path = path_tok_or_err.value
        
        # Try to find the file in multiple locations
        search_paths = []
        
        # 1. Try as absolute path
        if os.path.isabs(import_path):
            search_paths.append(import_path)
        else:
            # 2. Try relative to current file
            if self.fn != '<stdin>':
                current_dir = os.path.dirname(os.path.abspath(self.fn))
                search_paths.append(os.path.join(current_dir, import_path))
                search_paths.append(os.path.join(current_dir, import_path + '.xor'))
            
            # 3. Try in standard library directory
            try:
                # Find the stdlib directory relative to this file
                lexer_dir = os.path.dirname(os.path.abspath(__file__))
                stdlib_dir = os.path.join(lexer_dir, '..', 'stdlib')
                stdlib_dir = os.path.normpath(stdlib_dir)
                search_paths.append(os.path.join(stdlib_dir, import_path + '.xor'))
                search_paths.append(os.path.join(stdlib_dir, import_path))
            except:
                pass
            
            # 4. Try as relative path from current working directory
            search_paths.append(import_path)
            search_paths.append(import_path + '.xor')
        
        # Try each search path
        txt = None
        actual_path = None
        for path in search_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    txt = f.read()
                    actual_path = path
                    break
            except (FileNotFoundError, OSError):
                continue
        
        if txt is None:
            return ImportError(
                f"File '{import_path}' not found",
                path_tok_or_err.pos_start,
                path_tok_or_err.pos_end
            )
        
        sub_lexer = Lexer(actual_path, txt)
        sub_tokens, sub_err = sub_lexer.make_tokens()
        if sub_err:
            return sub_err
        
        # Add all tokens except EOF
        tokens.extend(sub_tokens[:-1])
        return None


# Public API
def run(fn: str, text: str) -> Tuple[List[Token], Optional[Exception]]:
    """Tokenize XorLang source code."""
    lexer = Lexer(fn, text)
    return lexer.make_tokens()
