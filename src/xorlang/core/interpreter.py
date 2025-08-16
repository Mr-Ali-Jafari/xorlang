from __future__ import annotations

# XorLang Optimized Interpreter v2.0.0
# Performance-optimized tree-walking interpreter for executing XorLang AST nodes

from dataclasses import dataclass, field
from typing import Any, Dict, List, Callable, Optional, Union
import os
import time
import http.client
import urllib.request
import urllib.error
import tkinter as tk
from functools import partial
from urllib import request as _py_request

from .ast_nodes import *
from .errors import RuntimeError, ReturnSignal, BreakSignal, ContinueSignal


@dataclass
class FunctionValue:
    """Represents a function value in the interpreter."""
    name: Optional[str]
    params: List[str]
    body: BlockNode
    closure: 'Environment'


@dataclass
class ClassValue:
    """Represents a class value in the interpreter."""
    name: str
    members: Dict[str, Any]  # functions or constants

    def __call__(self, interpreter, args):
        instance = InstanceValue(self)
        initializer = self.members.get("init")
        if isinstance(initializer, FunctionValue):
            # Bind 'this' to the instance
            bound_initializer = FunctionValue(
                name=initializer.name,
                params=initializer.params,
                body=initializer.body,
                closure=Environment(initializer.closure)
            )
            bound_initializer.closure.define("this", instance)
            interpreter._eval_function_call(bound_initializer, args)
        elif isinstance(initializer, tuple) and initializer[0] == 'builtin':
            # Handle built-in initializer
            _, name, func, *meta = initializer
            if meta and meta[0].get('pass_this'):
                func(instance, *args)
        return instance


@dataclass
class ArrayValue:
    """Represents a native array, wrapping a Python list."""
    items: List[Any] = field(default_factory=list)
    
    def get(self, index):
        """Get item at index."""
        try:
            idx = int(index)
            if 0 <= idx < len(self.items):
                return self.items[idx]
            return None
        except (ValueError, TypeError):
            raise RuntimeError(f"Array index must be an integer, got {index}")
    
    def set(self, index, value):
        """Set item at index."""
        try:
            idx = int(index)
            if 0 <= idx < len(self.items):
                self.items[idx] = value
        except (ValueError, TypeError):
            raise RuntimeError(f"Array index must be an integer, got {index}")
    
    def push(self, item):
        """Add item to end of array."""
        self.items.append(item)
    
    def pop(self):
        """Remove and return last item."""
        if not self.items:
            return None
        return self.items.pop()
    
    def length(self):
        """Get length of array."""
        return len(self.items)
    
    def removeAt(self, index):
        """Remove item at index."""
        try:
            idx = int(index)
            if 0 <= idx < len(self.items):
                return self.items.pop(idx)
            return None
        except (ValueError, TypeError):
            raise RuntimeError(f"Array index must be an integer, got {index}")
    
    def clear(self):
        """Clear all items."""
        self.items.clear()
    
    def indexOf(self, item):
        """Find index of item."""
        for i, val in enumerate(self.items):
            if val == item:
                return i
        return -1


@dataclass
class InstanceValue:
    """Represents an instance of a class."""
    cls: ClassValue
    fields: Dict[str, Any] = field(default_factory=dict)

    def get(self, name: str):
        if name in self.fields:
            return self.fields[name]

        method = self.cls.members.get(name)
        if method:
            # If the method is a built-in that expects 'this', pass the instance
            if isinstance(method, tuple) and len(method) > 3 and method[3].get('pass_this'):
                # Curry the function with the instance
                from functools import partial
                return ('builtin', method[1], partial(method[2], self), method[3])
            return method

        raise RuntimeError(f"Undefined property '{name}'.")

    def set(self, name: str, value: Any):
        self.fields[name] = value


