# XorLang Import System Guide

This guide explains how to use XorLang's import system to organize your code into modules and leverage the standard library.

## Basic Usage

The `import()` statement is used to load external modules. It takes a single string argument representing the path to the module file, relative to the standard library directory (`stdlib`).

```xorlang
// Import the 'lists.xor' module from the standard library
var Lists = import("lists.xor");

// You can now use the functions and classes defined in the Lists module
var myList = Lists.new();
myList.push(1);
```

## Module Resolution

When you use `import()`, the XorLang interpreter searches for the specified file within the `stdlib` directory. The path is resolved as follows:

1.  **Path Construction**: The interpreter joins the provided module path with the base path of the standard library.
2.  **File Extension**: The `.xor` extension is automatically appended to the module name if it's not present.
3.  **Security**: For security, module paths containing `..` or starting with `/` are considered invalid to prevent directory traversal attacks.

For example, `import("string")` and `import("stdlib/string.xor")` will both attempt to load the `stdlib/string.xor` file.

## Return Values

A XorLang module can return a value, which is typically a class or an object containing a set of functions. The last expression evaluated in a module file is its return value.

**Example: `stdlib/math.xor`**
```xorlang
// This class will be the return value of the module
class Math {
  func add(a, b) {
    return a + b;
  }
}
```

**Example: `main.xor`**
```xorlang
var Math = import("math.xor");
var result = Math.add(2, 3); // result is 5
```

## Standard Library

XorLang comes with a standard library that provides essential utilities. Some of the core modules include:

-   `prelude.xor`: A core module that is automatically loaded and provides fundamental classes like `Math`, `Time`, `Http`, and `File`.
-   `lists.xor`: Provides `List`, `Map`, and `Set` data structures.
-   `string.xor`: Contains utility functions for string manipulation.
-   `core.xor`: Includes foundational classes like `EventEmitter`.

By using the import system effectively, you can create more modular, reusable, and maintainable XorLang applications.
