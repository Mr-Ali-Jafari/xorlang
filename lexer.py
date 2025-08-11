# XorLang Lexer
# Supports: numbers, strings, identifiers, keywords, operators, delimiters, comments, and import

class Error:
    def __init__(self, error_name, pos_start, pos_end, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result  = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}\n"
        line_text = self.pos_start.ftext.split('\n')[self.pos_start.ln] if self.pos_start.ftext else ''
        result += line_text + '\n'
        result += ' ' * self.pos_start.col + '^'
        return result

class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__("IllegalCharacters", pos_start, pos_end, details)

class UnterminatedStringError(Error):
    def __init__(self, pos_start, pos_end, details="Unterminated string"):
        super().__init__("UnterminatedString", pos_start, pos_end, details)

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details="Expected character"):
        super().__init__("ExpectedCharacter", pos_start, pos_end, details)

class Positions:
    def __init__(self, idx, ln, col, fn, ftext):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftext = ftext

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1
        if current_char == '\n':
            self.ln += 1
            self.col = 0
        return self

    def copy(self):
        return Positions(self.idx, self.ln, self.col, self.fn, self.ftext)

# Token Types
TT_INT        = 'INT'
TT_FLOAT      = 'FLOAT'
TT_STRING     = 'STRING'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD    = 'KEYWORD'

TT_PLUS   = 'PLUS'
TT_MINUS  = 'MINUS'
TT_MUL    = 'MUL'
TT_DIV    = 'DIV'

TT_EQ     = 'EQ'     # '='
TT_EE     = 'EE'     # '=='
TT_NE     = 'NE'     # '!='
TT_LT     = 'LT'
TT_GT     = 'GT'
TT_LTE    = 'LTE'
TT_GTE    = 'GTE'

TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_LBRACE = 'LBRACE'
TT_RBRACE = 'RBRACE'
TT_COMMA  = 'COMMA'
TT_SEMI   = 'SEMI'
TT_DOT    = 'DOT'
TT_EOF    = 'EOF'

DIGITS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS_DIGITS = LETTERS + DIGITS + '_'

KEYWORDS = [
    'var', 'func', 'return', 'if', 'else', 'while', 'for', 'true', 'false', 'null',
    'import', 'class'
]

