# XorLang Interpreter
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os
import sys
import time as _py_time
from urllib import request as _py_request
from urllib import error as _py_error

from parser import (
    NumberNode, StringNode, BoolNode, NullNode,
    VarAccessNode, VarDeclNode, VarAssignNode,
    BinOpNode, UnaryOpNode, CallNode, BlockNode,
    IfNode, WhileNode, ForNode, FuncDefNode, ReturnNode, ClassDefNode,
    MemberAccessNode, ParseError
)

class RuntimeError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

@dataclass
class FunctionValue:
    name: Optional[str]
    params: List[str]
    body: BlockNode
    closure: 'Environment'

@dataclass
class ClassValue:
    name: str
    members: Dict[str, Any]  # functions or constants in future

class ReturnSignal(Exception):
    def __init__(self, value: Any):
        self.value = value

class Environment:
    def __init__(self, parent: Optional['Environment']=None):
        self.parent = parent
        self.values: Dict[str, Any] = {}

    def define(self, name: str, value: Any):
        self.values[name] = value

    def set(self, name: str, value: Any):
        env = self.resolve(name)
        if env is None:
            # allow implicit definition on assignment
            self.values[name] = value
        else:
            env.values[name] = value

    def get(self, name: str) -> Any:
        env = self.resolve(name)
        if env is None:
            raise RuntimeError(f"Undefined variable '{name}'")
        return env.values[name]

    def resolve(self, name: str) -> Optional['Environment']:
        if name in self.values:
            return self
        if self.parent:
            return self.parent.resolve(name)
        return None

class Interpreter:
    def __init__(self):
        self.globals = Environment()
        self.env = self.globals
        self._install_builtins()

    def _install_builtins(self):
        def builtin_print(*args):
            print(*args)
        self.globals.define('print', ('builtin', 'print', builtin_print))

        # Time built-ins
        def builtin_time_now():
            return _py_time.time()
        def builtin_time_ms():
            return int(_py_time.time() * 1000)
        def builtin_sleep(seconds):
            # best-effort convert
            try:
                _py_time.sleep(float(seconds))
            except Exception as e:
                raise RuntimeError(f"sleep error: {e}")
        self.globals.define('time_now', ('builtin', 'time_now', builtin_time_now))
        self.globals.define('time_ms', ('builtin', 'time_ms', builtin_time_ms))
        self.globals.define('sleep', ('builtin', 'sleep', builtin_sleep))

        # HTTP built-ins
        def builtin_http_get(url):
            try:
                with _py_request.urlopen(str(url)) as resp:
                    data = resp.read()
                    try:
                        return data.decode('utf-8')
                    except Exception:
                        # return binary as latin-1 text fallback
                        return data.decode('latin-1', errors='ignore')
            except _py_error.HTTPError as e:
                # include status code and message
                raise RuntimeError(f"HTTP GET error {e.code}: {e.reason}")
            except _py_error.URLError as e:
                raise RuntimeError(f"HTTP GET URL error: {e.reason}")
            except Exception as e:
                raise RuntimeError(f"HTTP GET unexpected error: {e}")
        def builtin_http_get_status(url):
            try:
                with _py_request.urlopen(str(url)) as resp:
                    return int(getattr(resp, 'status', 200))
            except _py_error.HTTPError as e:
                return int(e.code)
            except _py_error.URLError:
                return 0
            except Exception:
                return 0
        self.globals.define('http_get', ('builtin', 'http_get', builtin_http_get))
        self.globals.define('http_get_status', ('builtin', 'http_get_status', builtin_http_get_status))

    def eval(self, node, env: Optional[Environment]=None):
        if env is None:
            env = self.env
        method = f'_eval_{type(node).__name__}'
        if not hasattr(self, method):
            raise RuntimeError(f'No evaluator for node {type(node).__name__}')
        return getattr(self, method)(node, env)

    def _eval_BlockNode(self, node: BlockNode, env: Environment):
        result = None
        for stmt in node.statements:
            result = self.eval(stmt, env)
        return result

    def _eval_NumberNode(self, node: NumberNode, env: Environment):
        return node.tok.value

    def _eval_StringNode(self, node: StringNode, env: Environment):
        return node.tok.value

    def _eval_BoolNode(self, node: BoolNode, env: Environment):
        return True if node.tok.value == 'true' else False

    def _eval_NullNode(self, node: NullNode, env: Environment):
        return None

    def _eval_VarAccessNode(self, node: VarAccessNode, env: Environment):
        return env.get(node.name_tok.value)

    def _eval_MemberAccessNode(self, node: MemberAccessNode, env: Environment):
        obj = self.eval(node.obj_node, env)
        if isinstance(obj, ClassValue):
            name = node.member_tok.value
            if name not in obj.members:
                raise RuntimeError(f"Class '{obj.name}' has no member '{name}'")
            return obj.members[name]
        raise RuntimeError('Member access only supported on classes for now')

    def _eval_VarDeclNode(self, node: VarDeclNode, env: Environment):
        value = self.eval(node.value_node, env) if node.value_node else None
        env.define(node.name_tok.value, value)
        return value

    def _eval_VarAssignNode(self, node: VarAssignNode, env: Environment):
        value = self.eval(node.value_node, env)
        env.set(node.name_tok.value, value)
        return value

    def _eval_UnaryOpNode(self, node: UnaryOpNode, env: Environment):
        val = self.eval(node.node, env)
        if node.op_tok.type == 'PLUS':
            return +val
        if node.op_tok.type == 'MINUS':
            return -val
        raise RuntimeError('Unknown unary operator')

    def _eval_BinOpNode(self, node: BinOpNode, env: Environment):
        l = self.eval(node.left, env)
        r = self.eval(node.right, env)
        t = node.op_tok.type
        if t == 'PLUS': return l + r
        if t == 'MINUS': return l - r
        if t == 'MUL': return l * r
        if t == 'DIV': return l / r
        if t == 'EE': return l == r
        if t == 'NE': return l != r
        if t == 'LT': return l < r
        if t == 'GT': return l > r
        if t == 'LTE': return l <= r
        if t == 'GTE': return l >= r
        raise RuntimeError('Unknown binary operator')

    def _eval_CallNode(self, node: CallNode, env: Environment):
        callee = self.eval(node.callee_node, env)
        args = [self.eval(a, env) for a in node.arg_nodes]
        # builtins
        if isinstance(callee, tuple) and callee[0] == 'builtin':
            return callee[2](*args)
        # function value
        if isinstance(callee, FunctionValue):
            if len(args) != len(callee.params):
                raise RuntimeError(f"Function expected {len(callee.params)} args, got {len(args)}")
            local = Environment(callee.closure)
            for name, val in zip(callee.params, args):
                local.define(name, val)
            try:
                self.eval(callee.body, local)
            except ReturnSignal as rs:
                return rs.value
            return None
        raise RuntimeError('Can only call functions')

    def _eval_IfNode(self, node: IfNode, env: Environment):
        cond = self.eval(node.cond_node, env)
        if cond:
            return self.eval(node.then_block, env)
        if node.else_node:
            return self.eval(node.else_node, env)
        return None

    def _eval_WhileNode(self, node: WhileNode, env: Environment):
        result = None
        while self.eval(node.cond_node, env):
            result = self.eval(node.body_block, env)
        return result

    def _eval_ForNode(self, node: ForNode, env: Environment):
        result = None
        loop_env = Environment(env)
        if node.init_node is not None:
            self.eval(node.init_node, loop_env)
        while True:
            if node.cond_node is not None and not self.eval(node.cond_node, loop_env):
                break
            result = self.eval(node.body_block, loop_env)
            if node.update_node is not None:
                self.eval(node.update_node, loop_env)
            if node.cond_node is None:
                # Prevent infinite loop if no condition; treat as true for one iteration then break
                break
        return result

    def _eval_FuncDefNode(self, node: FuncDefNode, env: Environment):
        name = node.name_tok.value if node.name_tok else None
        params = [t.value for t in node.arg_name_toks]
        fn = FunctionValue(name, params, node.body_block, env)
        if name:
            env.define(name, fn)
        return fn

    def _eval_ReturnNode(self, node: ReturnNode, env: Environment):
        val = self.eval(node.expr_node, env) if node.expr_node else None
        raise ReturnSignal(val)

    def _eval_ClassDefNode(self, node: ClassDefNode, env: Environment):
        # Class environment inherits from current env so methods can see globals/builtins
        class_env = Environment(env)
        for m in node.members:
            fv = self._eval_FuncDefNode(m, class_env)
            if fv.name:
                class_env.define(fv.name, fv)
        cls = ClassValue(node.name_tok.value, class_env.values)
        env.define(node.name_tok.value, cls)
        return cls

