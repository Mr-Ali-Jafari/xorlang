# XorLang Parser
# Converts tokens into an Abstract Syntax Tree (AST)

from typing import List, Optional, Tuple, Union
from .lexer import Token, TT_INT, TT_FLOAT, TT_STRING, TT_IDENTIFIER, TT_KEYWORD, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_LPAREN, TT_RPAREN, TT_LBRACE, TT_RBRACE, TT_COMMA, TT_SEMI, TT_DOT, TT_EQ, TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE, TT_EOF
from .errors import ParseError
from .ast_nodes import *


class ParseResult:
    """Represents the result of a parsing operation."""
    
    def __init__(self):
        self.error: Optional[ParseError] = None
        self.node: Optional[ASTNode] = None
        self.advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        """Register that the parser advanced by one token."""
        self.advance_count += 1

    def register(self, res: 'ParseResult'):
        """Register the result of another parsing operation."""
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def try_register(self, res: 'ParseResult'):
        """Try to register a result, but allow backtracking on failure."""
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node: ASTNode):
        """Mark parsing as successful with the given node."""
        self.node = node
        return self

    def failure(self, error: ParseError):
        """Mark parsing as failed with the given error."""
        if not self.error or self.advance_count == 0:
            self.error = error
        return self


class Parser:
    """Recursive descent parser for XorLang."""
    
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.tok_idx = -1
        self.current_tok: Optional[Token] = None
        self.advance()

    def advance(self) -> Token:
        """Move to the next token."""
        self.tok_idx += 1
        self.update_current_tok()
        return self.current_tok

    def reverse(self, amount: int = 1):
        """Move back by the specified number of tokens."""
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        """Update the current token based on the current index."""
        if 0 <= self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self) -> ParseResult:
        """Parse the tokens into an AST."""
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*', '/', '==', '!=', '<', '>', '<=', '>=', 'var', 'if', 'for', 'while', 'func', 'return', or 'class'"
            ))
        return res

    def statements(self) -> ParseResult:
        """Parse a sequence of statements until a closing brace or EOF."""
        res = ParseResult()
        statements_list = []
        pos_start = self.current_tok.pos_start.copy()

        # Allow for an empty block
        if self.current_tok.type in (TT_EOF, TT_RBRACE):
            return res.success(BlockNode([], pos_start, self.current_tok.pos_end))

        # Parse first statement
        node = res.register(self.statement())
        if res.error:
            return res
        statements_list.append(node)

        # Parse subsequent statements
        while self.current_tok.type not in (TT_EOF, TT_RBRACE):
            # Statements can be separated by one or more semicolons
            semicolon_count = 0
            while self.current_tok.type == TT_SEMI:
                res.register_advancement()
                self.advance()
                semicolon_count += 1
            
            # If we consumed semicolons but are now at the end, it's a valid end of block
            if self.current_tok.type in (TT_EOF, TT_RBRACE):
                break

            # If there were no semicolons, it's a syntax error unless it's the start of a new valid statement
            # This logic is handled by the self.statement() call failing, so we just try to parse it.
            node = res.register(self.statement())
            if res.error:
                return res
            statements_list.append(node)

        pos_end = statements_list[-1].pos_end if statements_list else self.current_tok.pos_start
        return res.success(BlockNode(statements_list, pos_start, pos_end))



    def statement(self) -> ParseResult:
        """Parse a single statement."""
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, 'var'):
            return self.var_decl_statement()
        elif self.current_tok.matches(TT_KEYWORD, 'if'):
            return self.if_statement()
        elif self.current_tok.matches(TT_KEYWORD, 'while'):
            return self.while_statement()
        elif self.current_tok.matches(TT_KEYWORD, 'for'):
            return self.for_statement()
        elif self.current_tok.matches(TT_KEYWORD, 'func'):
            return self.func_def_statement()
        elif self.current_tok.matches(TT_KEYWORD, 'class'):
            return self.class_def_statement()
        elif self.current_tok.matches(TT_KEYWORD, 'return'):
            return self.return_statement()
        else:
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(ExpressionStatementNode(expr))

    def var_decl_statement(self) -> ParseResult:
        """Parse variable declaration statement."""
        res = ParseResult()
        res.register_advancement()
        self.advance() # consume 'var'

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected identifier"
            ))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_EQ:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            return res.success(VarDeclNode(var_name, expr))

        return res.success(VarDeclNode(var_name, None))

    def if_statement(self) -> ParseResult:
        """Parse if statement."""
        res = ParseResult()
        cases = []
        else_case = None

        res.register_advancement()
        self.advance() # consume 'if'

        if self.current_tok.type != TT_LPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '('"))
        
        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res
        cases.append((condition, body))

        if self.current_tok.type != TT_RBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '}'"
            ))

        res.register_advancement()
        self.advance()

        while self.current_tok.matches(TT_KEYWORD, 'elif'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_LPAREN:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '('"))

            res.register_advancement()
            self.advance()

            condition = res.register(self.expr())
            if res.error:
                return res

            if self.current_tok.type != TT_RPAREN:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_LBRACE:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '{'"
                ))

            res.register_advancement()
            self.advance()

            body = res.register(self.statements())
            if res.error:
                return res
            cases.append((condition, body))

            if self.current_tok.type != TT_RBRACE:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '}'"
                ))

            res.register_advancement()
            self.advance()

        if self.current_tok.matches(TT_KEYWORD, 'else'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_LBRACE:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '{'"
                ))

            res.register_advancement()
            self.advance()

            else_case = res.register(self.statements())
            if res.error:
                return res

            if self.current_tok.type != TT_RBRACE:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '}'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(IfNode(cases, else_case))

    def while_statement(self) -> ParseResult:
        """Parse while statement."""
        res = ParseResult()
        res.register_advancement()
        self.advance() # consume 'while'

        if self.current_tok.type != TT_LPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '('"))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expr())
        if res.error:
            return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if self.current_tok.type != TT_RBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '}'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(WhileNode(condition, body))

    def for_statement(self) -> ParseResult:
        """Parse for statement."""
        res = ParseResult()
        res.register_advancement()
        self.advance() # consume 'for'

        if self.current_tok.type != TT_LPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '('"))

        res.register_advancement()
        self.advance()

        # Init
        if self.current_tok.type == TT_SEMI:
            init_node = None
            res.register_advancement()
            self.advance()
        else:
            init_node = res.register(self.statement())
            if res.error:
                return res
            if self.current_tok.type != TT_SEMI:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ';' after for loop initializer"
                ))
            res.register_advancement()
            self.advance()

        # Condition
        if self.current_tok.type == TT_SEMI:
            cond_node = None
            res.register_advancement()
            self.advance()
        else:
            cond_node = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type != TT_SEMI:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ';' after for loop condition"
                ))
            res.register_advancement()
            self.advance()

        # Update
        if self.current_tok.type == TT_RPAREN:
            update_node = None
        else:
            update_node = res.register(self.expr())
            if res.error:
                return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')' after for loop clauses"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{'"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if self.current_tok.type != TT_RBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '}'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(ForNode(init_node, cond_node, update_node, body))

    def func_def_statement(self) -> ParseResult:
        """Parse function definition."""
        res = ParseResult()
        res.register_advancement()
        self.advance() # consume 'func'

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
        else:
            var_name_tok = None

        if self.current_tok.type != TT_LPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '(' in function definition"
            ))

        res.register_advancement()
        self.advance()

        arg_name_toks = []
        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(ParseError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier"
                    ))
                
                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

        if self.current_tok.type != TT_RPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')' or ',' in function definition"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{' in function definition"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.statements())
        if res.error:
            return res

        if self.current_tok.type != TT_RBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '}'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(var_name_tok, arg_name_toks, body))

    def class_def_statement(self) -> ParseResult:
        """Parse class definition."""
        res = ParseResult()
        res.register_advancement()
        self.advance() # consume 'class'

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected class name"
            ))

        class_name_tok = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{' after class name"
            ))

        res.register_advancement()
        self.advance()

        members = []
        while self.current_tok.type != TT_RBRACE and self.current_tok.type != TT_EOF:
            # Skip optional semicolons between members
            while self.current_tok.type == TT_SEMI:
                res.register_advancement()
                self.advance()

            if self.current_tok.matches(TT_KEYWORD, 'func'):
                member = res.register(self.func_def_statement())
                if res.error:
                    return res
                members.append(member)
            elif self.current_tok.type == TT_RBRACE:
                break # End of class body
            else:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'func' member or '}' in class definition"
                ))

        if self.current_tok.type != TT_RBRACE:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '}' to close class body"
            ))

        res.register_advancement()
        self.advance()

        return res.success(ClassDefNode(class_name_tok, members))

    def return_statement(self) -> ParseResult:
        """Parse return statement."""
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()
        res.register_advancement()
        self.advance() # consume 'return'

        expr = None
        if self.current_tok.type != TT_SEMI:
            expr = res.register(self.expr())
            if res.error:
                return res

        return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

    def expr(self) -> ParseResult:
        """Parse expression with assignment."""
        res = ParseResult()
        left = res.register(self.bin_op(self.comp, (TT_EE, TT_NE)))
        if res.error:
            return res

        if self.current_tok.type == TT_EQ:
            res.register_advancement()
            self.advance()  # Consume '='

            if not isinstance(left, (VarAccessNode, MemberAccessNode)):
                return res.failure(ParseError(
                    left.pos_start, left.pos_end,
                    "Invalid assignment target"
                ))

            right = res.register(self.expr())
            if res.error:
                return res
            
            return res.success(AssignNode(left, right))

        return res.success(left)

    def comp(self) -> ParseResult:
        """Parse comparison expressions."""
        return self.bin_op(self.term, (TT_LT, TT_GT, TT_LTE, TT_GTE))

    def term(self) -> ParseResult:
        """Parse addition and subtraction."""
        return self.bin_op(self.factor, (TT_PLUS, TT_MINUS))

    def factor(self) -> ParseResult:
        """Parse multiplication and division."""
        return self.bin_op(self.unary, (TT_MUL, TT_DIV))

    def unary(self) -> ParseResult:
        """Parse unary expressions."""
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            node = res.register(self.unary())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, node))

        return self.call_or_member()

    def call_or_member(self) -> ParseResult:
        """Parse function calls and member access."""
        res = ParseResult()
        node = res.register(self.primary())
        if res.error:
            return res

        while True:
            if self.current_tok.type == TT_LPAREN:
                # Function call
                res.register_advancement()
                self.advance()
                args = []

                if self.current_tok.type != TT_RPAREN:
                    args.append(res.register(self.expr()))
                    if res.error:
                        return res

                    while self.current_tok.type == TT_COMMA:
                        res.register_advancement()
                        self.advance()
                        args.append(res.register(self.expr()))
                        if res.error:
                            return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(ParseError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')' after arguments"
                    ))

                res.register_advancement()
                self.advance()
                node = CallNode(node, args)
                continue

            if self.current_tok.type == TT_DOT:
                # Member access
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(ParseError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier after '.'"
                    ))

                member_tok = self.current_tok
                res.register_advancement()
                self.advance()
                node = MemberAccessNode(node, member_tok)
                continue

            break

        return res.success(node)

    def primary(self) -> ParseResult:
        """Parse primary expressions."""
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        if tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        if tok.type == TT_KEYWORD and tok.value in ('true', 'false'):
            res.register_advancement()
            self.advance()
            return res.success(BoolNode(tok))

        if tok.type == TT_KEYWORD and tok.value == 'null':
            res.register_advancement()
            self.advance()
            return res.success(NullNode(tok))

        if tok.type == TT_KEYWORD and tok.value == 'this':
            res.register_advancement()
            self.advance()
            return res.success(ThisNode(tok))

        if tok.matches(TT_KEYWORD, 'new'):
            return self.new_expression()

        if tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        if tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type != TT_RPAREN:
                return res.failure(ParseError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
            res.register_advancement()
            self.advance()
            return res.success(expr)

        return res.failure(ParseError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, string, identifier, 'true', 'false', 'null', or '('"))

    def bin_op(self, func, ops):
        """Parse binary operations with the given precedence."""
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    def new_expression(self) -> ParseResult:
        """Parse a 'new' expression for object instantiation."""
        res = ParseResult()
        res.register_advancement()
        self.advance() # consume 'new'

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected class name after 'new'"
            ))

        class_name_tok = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_LPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '(' after class name"
            ))

        res.register_advancement()
        self.advance()

        arg_nodes = []
        if self.current_tok.type != TT_RPAREN:
            arg_nodes.append(res.register(self.expr()))
            if res.error:
                return res

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res

        if self.current_tok.type != TT_RPAREN:
            return res.failure(ParseError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ')' after arguments"
            ))

        res.register_advancement()
        self.advance()

        return res.success(NewNode(class_name_tok, arg_nodes))
