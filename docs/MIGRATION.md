# Migration Guide: Old to New Architecture

## Overview

This document describes the migration from the old flat file structure to the new modular package architecture for XorLang.

## Architecture Changes

### Old Structure
```
Xorlang/
├── lexer.py                    # Lexical analysis
├── parser.py                   # Syntax analysis  
├── interpreter.py              # Runtime execution
├── main.py                     # CLI entry point
├── xorlang_ide.py             # Simple IDE
├── stdlib/prelude.xor         # Standard library
└── README.md                  # Documentation
```

### New Structure
```
Xorlang/
├── src/xorlang/               # Main package
│   ├── __init__.py            # Public API
│   ├── cli.py                 # Enhanced CLI
│   ├── ide.py                 # Enhanced IDE
│   ├── core/                  # Core components
│   │   ├── lexer.py           # Improved lexer
│   │   ├── parser.py          # Improved parser
│   │   ├── ast_nodes.py       # AST definitions
│   │   ├── interpreter.py     # Improved interpreter
│   │   ├── runner.py          # Execution coordinator
│   │   └── errors.py          # Error handling
│   └── stdlib/                # Standard library
│       ├── __init__.py        # Stdlib utilities
│       └── prelude.xor        # Built-in functions
├── examples/                  # Example programs
├── tests/                     # Test suite
├── docs/                      # Documentation
├── setup.py                   # Package setup
├── pyproject.toml            # Modern config
└── MANIFEST.in               # Package manifest
```

## Key Improvements

### 1. Modular Architecture
- **Separation of Concerns**: Each component has a clear responsibility
- **Better Organization**: Related functionality grouped together
- **Easier Maintenance**: Changes isolated to specific modules

### 2. Enhanced Error Handling
- **Centralized Errors**: All error types in `core/errors.py`
- **Better Messages**: Improved error formatting with position info
- **Consistent API**: Uniform error handling across components

### 3. Improved Public API
- **Clean Interface**: Simple functions for common operations
- **Type Hints**: Better IDE support and documentation
- **Backwards Compatibility**: Existing functionality preserved

### 4. Professional Packaging
- **Modern Setup**: `pyproject.toml` for Python packaging standards
- **Entry Points**: Command-line tools automatically installed
- **Dependencies**: Clear dependency management

### 5. Enhanced Tools
- **Better CLI**: More options and better error handling
- **Improved IDE**: Enhanced GUI with better features
- **Testing**: Comprehensive test suite

## Migration Steps

### For Users

#### Old Usage
```bash
python main.py program.xor
python xorlang_ide.py
```

#### New Usage
```bash
# Install the package
pip install -e .

# Use command-line tools
xorlang program.xor
xorlang-ide

# Or use Python API
python -c "import xorlang; print(xorlang.run_code('print(42);'))"
```

### For Developers

#### Old Import Pattern
```python
from lexer import run as lex_run
from parser import Parser
from interpreter import run_program
```

#### New Import Pattern
```python
import xorlang
# or
from xorlang.core import lexer, parser, interpreter
from xorlang import run_code, tokenize, parse
```

## API Changes

### Public API Functions

#### `xorlang.run_code(source_code, filename="<string>")`
Execute XorLang source code and return (result, error).

#### `xorlang.tokenize(source_code, filename="<string>")`
Tokenize XorLang source code and return (tokens, error).

#### `xorlang.parse(tokens)`
Parse tokens into AST and return ParseResult.

### Core Components

#### Lexer
- **Old**: `lexer.run(filename, text)`
- **New**: `xorlang.core.lexer.run(filename, text)`
- **Improvements**: Better error handling, type hints

#### Parser  
- **Old**: `Parser(tokens).parse()`
- **New**: `xorlang.core.parser.Parser(tokens).parse()`
- **Improvements**: Better error recovery, cleaner AST nodes

#### Interpreter
- **Old**: `run_program(filename, source)`
- **New**: `xorlang.core.runner.run_program(filename, source)`
- **Improvements**: Better environment handling, more built-ins

## Backwards Compatibility

The new architecture maintains backwards compatibility:

1. **Core Functionality**: All original features preserved
2. **Language Syntax**: No changes to XorLang syntax
3. **Standard Library**: All built-in functions available
4. **File Formats**: `.xor` files work unchanged

## Testing the Migration

### Run Basic Tests
```bash
# Test the package installation
pip install -e .

# Test CLI
xorlang examples/hello.xor

# Test API
python -c "import xorlang; result, error = xorlang.run_code('print(42);'); print('Result:', result, 'Error:', error)"

# Test IDE
xorlang-ide

# Run test suite
python -m pytest tests/
```

### Verify Examples
```bash
# Test example programs
xorlang examples/hello.xor

# Test interactive mode
xorlang -i
```

## Benefits of New Architecture

1. **Professional Structure**: Industry-standard Python package layout
2. **Better Tooling**: Enhanced CLI and IDE with more features
3. **Easier Distribution**: Proper packaging for PyPI distribution
4. **Improved Testing**: Comprehensive test suite with CI/CD ready
5. **Better Documentation**: Detailed docs and examples
6. **Extensibility**: Clear extension points for new features
7. **Maintainability**: Modular design easier to maintain and debug

## Next Steps

1. **Test Thoroughly**: Verify all functionality works as expected
2. **Update Documentation**: Ensure all docs reflect new structure
3. **CI/CD Setup**: Configure automated testing and deployment
4. **Distribution**: Prepare for PyPI publication if desired
5. **Community**: Share improved architecture with users

## Troubleshooting

### Common Issues

#### Import Errors
- **Problem**: `ModuleNotFoundError: No module named 'xorlang'`
- **Solution**: Run `pip install -e .` from project root

#### Path Issues
- **Problem**: Can't find standard library
- **Solution**: Ensure `src/xorlang/stdlib/prelude.xor` exists

#### CLI Not Found
- **Problem**: `xorlang: command not found`
- **Solution**: Reinstall package with `pip install -e .`

### Getting Help

- Check the documentation in `docs/`
- Run tests to verify installation: `python -m pytest tests/`
- Use the issue tracker for bugs and questions