class Environment:
    """Optimized lexical environment for variable bindings."""
    
    def __init__(self, parent: Optional['Environment'] = None):
        self.parent = parent
        self.values: Dict[str, Any] = {}
        # Performance optimization: Cache resolved variables
        self._cache: Dict[str, Tuple[Any, int]] = {}
        self._cache_version = 0

    def define(self, name: str, value: Any) -> None:
        """Define a new variable in this environment."""
        self.values[name] = value
        # Invalidate cache when new variables are defined
        self._cache_version += 1

    def set(self, name: str, value: Any) -> None:
        """Set a variable value, searching up the scope chain."""
        env = self.resolve(name)
        if env is None:
            # Allow implicit definition on assignment
            self.values[name] = value
            self._cache_version += 1
        else:
            env.values[name] = value
            env._cache_version += 1

    def get(self, name: str) -> Any:
        """Get a variable value, searching up the scope chain."""
        # Performance optimization: Check cache first
        cache_key = f"{id(self)}:{name}"
        if cache_key in self._cache:
            cached_value, version = self._cache[cache_key]
            if version == self._cache_version:
                return cached_value
        
        env = self.resolve(name)
        if env is None:
            raise RuntimeError(f"Undefined variable '{name}'")
        
        value = env.values[name]
        # Cache the result
        self._cache[cache_key] = (value, self._cache_version)
        return value

    def resolve(self, name: str) -> Optional['Environment']:
        """Find the environment that defines the given variable."""
        if name in self.values:
            return self
        if self.parent:
            return self.parent.resolve(name)
        return None


