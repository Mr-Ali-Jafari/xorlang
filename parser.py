# XorLang Parser
from lexer import TT_INT, TT_FLOAT, TT_STRING, TT_IDENTIFIER, TT_KEYWORD, TT_PLUS, TT_MINUS, TT_MUL, TT_DIV, TT_LPAREN, TT_RPAREN, TT_LBRACE, TT_RBRACE, TT_COMMA, TT_SEMI, TT_DOT, TT_EQ, TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE

class ParseError:
    def __init__(self, pos_start, pos_end, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.details = details

    def as_string(self):
        result = f"SyntaxError: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}\n"
        line_text = self.pos_start.ftext.split('\n')[self.pos_start.ln] if self.pos_start.ftext else ''
        result += line_text + '\n'
        result += ' ' * self.pos_start.col + '^'
        return result

# AST Nodes
class NumberNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    def __repr__(self): return f"{self.tok}"

class StringNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    def __repr__(self): return f"{self.tok}"

class BoolNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    def __repr__(self): return f"{self.tok}"

class NullNode:
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    def __repr__(self): return f"{self.tok}"

class VarAccessNode:
    def __init__(self, name_tok):
        self.name_tok = name_tok
        self.pos_start = name_tok.pos_start
        self.pos_end = name_tok.pos_end
    def __repr__(self): return f"{self.name_tok}"

class MemberAccessNode:
    def __init__(self, obj_node, member_tok):
        self.obj_node = obj_node
        self.member_tok = member_tok
        self.pos_start = obj_node.pos_start
        self.pos_end = member_tok.pos_end
    def __repr__(self): return f"({self.obj_node}.{self.member_tok.value})"

class VarDeclNode:
    def __init__(self, name_tok, value_node=None):
        self.name_tok = name_tok
        self.value_node = value_node
        self.pos_start = name_tok.pos_start
        self.pos_end = (value_node.pos_end if value_node else name_tok.pos_end)
    def __repr__(self):
        if self.value_node: return f"(var {self.name_tok.value} = {self.value_node})"
        return f"(var {self.name_tok.value})"

class VarAssignNode:
    def __init__(self, name_tok, value_node):
        self.name_tok = name_tok
        self.value_node = value_node
        self.pos_start = name_tok.pos_start
        self.pos_end = value_node.pos_end
    def __repr__(self): return f"({self.name_tok.value} = {self.value_node})"

class BinOpNode:
    def __init__(self, left, op_tok, right):
        self.left = left
        self.op_tok = op_tok
        self.right = right
        self.pos_start = left.pos_start
        self.pos_end = right.pos_end
    def __repr__(self): return f"({self.left} {self.op_tok} {self.right})"

class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = op_tok.pos_start
        self.pos_end = node.pos_end
    def __repr__(self): return f"({self.op_tok}{self.node})"

class CallNode:
    def __init__(self, callee_node, arg_nodes):
        self.callee_node = callee_node
        self.arg_nodes = arg_nodes
        self.pos_start = callee_node.pos_start
        self.pos_end = (arg_nodes[-1].pos_end if arg_nodes else callee_node.pos_end)
    def __repr__(self): return f"({self.callee_node}({', '.join(map(str, self.arg_nodes))}))"

class BlockNode:
    def __init__(self, statements):
        self.statements = statements
        if statements:
            self.pos_start = statements[0].pos_start
            self.pos_end = statements[-1].pos_end
        else:
            self.pos_start = None
            self.pos_end = None
    def __repr__(self): return '{ ' + ' '.join(map(str, self.statements)) + ' }'

class IfNode:
    def __init__(self, cond_node, then_block, else_node=None):
        self.cond_node = cond_node
        self.then_block = then_block
        self.else_node = else_node
        self.pos_start = cond_node.pos_start
        self.pos_end = (else_node.pos_end if else_node else then_block.pos_end)
    def __repr__(self):
        if self.else_node: return f"(if {self.cond_node} {self.then_block} else {self.else_node})"
        return f"(if {self.cond_node} {self.then_block})"

class WhileNode:
    def __init__(self, cond_node, body_block):
        self.cond_node = cond_node
        self.body_block = body_block
        self.pos_start = cond_node.pos_start
        self.pos_end = body_block.pos_end
    def __repr__(self): return f"(while {self.cond_node} {self.body_block})"

class ForNode:
    def __init__(self, init_node, cond_node, update_node, body_block):
        self.init_node = init_node
        self.cond_node = cond_node
        self.update_node = update_node
        self.body_block = body_block
        first = next(n for n in [init_node, cond_node, update_node, body_block] if n is not None)
        last = next(n for n in [body_block, update_node, cond_node, init_node] if n is not None)
        self.pos_start = first.pos_start
        self.pos_end = last.pos_end
    def __repr__(self): return f"(for {self.init_node}; {self.cond_node}; {self.update_node} {self.body_block})"

class FuncDefNode:
    def __init__(self, name_tok, arg_name_toks, body_block):
        self.name_tok = name_tok
        self.arg_name_toks = arg_name_toks
        self.body_block = body_block
        self.pos_start = (name_tok.pos_start if name_tok else (arg_name_toks[0].pos_start if arg_name_toks else body_block.pos_start))
        self.pos_end = body_block.pos_end
    def __repr__(self):
        name = self.name_tok.value if self.name_tok else '<anon>'
        params = ','.join([t.value for t in self.arg_name_toks])
        return f"(func {name}({params}) {self.body_block})"

class ReturnNode:
    def __init__(self, expr_node=None):
        self.expr_node = expr_node
        self.pos_start = expr_node.pos_start if expr_node else None
        self.pos_end = expr_node.pos_end if expr_node else None
    def __repr__(self): return f"(return {self.expr_node})" if self.expr_node else "(return)"

class ClassDefNode:
    def __init__(self, name_tok, members):
        self.name_tok = name_tok
        self.members = members  # list of FuncDefNode (for now)
        self.pos_start = name_tok.pos_start
        self.pos_end = (members[-1].pos_end if members else name_tok.pos_end)
    def __repr__(self):
        return f"(class {self.name_tok.value} {{ {' '.join(map(str, self.members))} }})"

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
    def register_advancement(self): self.advance_count += 1
    def register(self, res):
        if isinstance(res, ParseResult):
            self.advance_count += res.advance_count
            if res.error: self.error = res.error
            return res.node
        return res
    def success(self, node): self.node = node; return self
    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = ParseResult()
        statements = []
        while self.current_tok.type != 'EOF':
            if self.current_tok.type == TT_SEMI:
                res.register_advancement(); self.advance(); continue
            stmt = res.register(self.statement())
            if res.error: return res
            statements.append(stmt)
            if self.current_tok.type == TT_SEMI:
                res.register_advancement(); self.advance()
            else:
                if self.current_tok.type not in ('EOF', TT_RBRACE):
                    return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ';' or end of statement"))
        return res.success(BlockNode(statements))

    def statement(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type == TT_KEYWORD and tok.value == 'var':
            res.register_advancement(); self.advance()
            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, 'Expected identifier'))
            name_tok = self.current_tok
            res.register_advancement(); self.advance()
            value_node = None
            if self.current_tok.type == TT_EQ:
                res.register_advancement(); self.advance()
                value_node = res.register(self.expr())
                if res.error: return res
            return res.success(VarDeclNode(name_tok, value_node))
        if tok.type == TT_KEYWORD and tok.value == 'func':
            node = res.register(self.func_def())
            if res.error: return res
            return res.success(node)
        if tok.type == TT_KEYWORD and tok.value == 'class':
            node = res.register(self.class_def())
            if res.error: return res
            return res.success(node)
        if tok.type == TT_KEYWORD and tok.value == 'return':
            res.register_advancement(); self.advance()
            expr_node = None
            if self.current_tok.type not in (TT_SEMI, TT_RBRACE, 'EOF'):
                expr_node = res.register(self.expr())
                if res.error: return res
            return res.success(ReturnNode(expr_node))
        if tok.type == TT_KEYWORD and tok.value == 'if':
            node = res.register(self.if_statement())
            if res.error: return res
            return res.success(node)
        if tok.type == TT_KEYWORD and tok.value == 'while':
            node = res.register(self.while_statement())
            if res.error: return res
            return res.success(node)
        if tok.type == TT_KEYWORD and tok.value == 'for':
            node = res.register(self.for_statement())
            if res.error: return res
            return res.success(node)
        # expression or assignment
        expr = res.register(self.expr())
        if res.error: return res
        if self.current_tok.type == TT_EQ and isinstance(expr, VarAccessNode):
            res.register_advancement(); self.advance()
            value = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(expr.name_tok, value))
        return res.success(expr)

    def func_def(self):
        res = ParseResult()
        res.register_advancement(); self.advance()  # consume 'func'
        name_tok = None
        if self.current_tok.type == TT_IDENTIFIER:
            name_tok = self.current_tok
            res.register_advancement(); self.advance()
        if self.current_tok.type != TT_LPAREN:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '(' after function name"))
        res.register_advancement(); self.advance()
        args = []
        if self.current_tok.type == TT_IDENTIFIER:
            args.append(self.current_tok)
            res.register_advancement(); self.advance()
            while self.current_tok.type == TT_COMMA:
                res.register_advancement(); self.advance()
                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, 'Expected identifier'))
                args.append(self.current_tok)
                res.register_advancement(); self.advance()
        if self.current_tok.type != TT_RPAREN:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')' after parameters"))
        res.register_advancement(); self.advance()
        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{' before function body"))
        body = res.register(self.block())
        if res.error: return res
        return res.success(FuncDefNode(name_tok, args, body))

    def class_def(self):
        res = ParseResult()
        res.register_advancement(); self.advance()  # consume 'class'
        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, 'Expected class name'))
        name_tok = self.current_tok
        res.register_advancement(); self.advance()
        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{' before class body"))
        res.register_advancement(); self.advance()
        members = []
        while self.current_tok.type != TT_RBRACE and self.current_tok.type != 'EOF':
            if self.current_tok.type == TT_SEMI:
                res.register_advancement(); self.advance(); continue
            if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'func':
                fn = res.register(self.func_def())
                if res.error: return res
                members.append(fn)
                if self.current_tok.type == TT_SEMI:
                    res.register_advancement(); self.advance()
                continue
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, 'Only function members are allowed in class body'))
        if self.current_tok.type != TT_RBRACE:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}' after class body"))
        res.register_advancement(); self.advance()
        return res.success(ClassDefNode(name_tok, members))

    def block(self):
        res = ParseResult()
        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{'"))
        res.register_advancement(); self.advance()
        statements = []
        while self.current_tok.type != TT_RBRACE and self.current_tok.type != 'EOF':
            if self.current_tok.type == TT_SEMI:
                res.register_advancement(); self.advance(); continue
            stmt = res.register(self.statement())
            if res.error: return res
            statements.append(stmt)
            if self.current_tok.type == TT_SEMI:
                res.register_advancement(); self.advance()
        if self.current_tok.type != TT_RBRACE:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '}'"))
        res.register_advancement(); self.advance()
        return res.success(BlockNode(statements))

    def if_statement(self):
        res = ParseResult()
        res.register_advancement(); self.advance()  # 'if'
        if self.current_tok.type != TT_LPAREN:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '(' after 'if'"))
        res.register_advancement(); self.advance()
        cond = res.register(self.expr())
        if res.error: return res
        if self.current_tok.type != TT_RPAREN:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')' after condition"))
        res.register_advancement(); self.advance()
        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{' to start if-body"))
        then_block = res.register(self.block())
        if res.error: return res
        else_node = None
        if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'else':
            res.register_advancement(); self.advance()
            if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'if':
                else_node = res.register(self.if_statement())
                if res.error: return res
            else:
                if self.current_tok.type != TT_LBRACE:
                    return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{' to start else-body"))
                else_node = res.register(self.block())
                if res.error: return res
        return res.success(IfNode(cond, then_block, else_node))

    def while_statement(self):
        res = ParseResult()
        res.register_advancement(); self.advance()
        if self.current_tok.type != TT_LPAREN:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '(' after 'while'"))
        res.register_advancement(); self.advance()
        cond = res.register(self.expr())
        if res.error: return res
        if self.current_tok.type != TT_RPAREN:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')' after condition"))
        res.register_advancement(); self.advance()
        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{' to start while-body"))
        body = res.register(self.block())
        if res.error: return res
        return res.success(WhileNode(cond, body))

    def for_statement(self):
        res = ParseResult()
        res.register_advancement(); self.advance()
        if self.current_tok.type != TT_LPAREN:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '(' after 'for'"))
        res.register_advancement(); self.advance()
        init = None
        if self.current_tok.type != TT_SEMI:
            if self.current_tok.type == TT_KEYWORD and self.current_tok.value == 'var':
                res.register_advancement(); self.advance()
                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, 'Expected identifier'))
                name_tok = self.current_tok
                res.register_advancement(); self.advance()
                init_value = None
                if self.current_tok.type == TT_EQ:
                    res.register_advancement(); self.advance()
                    init_value = res.register(self.expr())
                    if res.error: return res
                init = VarDeclNode(name_tok, init_value)
            else:
                init = res.register(self.expr_with_optional_assignment())
                if res.error: return res
        if self.current_tok.type != TT_SEMI:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ';' after for-init"))
        res.register_advancement(); self.advance()
        cond = None
        if self.current_tok.type != TT_SEMI:
            cond = res.register(self.expr())
            if res.error: return res
        if self.current_tok.type != TT_SEMI:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ';' after for-condition"))
        res.register_advancement(); self.advance()
        update = None
        if self.current_tok.type != TT_RPAREN:
            update = res.register(self.expr_with_optional_assignment())
            if res.error: return res
        if self.current_tok.type != TT_RPAREN:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')' after for-update"))
        res.register_advancement(); self.advance()
        if self.current_tok.type != TT_LBRACE:
            return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '{' to start for-body"))
        body = res.register(self.block())
        if res.error: return res
        return res.success(ForNode(init, cond, update, body))

    def expr_with_optional_assignment(self):
        res = ParseResult()
        left = res.register(self.expr())
        if res.error: return res
        if self.current_tok.type == TT_EQ and isinstance(left, VarAccessNode):
            res.register_advancement(); self.advance()
            value = res.register(self.expr())
            if res.error: return res
            return res.success(VarAssignNode(left.name_tok, value))
        return res.success(left)

    def expr(self):
        return self.bin_op(self.comp, (TT_EE, TT_NE))
    def comp(self):
        return self.bin_op(self.term, (TT_LT, TT_GT, TT_LTE, TT_GTE))
    def term(self):
        return self.bin_op(self.factor, (TT_PLUS, TT_MINUS))
    def factor(self):
        return self.bin_op(self.unary, (TT_MUL, TT_DIV))

    def unary(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement(); self.advance()
            node = res.register(self.unary())
            if res.error: return res
            return res.success(UnaryOpNode(tok, node))
        return self.call_or_member()

    def call_or_member(self):
        res = ParseResult()
        node = res.register(self.primary())
        if res.error: return res
        while True:
            if self.current_tok.type == TT_LPAREN:
                # call
                res.register_advancement(); self.advance()
                args = []
                if self.current_tok.type != TT_RPAREN:
                    args.append(res.register(self.expr()))
                    if res.error: return res
                    while self.current_tok.type == TT_COMMA:
                        res.register_advancement(); self.advance()
                        args.append(res.register(self.expr()))
                        if res.error: return res
                if self.current_tok.type != TT_RPAREN:
                    return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')' after arguments"))
                res.register_advancement(); self.advance()
                node = CallNode(node, args)
                continue
            if self.current_tok.type == TT_DOT:
                res.register_advancement(); self.advance()
                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected identifier after '.'"))
                member_tok = self.current_tok
                res.register_advancement(); self.advance()
                node = MemberAccessNode(node, member_tok)
                continue
            break
        return res.success(node)

    def primary(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement(); self.advance(); return res.success(NumberNode(tok))
        if tok.type == TT_STRING:
            res.register_advancement(); self.advance(); return res.success(StringNode(tok))
        if tok.type == TT_KEYWORD and tok.value in ('true','false'):
            res.register_advancement(); self.advance(); return res.success(BoolNode(tok))
        if tok.type == TT_KEYWORD and tok.value == 'null':
            res.register_advancement(); self.advance(); return res.success(NullNode(tok))
        if tok.type == TT_IDENTIFIER:
            res.register_advancement(); self.advance(); return res.success(VarAccessNode(tok))
        if tok.type == TT_LPAREN:
            res.register_advancement(); self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type != TT_RPAREN:
                return res.failure(ParseError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected ')'"))
            res.register_advancement(); self.advance()
            return res.success(expr)
        return res.failure(ParseError(tok.pos_start, tok.pos_end, "Expected int, float, string, identifier, 'true', 'false', 'null', or '('"))

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register_advancement(); self.advance()
            right = res.register(func())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
        return res.success(left) 