class TOKEN:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        self.pos_start = pos_start.copy() if pos_start else None
        self.pos_end = pos_end.copy() if pos_end else None

    def __repr__(self):
        if self.value is not None:
            return f"{self.type}:{self.value}"
        return f"{self.type}"

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Positions(-1, 0, 0, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def peek(self):
        nxt = self.pos.idx + 1
        if nxt < len(self.text):
            return self.text[nxt]
        return None

    def make_tokens(self):
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
                tok = self.make_identifier_or_keyword()
                if tok.type == TT_KEYWORD and tok.value == 'import':
                    err = self.handle_import(tokens)
                    if err:
                        return [], err
                else:
                    tokens.append(tok)
            elif self.current_char in '"\'':
                tok_or_err = self.make_string()
                if isinstance(tok_or_err, Error):
                    return [], tok_or_err
                tokens.append(tok_or_err)
            elif self.current_char == '+':
                tokens.append(TOKEN(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(TOKEN(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(TOKEN(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(TOKEN(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(TOKEN(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(TOKEN(TT_RPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == '{':
                tokens.append(TOKEN(TT_LBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == '}':
                tokens.append(TOKEN(TT_RBRACE, pos_start=self.pos))
                self.advance()
            elif self.current_char == ',':
                tokens.append(TOKEN(TT_COMMA, pos_start=self.pos))
                self.advance()
            elif self.current_char == ';':
                tokens.append(TOKEN(TT_SEMI, pos_start=self.pos))
                self.advance()
            elif self.current_char == '.':
                tokens.append(TOKEN(TT_DOT, pos_start=self.pos))
                self.advance()
            elif self.current_char == '!':
                pos_start = self.pos.copy()
                if self.peek() == '=':
                    self.advance(); self.advance()
                    tokens.append(TOKEN(TT_NE, pos_start=pos_start))
                else:
                    return [], IllegalCharError(pos_start, self.pos.copy(), "'!'")
            elif self.current_char == '=':
                pos_start = self.pos.copy()
                if self.peek() == '=':
                    self.advance(); self.advance()
                    tokens.append(TOKEN(TT_EE, pos_start=pos_start))
                else:
                    tokens.append(TOKEN(TT_EQ, pos_start=pos_start))
                    self.advance()
            elif self.current_char == '<':
                pos_start = self.pos.copy()
                if self.peek() == '=':
                    self.advance(); self.advance()
                    tokens.append(TOKEN(TT_LTE, pos_start=pos_start))
                else:
                    tokens.append(TOKEN(TT_LT, pos_start=pos_start))
                    self.advance()
            elif self.current_char == '>':
                pos_start = self.pos.copy()
                if self.peek() == '=':
                    self.advance(); self.advance()
                    tokens.append(TOKEN(TT_GTE, pos_start=pos_start))
                else:
                    tokens.append(TOKEN(TT_GT, pos_start=pos_start))
                    self.advance()
            else:
                pos_start = self.pos.copy()
                ch = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos.copy(), f"'{ch}'")
        tokens.append(TOKEN(TT_EOF, pos_start=self.pos.copy(), pos_end=self.pos.copy()))
        return tokens, None

    def skip_line_comment(self):
        self.advance(); self.advance()
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        if self.current_char == '\n':
            self.advance()

    def skip_block_comment(self):
        self.advance(); self.advance()
        while self.current_char is not None:
            if self.current_char == '*' and self.peek() == '/':
                self.advance(); self.advance();
                return None
            self.advance()
        pos_start = self.pos.copy()
        return IllegalCharError(pos_start, self.pos.copy(), 'Unterminated block comment')

    def make_number(self):
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
            return TOKEN(TT_INT, int(num), pos_start=start, pos_end=self.pos.copy())
        else:
            return TOKEN(TT_FLOAT, float(num), pos_start=start, pos_end=self.pos.copy())

    def make_identifier_or_keyword(self):
        s = ''
        start = self.pos.copy()
        while self.current_char is not None and self.current_char in LETTERS_DIGITS:
            s += self.current_char
            self.advance()
        t = TT_KEYWORD if s in KEYWORDS else TT_IDENTIFIER
        return TOKEN(t, s, pos_start=start, pos_end=self.pos.copy())

    def make_string(self):
        quote = self.current_char
        start = self.pos.copy()
        self.advance()
        s = ''
        escape = False
        while self.current_char is not None and (self.current_char != quote or escape):
            if escape:
                if self.current_char == 'n': s += '\n'
                elif self.current_char == 't': s += '\t'
                elif self.current_char == 'r': s += '\r'
                elif self.current_char == '"': s += '"'
                elif self.current_char == "'": s += "'"
                elif self.current_char == '\\': s += '\\'
                else: s += self.current_char
                escape = False
            else:
                if self.current_char == '\\':
                    escape = True
                else:
                    s += self.current_char
            self.advance()
        if self.current_char is None:
            return UnterminatedStringError(start, self.pos.copy())
        self.advance()
        return TOKEN(TT_STRING, s, pos_start=start, pos_end=self.pos.copy())

    def handle_import(self, tokens):
        # skip whitespace/comments
        while True:
            if self.current_char is None:
                break
            if self.current_char in ' \t\r\n':
                self.advance(); continue
            if self.current_char == '/' and self.peek() == '/':
                self.skip_line_comment(); continue
            if self.current_char == '/' and self.peek() == '*':
                err = self.skip_block_comment()
                if err: return err
                continue
            break
        if self.current_char not in ('"', "'"):
            pos = self.pos.copy()
            return ExpectedCharError(pos, pos, 'Expected string literal after import')
        path_tok_or_err = self.make_string()
        if isinstance(path_tok_or_err, Error):
            return path_tok_or_err
        import_path = path_tok_or_err.value
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                txt = f.read()
        except FileNotFoundError:
            return Error('ImportError', path_tok_or_err.pos_start, path_tok_or_err.pos_end, f"File '{import_path}' not found")
        sub = Lexer(import_path, txt)
        sub_tokens, sub_err = sub.make_tokens()
        if sub_err:
            return sub_err
        tokens.extend(sub_tokens[:-1])
        return None

# Public API

def run(fn, text):
    lexer = Lexer(fn, text)
    return lexer.make_tokens() 