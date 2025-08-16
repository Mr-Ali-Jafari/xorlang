"""
XorLang Abstract Syntax Tree Nodes

This module contains all AST node classes used by the parser
to represent the structure of XorLang programs.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Any
from abc import ABC, abstractmethod

from .lexer import Token


class ASTNode(ABC):
    """Base class for all AST nodes."""
    
    def __init__(self):
        self.pos_start = None
        self.pos_end = None


# Literal Nodes
class NumberNode(ASTNode):
    """Represents numeric literals (int and float)."""
    
    def __init__(self, tok):
        super().__init__()
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    
    def __repr__(self):
        return f"{self.tok}"


class StringNode(ASTNode):
    """Represents string literals."""
    
    def __init__(self, tok):
        super().__init__()
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    
    def __repr__(self):
        return f"{self.tok}"


class BoolNode(ASTNode):
    """Represents boolean literals (true/false)."""
    
    def __init__(self, tok):
        super().__init__()
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    
    def __repr__(self):
        return f"{self.tok}"


@dataclass
class NullNode(ASTNode):
    """Represents a null literal."""
    
    def __init__(self, tok):
        super().__init__()
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    
    def __repr__(self):
        return f"{self.tok}"


@dataclass
class ContinueNode(ASTNode):
    """Represents a 'continue' statement."""
    tok: Token


@dataclass
class BreakNode(ASTNode):
    """Represents a 'break' statement."""
    tok: Token


@dataclass
class ThisNode(ASTNode):
    """Represents the 'this' keyword."""
    
    def __init__(self, tok):
        super().__init__()
        self.tok = tok
        self.pos_start = tok.pos_start
        self.pos_end = tok.pos_end
    
    def __repr__(self):
        return f"{self.tok}"


# Variable Nodes
class VarAccessNode(ASTNode):
    """Represents variable access."""
    
    def __init__(self, name_tok):
        super().__init__()
        self.name_tok = name_tok
        self.pos_start = name_tok.pos_start
        self.pos_end = name_tok.pos_end
    
    def __repr__(self):
        return f"{self.name_tok}"


class MemberAccessNode(ASTNode):
    """Represents member access (object.member)."""
    
    def __init__(self, obj_node, member_tok):
        super().__init__()
        self.obj_node = obj_node
        self.member_tok = member_tok
        self.pos_start = obj_node.pos_start
        self.pos_end = member_tok.pos_end
    
    def __repr__(self):
        return f"({self.obj_node}.{self.member_tok.value})"


class VarDeclNode(ASTNode):
    """Represents variable declaration."""
    
    def __init__(self, name_tok, value_node=None):
        super().__init__()
        self.name_tok = name_tok
        self.value_node = value_node
        self.pos_start = name_tok.pos_start
        self.pos_end = (value_node.pos_end if value_node else name_tok.pos_end)
    
    def __repr__(self):
        if self.value_node:
            return f"(var {self.name_tok.value} = {self.value_node})"
        return f"(var {self.name_tok.value})"


@dataclass
class AssignNode(ASTNode):
    """Represents an assignment to a variable or a property."""
    target_node: ASTNode
    expr_node: ASTNode

    def __init__(self, target_node, expr_node):
        super().__init__()
        self.target_node = target_node
        self.expr_node = expr_node
        self.pos_start = target_node.pos_start
        self.pos_end = expr_node.pos_end
    
    def __repr__(self):
        return f"({self.target_node} = {self.expr_node})"


# Expression Nodes
class BinOpNode(ASTNode):
    """Represents binary operations (+, -, *, /, ==, etc.)."""
    
    def __init__(self, left, op_tok, right):
        super().__init__()
        self.left = left
        self.op_tok = op_tok
        self.right = right
        self.pos_start = left.pos_start
        self.pos_end = right.pos_end
    
    def __repr__(self):
        return f"({self.left} {self.op_tok} {self.right})"


class UnaryOpNode(ASTNode):
    """Represents unary operations (+expr, -expr)."""
    
    def __init__(self, op_tok, node):
        super().__init__()
        self.op_tok = op_tok
        self.node = node
        self.pos_start = op_tok.pos_start
        self.pos_end = node.pos_end
    
    def __repr__(self):
        return f"({self.op_tok}{self.node})"


class CallNode(ASTNode):
    """Represents function calls."""
    
    def __init__(self, callee_node, arg_nodes):
        super().__init__()
        self.callee_node = callee_node
        self.arg_nodes = arg_nodes
        self.pos_start = callee_node.pos_start
        self.pos_end = (arg_nodes[-1].pos_end if arg_nodes else callee_node.pos_end)
    
    def __repr__(self):
        return f"({self.callee_node}({', '.join(map(str, self.arg_nodes))}))"


# Statement Nodes
class BlockNode(ASTNode):
    """Represents a block of statements."""
    
    def __init__(self, statements, pos_start, pos_end):
        super().__init__()
        self.statements = statements
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def __repr__(self):
        return '{ ' + ' '.join(map(str, self.statements)) + ' }'


@dataclass
class ExpressionStatementNode(ASTNode):
    """Represents a statement that is just an expression."""
    expr: ASTNode

    def __init__(self, expr):
        self.expr = expr
        if expr is not None and hasattr(expr, 'pos_start'):
            self.pos_start = expr.pos_start
            self.pos_end = expr.pos_end
        else:
            self.pos_start = None
            self.pos_end = None
    
    def __repr__(self):
        return f"ExprStmt({self.expr})"


class IfNode(ASTNode):
    """Represents if/else statements."""
    
    def __init__(self, cases, else_case=None):
        super().__init__()
        self.cases = cases  # List of (condition, body) tuples
        self.else_case = else_case
        
        if cases:
            self.pos_start = cases[0][0].pos_start
            self.pos_end = (else_case.pos_end if else_case else cases[-1][1].pos_end)
    
    def __repr__(self):
        result = "if"
        for i, (cond, body) in enumerate(self.cases):
            if i == 0:
                result += f" ({cond}) {body}"
            else:
                result += f" else if ({cond}) {body}"
        if self.else_case:
            result += f" else {self.else_case}"
        return result


class WhileNode(ASTNode):
    """Represents while loops."""
    
    def __init__(self, cond_node, body_block):
        super().__init__()
        self.cond_node = cond_node
        self.body_block = body_block
        self.pos_start = cond_node.pos_start
        self.pos_end = body_block.pos_end
    
    def __repr__(self):
        return f"while ({self.cond_node}) {self.body_block}"


class ForNode(ASTNode):
    """Represents for loops."""
    
    def __init__(self, init_node, cond_node, update_node, body_block):
        super().__init__()
        self.init_node = init_node
        self.cond_node = cond_node
        self.update_node = update_node
        self.body_block = body_block
        
        self.pos_start = init_node.pos_start if init_node else cond_node.pos_start
        self.pos_end = body_block.pos_end
    
    def __repr__(self):
        return f"for ({self.init_node}; {self.cond_node}; {self.update_node}) {self.body_block}"


class FuncDefNode(ASTNode):
    """Represents function definitions."""
    
    def __init__(self, name_tok, arg_name_toks, body_block):
        super().__init__()
        self.name_tok = name_tok
        self.arg_name_toks = arg_name_toks
        self.body_block = body_block
        
        self.pos_start = name_tok.pos_start if name_tok else body_block.pos_start
        self.pos_end = body_block.pos_end
    
    def __repr__(self):
        args = ', '.join([tok.value for tok in self.arg_name_toks])
        name = self.name_tok.value if self.name_tok else "<anonymous>"
        return f"func {name}({args}) {self.body_block}"


class ReturnNode(ASTNode):
    """Represents return statements."""
    
    def __init__(self, expr_node, pos_start, pos_end):
        super().__init__()
        self.expr_node = expr_node
        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def __repr__(self):
        if self.expr_node:
            return f"return {self.expr_node}"
        return "return"


class NewNode(ASTNode):
    """Represents object instantiation using 'new'."""
    
    def __init__(self, class_name_tok, arg_nodes):
        super().__init__()
        self.class_name_tok = class_name_tok
        self.arg_nodes = arg_nodes
        self.pos_start = class_name_tok.pos_start
        self.pos_end = (arg_nodes[-1].pos_end if arg_nodes else class_name_tok.pos_end)


class ClassDefNode(ASTNode):
    """Represents class definition."""
    
    def __init__(self, name_tok, members):
        super().__init__()
        self.name_tok = name_tok
        self.members = members  # List of FuncDefNode
        
        self.pos_start = name_tok.pos_start
        self.pos_end = members[-1].pos_end if members else name_tok.pos_end
    
    def __repr__(self):
        return f"class {self.name_tok.value} {{ {len(self.members)} members }}"


class ImportNode(ASTNode):
    """Represents import statements."""
    
    def __init__(self, module_name):
        super().__init__()
        self.module_name = module_name
        self.pos_start = module_name.pos_start
        self.pos_end = module_name.pos_end
    
    def __repr__(self):
        return f"import({self.module_name.value})"