class Interpreter:
    """Performance-optimized tree-walking interpreter for XorLang."""

    def __init__(self, stdlib_path: Optional[str] = None, error_handler=None):
        self.globals = Environment()
        self.env = self.globals
        
        # Performance optimization: Cache for frequently accessed values
        self._eval_cache = {}
        self._method_cache = {}
        
        # Set up standard library path
        if stdlib_path is None:
            # Default to looking in the source package directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            self.stdlib_path = os.path.join(script_dir, '..', 'stdlib')
        else:
            self.stdlib_path = stdlib_path
            
        # Verify the path exists
        if not os.path.isdir(self.stdlib_path):
            # Try looking in the project root
            project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))
            self.stdlib_path = os.path.join(project_root, 'src', 'xorlang', 'stdlib')
            
        self.error_handler = error_handler or self.report_error

        # GUI state
        self.gui_windows = {}
        self.gui_next_id = 0

        # Performance optimization: Pre-load stdlib to avoid repeated file I/O
        self._stdlib_cache = {}
        
        self._install_builtins()
        self._load_all_stdlib()

    def _install_builtins(self) -> None:
        """Install built-in functions and constants."""
        
        # Import math functions
        import math
        import random
        
        def builtin_print(*args):
            """Built-in print function."""
            print(*args)
            
        def builtin_input(prompt=None):
            """Built-in input function."""
            try:
                if prompt is not None:
                    return input(str(prompt))
                return input()
            except EOFError:
                return None
        
        self.globals.define('print', ('builtin', 'print', builtin_print))
        self.globals.define('input', ('builtin', 'input', builtin_input))

        # Time built-ins
        def builtin_time_now():
            """Get current time as seconds since epoch."""
            return time.time()
        
        def builtin_time_ms():
            """Get current time as milliseconds since epoch."""
            return int(time.time() * 1000)
        
        def builtin_sleep(seconds):
            """Sleep for the specified number of seconds."""
            try:
                time.sleep(float(seconds))
            except Exception as e:
                raise RuntimeError(f"sleep error: {e}")
        
        self.globals.define('time_now', ('builtin', 'time_now', builtin_time_now))
        self.globals.define('time_ms', ('builtin', 'time_ms', builtin_time_ms))
        self.globals.define('sleep', ('builtin', 'sleep', builtin_sleep))

        # String built-ins
        def builtin_len(s):
            if not isinstance(s, str):
                raise RuntimeError(f"len() expected a string, but got {type(s).__name__}")
            return len(s)

        def builtin_ord(c):
            if not isinstance(c, str) or len(c) != 1:
                raise RuntimeError(f"ord() expected a single character string, but got '{c}'")
            return ord(c)

        def builtin_chr(code):
            try:
                return chr(int(code))
            except (ValueError, TypeError):
                raise RuntimeError(f"chr() expected an integer code, but got '{code}'")

        def builtin_str_get(s, index):
            if not isinstance(s, str):
                raise RuntimeError(f"__str_get__() expected a string, but got {type(s).__name__}")
            try:
                idx = int(index)
                if 0 <= idx < len(s):
                    return s[idx]
                return None # Return null for out-of-bounds access
            except (ValueError, TypeError):
                raise RuntimeError(f"__str_get__() expected an integer index, but got '{index}'")

        self.globals.define('len', ('builtin', 'len', builtin_len))
        self.globals.define('ord', ('builtin', 'ord', builtin_ord))
        self.globals.define('chr', ('builtin', 'chr', builtin_chr))
        self.globals.define('__str_get__', ('builtin', '__str_get__', builtin_str_get))

        # HTTP functions
        def builtin_http_get(url):
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    return response.read().decode('utf-8', 'ignore')
            except Exception:
                return None # Return null on error

        def builtin_http_get_status(url):
            try:
                with urllib.request.urlopen(url, timeout=10) as response:
                    return response.getcode()
            except Exception:
                return -1 # Return -1 on error

        self.globals.define('http_get', ('builtin', 'http_get', builtin_http_get))
        self.globals.define('http_get_status', ('builtin', 'http_get_status', builtin_http_get_status))

        # GUI functions
        def builtin_gui_create_window(title, width, height):
            window_id = self.gui_next_id
            self.gui_next_id += 1

            root = tk.Tk()
            root.title(title)
            root.geometry(f"{int(width)}x{int(height)}")
            
            self.gui_windows[window_id] = {"root": root, "widgets": {}}
            return window_id

        def builtin_gui_add_label(window_id, text, x, y):
            if window_id not in self.gui_windows:
                raise RuntimeError(f"GUI window with id {window_id} not found.")
            root = self.gui_windows[window_id]["root"]
            label = tk.Label(root, text=str(text))
            label.place(x=int(x), y=int(y))

        def builtin_gui_add_button(window_id, text, x, y, callback):
            if window_id not in self.gui_windows:
                raise RuntimeError(f"GUI window with id {window_id} not found.")
            if not isinstance(callback, FunctionValue):
                raise RuntimeError("Button callback must be a function.")

            root = self.gui_windows[window_id]["root"]
            # Use a partial to pass the callback to the handler
            handler = partial(self._eval_function_call, callback, [])
            button = tk.Button(root, text=str(text), command=handler)
            button.place(x=int(x), y=int(y))

        def builtin_gui_show_window(window_id):
            if window_id not in self.gui_windows:
                raise RuntimeError(f"GUI window with id {window_id} not found.")
            root = self.gui_windows[window_id]["root"]
            try:
                root.mainloop()
            except (tk.TclError, KeyboardInterrupt):
                # Handle window being closed or interrupt
                pass

        self.globals.define('gui_create_window', ('builtin', 'gui_create_window', builtin_gui_create_window))
        self.globals.define('gui_add_label', ('builtin', 'gui_add_label', builtin_gui_add_label))
        self.globals.define('gui_add_button', ('builtin', 'gui_add_button', builtin_gui_add_button))
        self.globals.define('gui_show_window', ('builtin', 'gui_show_window', builtin_gui_show_window))
        
        # Math built-ins
        def builtin_math_sin(x): return math.sin(x)
        def builtin_math_cos(x): return math.cos(x)
        def builtin_math_tan(x): return math.tan(x)
        def builtin_math_asin(x): return math.asin(x)
        def builtin_math_acos(x): return math.acos(x)
        def builtin_math_atan(x): return math.atan(x)
        def builtin_math_atan2(y, x): return math.atan2(y, x)
        def builtin_math_sqrt(x): return math.sqrt(x)
        def builtin_math_pow(x, y): return math.pow(x, y)
        def builtin_math_floor(x): return math.floor(x)
        def builtin_math_ceil(x): return math.ceil(x)
        def builtin_math_round(x): return round(x)
        def builtin_math_random(): return random.random()
        def builtin_math_log(x): return math.log(x)
        def builtin_math_exp(x): return math.exp(x)
        
        # Register math built-ins
        math_builtins = {
            '__math_sin': builtin_math_sin,
            '__math_cos': builtin_math_cos,
            '__math_tan': builtin_math_tan,
            '__math_asin': builtin_math_asin,
            '__math_acos': builtin_math_acos,
            '__math_atan': builtin_math_atan,
            '__math_atan2': builtin_math_atan2,
            '__math_sqrt': builtin_math_sqrt,
            '__math_pow': builtin_math_pow,
            '__math_floor': builtin_math_floor,
            '__math_ceil': builtin_math_ceil,
            '__math_round': builtin_math_round,
            '__math_random': builtin_math_random,
            '__math_log': builtin_math_log,
            '__math_exp': builtin_math_exp
        }
        
        for name, func in math_builtins.items():
            self.globals.define(name, ('builtin', name, func))

        # File system built-ins
        def builtin_file_exists(path):
            try:
                return os.path.exists(str(path))
            except Exception:
                return False

        def builtin_file_read(path):
            try:
                with open(str(path), 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                return None

        def builtin_file_write(path, content):
            try:
                with open(str(path), 'w', encoding='utf-8') as f:
                    f.write(str(content))
                return True
            except Exception:
                return False

        # OS built-ins
        def builtin_os_getenv(name):
            try:
                return os.environ.get(str(name))
            except Exception:
                return None

        def builtin_os_listdir(path):
            try:
                files = os.listdir(str(path))
                # Convert Python list to ArrayValue
                array_value = ArrayValue()
                array_value.items = files
                return array_value
            except Exception:
                return None

        # Register file system and OS built-ins
        self.globals.define('__file_exists', ('builtin', '__file_exists', builtin_file_exists))
        self.globals.define('__file_read', ('builtin', '__file_read', builtin_file_read))
        self.globals.define('__file_write', ('builtin', '__file_write', builtin_file_write))
        self.globals.define('__os_getenv', ('builtin', '__os_getenv', builtin_os_getenv))
        self.globals.define('__os_listdir', ('builtin', '__os_listdir', builtin_os_listdir))

        # Array class - Create it here to avoid conflicts
        self._create_builtin_array_class()

        # Note: Standard libraries are loaded in the constructor, not here

    def _create_builtin_array_class(self):
        """Creates and installs the built-in Array class."""
        members = {}

        # Helper to get native list from instance
        def get_native_list(instance):
            if not isinstance(instance, InstanceValue) or 'items' not in instance.fields or not isinstance(instance.fields['items'], ArrayValue):
                raise RuntimeError("Array method called on incompatible type.")
            return instance.fields['items'].items

        def array_init(this):
            """Initialize a new array."""
            this.fields['items'] = ArrayValue()
            return None

        def array_push(this, item):
            """Push an item onto the array."""
            items = get_native_list(this)
            items.append(item)
            return None

        def array_pop(this):
            """Pop an item from the array."""
            items = get_native_list(this)
            if not items:
                return None
            return items.pop()

        def array_get(this, index):
            """Get an item at index."""
            items = get_native_list(this)
            try:
                idx = int(index)
                if 0 <= idx < len(items):
                    return items[idx]
                return None
            except (ValueError, TypeError):
                raise RuntimeError(f"Array index must be an integer, got {index}")

        def array_set(this, index, value):
            """Set an item at index."""
            items = get_native_list(this)
            try:
                idx = int(index)
                if 0 <= idx < len(items):
                    items[idx] = value
                    return None
                raise RuntimeError(f"Array index {idx} out of bounds (0 to {len(items)-1})")
            except (ValueError, TypeError):
                raise RuntimeError(f"Array index must be an integer, got {index}")

        def array_length(this):
            """Get array length."""
            return len(get_native_list(this))

        def array_remove_at(this, index):
            """Remove item at index."""
            items = get_native_list(this)
            try:
                idx = int(index)
                if 0 <= idx < len(items):
                    item = items.pop(idx)
                    return item
                raise RuntimeError(f"Array index {idx} out of bounds (0 to {len(items)-1})")
            except (ValueError, TypeError):
                raise RuntimeError(f"Array index must be an integer, got {index}")

        def array_clear(this):
            """Clear all items."""
            get_native_list(this).clear()
            return None

        def array_contains(this, item):
            """Check if array contains item."""
            try:
                return item in get_native_list(this)
            except Exception:
                return False

        def array_index_of(this, item):
            """Find index of item."""
            items = get_native_list(this)
            try:
                for i, val in enumerate(items):
                    if val == item:
                        return i
                return -1
            except Exception:
                return -1

        def array_for_each(this, callback):
            items = list(get_native_list(this)) # Create a copy for safe iteration
            if not isinstance(callback, FunctionValue):
                raise RuntimeError("forEach expects a function.")
            for i, item in enumerate(items):
                self._eval_function_call(callback, [item, i])

        def array_join(this, separator=""):
            items = get_native_list(this)
            return str(separator).join(map(str, items))

        # Define methods as built-ins that expect 'this'
        methods = {
            "init": array_init,
            "push": array_push,
            "pop": array_pop,
            "get": array_get,
            "set": array_set,
            "length": array_length,
            "removeAt": array_remove_at,
            "clear": array_clear,
            "contains": array_contains,
            "indexOf": array_index_of,
            "forEach": array_for_each,
            "join": array_join,
        }

        for name, func in methods.items():
            # Mark built-in as needing 'this' passed
            members[name] = ('builtin', name, func, {'pass_this': True})

        # Create the Array class and define it globally
        array_class = ClassValue("Array", members)
        self.globals.define("Array", array_class)

    def _load_all_stdlib(self):
        """Load all standard library files in the correct order."""
        if not self.stdlib_path or not os.path.isdir(self.stdlib_path):
            return
            
        # Define the load order - prelude.xor must be first
        stdlib_files = [
            'prelude.xor',
            'core.xor',
            'string.xor',
            'lists.xor',
            'gui.xor'
        ]
        
        for filename in stdlib_files:
            self._load_stdlib_file(filename)

    def _load_stdlib_file(self, filename):
        """Finds, parses, and evaluates a standard library file with caching."""
        # Performance optimization: Check cache first
        if filename in self._stdlib_cache:
            return self._stdlib_cache[filename]
            
        lib_path = self._find_stdlib_file(filename)
        if lib_path and os.path.exists(lib_path):
            try:
                with open(lib_path, 'r', encoding='utf-8') as f:
                    code = f.read()
                
                from .lexer import Lexer
                from .parser import Parser

                lexer = Lexer(lib_path, code)
                tokens, error = lexer.make_tokens()
                if error:
                    return

                parser = Parser(tokens)
                ast = parser.parse()
                if ast.error:
                    return

                if ast.node:
                    # Save current environment and switch to globals
                    old_env = self.env
                    self.env = self.globals
                    try:
                        self.eval(ast.node)
                        # Cache the AST for future use
                        self._stdlib_cache[filename] = ast.node
                    except Exception:
                        import traceback
                        traceback.print_exc()
                        raise
                    finally:
                        # Restore original environment
                        self.env = old_env

            except Exception:
                import traceback
                traceback.print_exc()

    def _find_stdlib_file(self, filename):
        """Finds the path to a standard library file."""
        # Check relative to the interpreter file's location
        script_dir = os.path.dirname(__file__)
        stdlib_path = os.path.join(script_dir, '..', 'stdlib', filename)
        if os.path.exists(stdlib_path):
            return os.path.abspath(stdlib_path)
        return None

    def report_error(self, message, line, column):
        """Default error handler."""
        print(f"[Runtime Error] line {line}:{column}: {message}")

    # Performance optimization: Use method dispatch table
    _eval_methods = {}

    def eval(self, node: ASTNode, env: Optional[Environment] = None) -> Any:
        """Evaluate an AST node in the given environment with caching."""
        env = env or self.env
        node_type = type(node)
        
        # Performance optimization: Use method dispatch table
        if node_type not in self._eval_methods:
            method_name = f'_eval_{node_type.__name__}'
            method = getattr(self, method_name, self._generic_eval)
            self._eval_methods[node_type] = method
        
        return self._eval_methods[node_type](node, env)

    def _generic_eval(self, node: ASTNode, env: Environment) -> Any:
        """Generic evaluation for unknown node types."""
        raise RuntimeError(f"No evaluation method for {type(node).__name__}")

    def _eval_BlockNode(self, node, env):
        """Evaluate a block of statements."""
        result = None
        for stmt in node.statements:
            result = self.eval(stmt, env)
        return result

    def _eval_ExpressionStatementNode(self, node, env):
        """Evaluate an expression statement."""
        return self.eval(node.expr, env)

    def _eval_NumberNode(self, node: NumberNode, env: Environment) -> Any:
        """Evaluate a number literal."""
        return node.tok.value

    def _eval_StringNode(self, node: StringNode, env: Environment) -> Any:
        """Evaluate a string literal."""
        return node.tok.value

    def _eval_BoolNode(self, node: BoolNode, env: Environment) -> Any:
        """Evaluate a boolean literal."""
        return node.tok.value == 'true'

    def _eval_NullNode(self, node: NullNode, env: Environment) -> Any:
        """Evaluate a null literal."""
        return None

    def _eval_VarAccessNode(self, node: VarAccessNode, env: Environment) -> Any:
        """Evaluate variable access."""
        return env.get(node.name_tok.value)

    def _eval_MemberAccessNode(self, node: MemberAccessNode, env: Environment) -> Any:
        """Evaluate member access (object.member) with caching."""
        obj = self.eval(node.obj_node, env)
        member_name = node.member_tok.value

        # Performance optimization: Cache method lookups
        cache_key = (id(obj), member_name)
        if cache_key in self._method_cache:
            return self._method_cache[cache_key]

        if isinstance(obj, InstanceValue):
            # First, check instance fields
            if member_name in obj.fields:
                result = obj.fields[member_name]
                self._method_cache[cache_key] = result
                return result

            # If not in fields, check class methods
            method = obj.cls.members.get(member_name)
            if method:
                if isinstance(method, FunctionValue):
                    # Bind 'this' to the instance for user-defined methods
                    bound_method = FunctionValue(
                        name=method.name,
                        params=method.params,
                        body=method.body,
                        closure=Environment(method.closure)
                    )
                    bound_method.closure.define("this", obj)
                    result = bound_method
                    self._method_cache[cache_key] = result
                    return result
                elif isinstance(method, tuple) and method[0] == 'builtin':
                    # Handle built-in methods
                    if len(method) > 3 and method[3].get('pass_this'):
                        # Curry the function with the instance ('this')
                        from functools import partial
                        result = ('builtin', method[1], partial(method[2], obj), method[3])
                        self._method_cache[cache_key] = result
                        return result
                    self._method_cache[cache_key] = method
                    return method

            raise RuntimeError(f"Undefined property '{member_name}'.")
        elif isinstance(obj, ClassValue):
            # Accessing static members of a class
            if member_name in obj.members:
                result = obj.members[member_name]
                self._method_cache[cache_key] = result
                return result
            else:
                raise RuntimeError(f"'{obj.name}' has no static member '{member_name}'")
        elif isinstance(obj, ArrayValue):
            # Accessing methods of ArrayValue objects
            if hasattr(obj, member_name):
                method = getattr(obj, member_name)
                if callable(method):
                    result = ('builtin', member_name, method)
                    self._method_cache[cache_key] = result
                    return result
                else:
                    self._method_cache[cache_key] = method
                    return method
            else:
                raise RuntimeError(f"ArrayValue has no member '{member_name}'")
        else:
            raise RuntimeError(f"Cannot access member of non-class value")

    def _eval_VarDeclNode(self, node: VarDeclNode, env: Environment) -> Any:
        """Evaluate variable declaration."""
        # First, evaluate the expression on the right-hand side.
        value_to_assign = self.eval(node.value_node, env) if node.value_node else None
        
        # Then, define the variable in the environment with the computed value.
        env.define(node.name_tok.value, value_to_assign)
        
        # The result of a declaration statement is the value assigned.
        return value_to_assign

    def _eval_AssignNode(self, node: AssignNode, env: Environment) -> Any:
        """Evaluate assignment."""
        if isinstance(node.target_node, MemberAccessNode):
            # Handle obj.member = value
            obj = self.eval(node.target_node.obj_node, env)
            if isinstance(obj, InstanceValue):
                val = self.eval(node.expr_node, env)
                member_name = node.target_node.member_tok.value
                obj.set(member_name, val)
                return val
            else:
                raise RuntimeError("Cannot assign to member of non-instance")
        elif isinstance(node.target_node, VarAccessNode):
            # Handle var = value
            name = node.target_node.name_tok.value
            val = self.eval(node.expr_node, env)
            env.set(name, val)
            return val
        else:
            raise RuntimeError("Invalid assignment target")

    def _eval_ImportNode(self, node: ImportNode, env: Environment) -> Any:
        """Evaluate import statements."""
        module_name = node.module_name.value
        # Basic security: prevent directory traversal
        if '..' in module_name or module_name.startswith('/'):
            raise RuntimeError(f"Import error: Invalid module path '{module_name}'")

        # Construct the full path to the module file
        if not self.stdlib_path or not os.path.isdir(self.stdlib_path):
            raise RuntimeError("Standard library path is not configured.")

        # Handle different import path formats
        if module_name.startswith('stdlib/'):
            # Remove 'stdlib/' prefix and construct path
            relative_path = module_name[7:]  # Remove 'stdlib/'
            # Check if the path already has .xor extension
            if relative_path.endswith('.xor'):
                module_path = os.path.join(self.stdlib_path, relative_path)
            else:
                module_path = os.path.join(self.stdlib_path, f"{relative_path}.xor")
        else:
            # Direct module name
            # Check if the path already has .xor extension
            if module_name.endswith('.xor'):
                module_path = os.path.join(self.stdlib_path, module_name)
            else:
                module_path = os.path.join(self.stdlib_path, f"{module_name}.xor")

        if not os.path.isfile(module_path):
            raise RuntimeError(f"Import error: File '{module_name}' not found at '{module_path}'")

        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
            return self._eval_module(module_path, source_code)
        except FileNotFoundError:
            # This should be caught by the isfile check, but as a fallback
            raise RuntimeError(f"Import error: File '{module_name}' not found at '{module_path}'")

    def _eval_module(self, module_path: str, source_code: str) -> Any:
        """Evaluate a module and return its exports."""
        # Create a new environment for the module
        module_env = Environment()
        
        # Parse the module source code
        from .lexer import Lexer
        from .parser import Parser

        lexer = Lexer(module_path, source_code)
        tokens, error = lexer.make_tokens()
        if error:
            raise RuntimeError(f"Lexer error in module {module_path}: {error.format_error()}")

        parser = Parser(tokens)
        ast = parser.parse()
        if ast.error:
            raise RuntimeError(f"Parser error in module {module_path}: {ast.error.format_error()}")

        # Evaluate the module in its own environment
        old_env = self.env
        self.env = module_env
        try:
            if ast.node:
                self.eval(ast.node)
        finally:
            # Restore original environment
            self.env = old_env

        # Return the module environment as the module object
        return module_env

    def _eval_ThisNode(self, node: ThisNode, env: Environment) -> Any:
        """Evaluate 'this' keyword."""
        try:
            return env.get("this")
        except RuntimeError:
            raise RuntimeError("'this' is not defined in this context")

    def _eval_UnaryOpNode(self, node: UnaryOpNode, env: Environment) -> Any:
        """Evaluate unary operations."""
        operand = self.eval(node.node, env)
        
        if node.op_tok.type == 'PLUS':
            return +operand
        elif node.op_tok.type == 'MINUS':
            return -operand
        else:
            raise RuntimeError(f"Unknown unary operator: {node.op_tok.type}")

    def _eval_BinOpNode(self, node: BinOpNode, env: Environment) -> Any:
        """Evaluate binary operations."""
        left = self.eval(node.left, env)
        right = self.eval(node.right, env)
        
        if node.op_tok.type == 'PLUS':
            return left + right
        elif node.op_tok.type == 'MINUS':
            return left - right
        elif node.op_tok.type == 'MUL':
            return left * right
        elif node.op_tok.type == 'DIV':
            if right == 0:
                raise RuntimeError("Division by zero")
            return left / right
        elif node.op_tok.type == 'MOD':
            if right == 0:
                raise RuntimeError("Modulo by zero")
            return left % right
        elif node.op_tok.type == 'EE':
            return left == right
        elif node.op_tok.type == 'NE':
            return left != right
        elif node.op_tok.type == 'LT':
            return left < right
        elif node.op_tok.type == 'GT':
            return left > right
        elif node.op_tok.type == 'LTE':
            return left <= right
        elif node.op_tok.type == 'GTE':
            return left >= right
        else:
            raise RuntimeError(f"Unknown binary operator: {node.op_tok.type}")

    def _eval_CallNode(self, node: CallNode, env: Environment) -> Any:
        """Evaluate function calls and class instantiations."""
        callee = self.eval(node.callee_node, env)
        args = [self.eval(arg, env) for arg in node.arg_nodes]

        if isinstance(callee, tuple) and callee[0] == 'builtin':
            # Built-in function
            _, name, func, *meta = callee
            # If it's a partially applied method from get(), the instance is already bound
            return func(*args)
        elif isinstance(callee, FunctionValue):
            # User-defined function
            return self._eval_function_call(callee, args)
        elif isinstance(callee, ClassValue):
            # Class instantiation
            return callee(self, args)
        else:
            raise RuntimeError(f"'{callee}' is not callable")

    def _eval_function_call(self, callee: FunctionValue, args: List[Any]) -> Any:
        """Helper to evaluate a function call."""
        if len(args) != len(callee.params):
            raise RuntimeError(f"Function '{callee.name}' expects {len(callee.params)} arguments, got {len(args)}")
        
        # Create new environment for function execution
        func_env = Environment(callee.closure)
        for param, arg in zip(callee.params, args):
            func_env.define(param, arg)
        
        try:
            # If 'this' is defined, it's a method call
            if func_env.resolve("this"):
                pass # 'this' is already in the closure for bound methods
            return self.eval(callee.body, func_env)
        except ReturnSignal as ret:
            return ret.value

    def _eval_IfNode(self, node: IfNode, env: Environment) -> Any:
        """Evaluate if statements."""
        for condition, body in node.cases:
            if self.eval(condition, env):
                return self.eval(body, env)
        
        if node.else_case:
            return self.eval(node.else_case, env)
        
        return None

    def _eval_WhileNode(self, node: WhileNode, env: Environment) -> Any:
        """Evaluate while loops."""
        while self.eval(node.cond_node, env):
            self.eval(node.body_block, env)
        return None

    def _eval_ForNode(self, node: ForNode, env: Environment) -> Any:
        """Evaluate for loops."""
        # Create new environment for loop scope
        loop_env = Environment(env)
        
        # Initialize
        if node.init_node is not None:
            self.eval(node.init_node, loop_env)
        
        # Loop
        while True:
            if node.cond_node is not None and not self.eval(node.cond_node, loop_env):
                break
            
            self.eval(node.body_block, loop_env)
            
            if node.update_node is not None:
                self.eval(node.update_node, loop_env)
            
            # Prevent infinite loop if no condition
            if node.cond_node is None:
                break
        
        return None

    def _eval_FuncDefNode(self, node: FuncDefNode, env: Environment) -> Any:
        """Evaluate function definitions."""
        name = node.name_tok.value if node.name_tok else None
        params = [t.value for t in node.arg_name_toks]
        fn = FunctionValue(name, params, node.body_block, env)
        
        if name:
            env.define(name, fn)
        
        return fn

    def _eval_ReturnNode(self, node: ReturnNode, env: Environment) -> Any:
        """Evaluate return statements."""
        val = self.eval(node.expr_node, env) if node.expr_node else None
        raise ReturnSignal(val)

    def _eval_ClassDefNode(self, node: ClassDefNode, env: Environment) -> Any:
        """Evaluate class definitions."""
        # Class environment inherits from current env so methods can see globals/builtins
        class_env = Environment(env)
        
        for member in node.members:
            fv = self._eval_FuncDefNode(member, class_env)
            if fv.name:
                class_env.define(fv.name, fv)
        
        cls = ClassValue(node.name_tok.value, class_env.values)
        env.define(node.name_tok.value, cls)
        return cls

    def _eval_NewNode(self, node: NewNode, env: Environment) -> Any:
        """Evaluate 'new' expressions for object instantiation."""
        class_name = node.class_name_tok.value
        cls = env.get(class_name)

        if not isinstance(cls, ClassValue):
            raise RuntimeError(f"'{class_name}' is not a class.")

        args = [self.eval(arg, env) for arg in node.arg_nodes]
        return cls(self, args)