# Run helper
from lexer import run as lex_run
from parser import Parser

def _find_stdlib_prelude_path() -> Optional[str]:
    # Prefer packaged stdlib, then XORLANG_HOME, then local
    candidates: List[str] = []
    # 1) PyInstaller _MEIPASS
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        candidates.append(os.path.join(meipass, 'stdlib', 'prelude.xor'))
    # 2) XORLANG_HOME environment variable
    home = os.environ.get('XORLANG_HOME')
    if home:
        candidates.append(os.path.join(home, 'stdlib', 'prelude.xor'))
    # 3) Next to this file
    here = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(here, 'stdlib', 'prelude.xor'))
    # 4) Current working directory stdlib
    candidates.append(os.path.join(os.getcwd(), 'stdlib', 'prelude.xor'))
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None

def _load_and_eval(interpreter: Interpreter, path: str, src: str):
    tokens, lex_err = lex_run(path, src)
    if lex_err:
        return None, lex_err.as_string()
    parser = Parser(tokens)
    res = parser.parse()
    if res.error:
        return None, res.error.as_string()
    try:
        value = interpreter.eval(res.node, interpreter.env)
    except RuntimeError as e:
        return None, f"RuntimeError: {e}"
    except ReturnSignal:
        return None, "RuntimeError: 'return' used outside of a function"
    return value, None

def run_program(fn: str, text: str):
    interpreter = Interpreter()
    # Auto-load stdlib prelude if present
    prelude_path = _find_stdlib_prelude_path()
    if prelude_path:
        try:
            with open(prelude_path, 'r', encoding='utf-8') as f:
                prelude_src = f.read()
        except Exception as e:
            return None, f"StdlibError: Failed to read prelude at {prelude_path}: {e}"
        _, std_err = _load_and_eval(interpreter, prelude_path, prelude_src)
        if std_err:
            return None, std_err

    # Load and run user program
    tokens, lex_err = lex_run(fn, text)
    if lex_err:
        return None, lex_err.as_string()
    parser = Parser(tokens)
    res = parser.parse()
    if res.error:
        return None, res.error.as_string()
    try:
        result = interpreter.eval(res.node, interpreter.env)
    except RuntimeError as e:
        return None, f"RuntimeError: {e}"
    except ReturnSignal as r:
        # return outside function
        return None, "RuntimeError: 'return' used outside of a function"
    return result, None 