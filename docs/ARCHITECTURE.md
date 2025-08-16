# XorLang Architecture Documentation

## Overview

XorLang is a modern, interpreted programming language implemented in Python. This document describes the architecture and organization of the XorLang interpreter.

## Project Structure

```
Xorlang/
├── src/xorlang/                 # Main package source
│   ├── __init__.py             # Package initialization and public API
│   ├── cli.py                  # Command-line interface
│   ├── ide.py                  # Graphical IDE
│   ├── core/                   # Core interpreter components
│   │   ├── __init__.py         # Core module initialization
│   │   ├── lexer.py            # Lexical analysis (tokenization)
│   │   ├── parser.py           # Syntax analysis (AST generation)
│   │   ├── ast_nodes.py        # Abstract Syntax Tree node definitions
│   │   ├── interpreter.py      # Runtime execution engine
│   │   ├── runner.py           # Program execution coordinator
│   │   └── errors.py           # Error classes and handling
│   └── stdlib/                 # Standard library
│       ├── __init__.py         # Standard library utilities
│       └── prelude.xor         # Built-in XorLang functions
├── examples/                   # Example XorLang programs
├── tests/                      # Test suite
├── docs/                       # Documentation
├── setup.py                    # Package setup (legacy)
├── pyproject.toml             # Modern package configuration
├── MANIFEST.in                # Package manifest
├── requirements.txt           # Dependencies
└── README.md                  # Project overview
```

## Core Components

### 1. Lexer (`core/lexer.py`)

The lexer performs lexical analysis, converting source code into tokens.

**Key Classes:**
- `Lexer`: Main tokenizer class
- `Token`: Represents individual tokens
- `Position`: Tracks source code positions for error reporting

**Features:**
- Supports numbers (int/float), strings, identifiers, keywords
- Handles operators and delimiters
- Processes comments (single-line `//` and multi-line `/* */`)
- Import statement processing

### 2. Parser (`core/parser.py`)

The parser performs syntax analysis, converting tokens into an Abstract Syntax Tree (AST).

**Key Classes:**
- `Parser`: Recursive descent parser
- `ParseResult`: Represents parsing operation results

**Features:**
- Recursive descent parsing with operator precedence
- Error recovery and reporting
- Support for all XorLang language constructs

### 3. AST Nodes (`core/ast_nodes.py`)

Defines all Abstract Syntax Tree node types.

**Node Categories:**
- **Literals**: `NumberNode`, `StringNode`, `BoolNode`, `NullNode`
- **Variables**: `VarAccessNode`, `VarDeclNode`, `VarAssignNode`, `MemberAccessNode`
- **Expressions**: `BinOpNode`, `UnaryOpNode`, `CallNode`
- **Statements**: `BlockNode`, `IfNode`, `WhileNode`, `ForNode`, `FuncDefNode`, `ReturnNode`, `ClassDefNode`

### 4. Interpreter (`core/interpreter.py`)

The tree-walking interpreter that executes AST nodes.

**Key Classes:**
- `Interpreter`: Main execution engine
- `Environment`: Lexical scope management
- `FunctionValue`: Runtime function representation
- `ClassValue`: Runtime class representation

**Features:**
- Tree-walking evaluation
- Lexical scoping with environments
- Built-in function support
- Error handling with stack traces

### 5. Runner (`core/runner.py`)

Coordinates the execution pipeline from source code to results.

**Functions:**
- `run_program()`: Execute XorLang source code
- `run_file()`: Execute XorLang files
- `run_interactive()`: Interactive REPL mode

### 6. Error Handling (`core/errors.py`)

Centralized error management with position tracking.

**Error Types:**
- `LexError`: Tokenization errors
- `ParseError`: Syntax errors
- `RuntimeError`: Execution errors
- `ImportError`: Module import errors

## Language Features

### Data Types
- **Numbers**: Integers and floating-point
- **Strings**: UTF-8 text with escape sequences
- **Booleans**: `true` and `false`
- **Null**: `null` value

### Variables
```xor
var x = 42;
var name = "XorLang";
```

### Functions
```xor
func add(a, b) {
    return a + b;
}
```

### Classes
```xor
class Calculator {
    func multiply(a, b) {
        return a * b;
    }
}
```

### Control Flow
```xor
if (condition) {
    // code
} else {
    // code
}

while (condition) {
    // code
}

for (var i = 0; i < 10; i = i + 1) {
    // code
}
```

## Standard Library

The standard library (`stdlib/prelude.xor`) provides:

- **IO Functions**: `print()`, `println()`
- **Time Module**: `Time.now()`, `Time.wait()`
- **HTTP Module**: `Http.get()`, `Http.status()`
- **Math Module**: Basic arithmetic functions
- **Assertions**: `assert()`, `assertEqual()`

## Entry Points

### Command Line Interface (`cli.py`)
```bash
xorlang file.xor          # Execute file
xorlang -i                # Interactive mode
xorlang -c "print(42);"   # Execute code
```

### Graphical IDE (`ide.py`)
```bash
xorlang-ide               # Start GUI IDE
```

## Installation and Packaging

The project supports modern Python packaging:

- **pyproject.toml**: Modern package configuration
- **setup.py**: Legacy setup script
- **MANIFEST.in**: Package manifest for additional files

### Installation
```bash
pip install -e .          # Development install
pip install xorlang       # Production install
```

## Testing

The test suite (`tests/`) provides:
- Unit tests for core components
- Integration tests for language features
- Error handling verification

```bash
python -m pytest tests/   # Run tests
```

## Development Workflow

1. **Code Organization**: Follow the modular architecture
2. **Error Handling**: Use the centralized error system
3. **Testing**: Add tests for new features
4. **Documentation**: Update docs for changes

## Extension Points

The architecture supports extensions:

- **Built-in Functions**: Add to `Interpreter._install_builtins()`
- **Language Features**: Extend lexer, parser, and interpreter
- **Standard Library**: Add XorLang modules to `stdlib/`
- **Tools**: Create new entry points in the package

## Performance Considerations

- **Tree-walking**: Direct AST interpretation (simple but not fastest)
- **Memory**: Environments create scope chains
- **Optimization**: Future bytecode compilation possible

## Future Enhancements

Potential improvements:
- Bytecode compilation for performance
- Advanced error recovery in parser
- Debugging support with breakpoints
- Package/module system
- Type system (optional typing)
- JIT compilation
