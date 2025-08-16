# XorLang Programming Language v2.0.0

A modern, interpreted programming language designed for simplicity and expressiveness. XorLang features a clean syntax, comprehensive standard library, and built-in support for various programming paradigms.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Language Syntax](#language-syntax)
- [Standard Library](#standard-library)
- [Examples](#examples)
- [Command Line Interface](#command-line-interface)
- [Development](#development)

## Features

- **Clean Syntax**: Simple and readable syntax inspired by modern programming languages
- **Dynamic Typing**: Automatic type inference and dynamic type checking
- **Object-Oriented**: Full support for classes, methods, and inheritance
- **Functional Programming**: Support for higher-order functions and functional patterns
- **Standard Library**: Comprehensive built-in libraries for common tasks
- **Cross-Platform**: Runs on Windows, macOS, and Linux
- **Interactive Shell**: Built-in REPL for interactive development
- **Error Handling**: Clear error messages with line numbers and context

## Installation

XorLang provides multiple installation methods for Linux systems with comprehensive tooling and desktop integration.

### Prerequisites

- **Linux OS**: Ubuntu 18.04+, Debian 9+, CentOS 7+, or equivalent
- **Architecture**: x86_64 (64-bit)
- **Python**: 3.8+ (for building from source)
- **Privileges**: sudo access for system-wide installation
- **Disk Space**: ~100MB for installation

### Quick Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/Mr-Ali-Jafari/Xorlang.git
cd Xorlang

# Build executables (if needed)
python build.py

# Run the enhanced installer
sudo ./install_to_opt.sh
```

### Installation Methods

1. **🚀 Enhanced Installer** (Recommended)
   - Automated installation with desktop integration
   - Icon support and file associations
   - Comprehensive logging and backup
   - Command: `sudo ./install_to_opt.sh`

2. **📦 Release Packages**
   - Pre-built installer packages
   - Download from GitHub Releases
   - Extract and run installer

3. **🔧 Manual Installation**
   - Custom setup and configuration
   - Full control over installation process
   - Suitable for advanced users

📖 **[Complete Installation Guide](INSTALLATION.md)** - Comprehensive installation documentation with troubleshooting

### Quick Verification

```bash
# Test CLI installation
xorlang --version
xorlang --help

# Test IDE installation
xorlang-ide

# Test file association (if desktop integration enabled)
# Create test file and double-click to open in IDE
echo 'print("Hello, XorLang!");' > test.xor
```

### Uninstallation

```bash
# Using the dedicated uninstaller (recommended)
sudo ./uninstall_xorlang.sh

# Preview what will be removed
sudo ./uninstall_xorlang.sh --dry-run

# Force removal without prompts
sudo ./uninstall_xorlang.sh --force
```

## Quick Start

### Hello World

Create a file named `hello.xor`:

```xor
print("Hello, World!");
```

Run it:

```bash
python3 src/xorlang/cli.py hello.xor
```

### Interactive Mode

Start the interactive shell:

```bash
python3 src/xorlang/cli.py -i
```

## Language Syntax

### Variables and Data Types

```xor
// Variable declaration
var name = "XorLang";
var version = 2.0;
var isAwesome = true;
var items = new Array();

// Dynamic typing
var dynamic = "string";
dynamic = 42;  // Now it's a number
dynamic = true;  // Now it's a boolean
```

### Control Flow

#### If Statements

```xor
if (condition) {
    // code here
} else if (another_condition) {
    // code here
} else {
    // code here
}
```

#### Loops

```xor
// While loop
var i = 0;
while (i < 10) {
    print(i);
    i = i + 1;
}

// For loop
for (var j = 0; j < 5; j = j + 1) {
    print("Iteration " + j);
}
```

### Functions

```xor
// Function definition
func greet(name) {
    return "Hello, " + name + "!";
}

// Function call
var message = greet("World");
print(message);

// Function with multiple parameters
func add(a, b) {
    return a + b;
}

// Function with default parameters (using null checks)
func greetWithTitle(name, title) {
    if (title == null) {
        title = "Mr.";
    }
    return "Hello, " + title + " " + name + "!";
}
```

### Classes and Objects

```xor
// Class definition
class Person {
    func init(name, age) {
        this.name = name;
        this.age = age;
    }
    
    func greet() {
        return "Hello, I'm " + this.name + " and I'm " + this.age + " years old.";
    }
    
    func haveBirthday() {
        this.age = this.age + 1;
        return "Happy birthday! I'm now " + this.age + " years old.";
    }
}

// Creating objects
var person = new Person("Alice", 25);
print(person.greet());
print(person.haveBirthday());
```

### Arrays

```xor
// Creating arrays
var numbers = new Array();
numbers.push(1);
numbers.push(2);
numbers.push(3);

// Accessing elements
print(numbers.get(0));  // 1
print(numbers.length());  // 3

// Setting elements
numbers.set(1, 42);
print(numbers.get(1));  // 42

// Removing elements
numbers.removeAt(0);
print(numbers.length());  // 2
```

## Standard Library

XorLang comes with a comprehensive standard library organized into modules:

### Core Module (`core.xor`)

**EventEmitter**: Event-driven programming support

```xor
var EventEmitter = import("stdlib/core.xor");
var emitter = new EventEmitter();

emitter.on("message", func(data) {
    print("Received: " + data);
});

emitter.emit("message", "Hello from event!");
```

### Lists Module (`lists.xor`)

**List**: Dynamic array implementation

```xor
var List = import("stdlib/lists.xor");
var list = new List();
list.push("item1");
list.push("item2");
print(list.size());  // 2
```

**Stack**: Last-In-First-Out data structure

```xor
var Stack = import("stdlib/lists.xor");
var stack = new Stack();
stack.push(1);
stack.push(2);
print(stack.pop());  // 2
print(stack.peek());  // 1
```

**Queue**: First-In-First-Out data structure

```xor
var Queue = import("stdlib/lists.xor");
var queue = new Queue();
queue.enqueue("first");
queue.enqueue("second");
print(queue.dequeue());  // "first"
```

**Map**: Key-value storage

```xor
var Map = import("stdlib/lists.xor");
var map = new Map();
map.set("name", "XorLang");
map.set("version", 2.0);
print(map.get("name"));  // "XorLang"
print(map.has("version"));  // true
```

**Set**: Unique value collection

```xor
var Set = import("stdlib/lists.xor");
var set = new Set();
set.add("apple");
set.add("banana");
set.add("apple");  // Duplicate, won't be added
print(set.size());  // 2
```

### String Module (`string.xor`)

```xor
var String = import("stdlib/string.xor");

// String manipulation
var text = "  Hello, World!  ";
print(String.trim(text));  // "Hello, World!"
print(String.toUpperCase(text));  // "  HELLO, WORLD!  "
print(String.toLowerCase(text));  // "  hello, world!  "

// String searching
print(String.indexOf("Hello World", "World"));  // 6
print(String.contains("Hello World", "World"));  // true
print(String.startsWith("Hello World", "Hello"));  // true
print(String.endsWith("Hello World", "World"));  // true

// String transformation
print(String.replace("Hello World", "World", "XorLang"));  // "Hello XorLang"
print(String.reverse("Hello"));  // "olleH"
print(String.repeat("Ha", 3));  // "HaHaHa"

// String splitting and joining
var parts = String.split("apple,banana,orange", ",");
print(parts.get(0));  // "apple"
```

### Math Module (`prelude.xor`)

```xor
var Math = import("stdlib/prelude.xor");

// Constants
print(Math.PI());  // 3.141592653589793
print(Math.E());   // 2.718281828459045

// Basic arithmetic
print(Math.add(5, 3));  // 8
print(Math.sub(10, 4));  // 6
print(Math.mul(6, 7));   // 42
print(Math.div(20, 5));  // 4.0

// Mathematical functions
print(Math.abs(-42));    // 42
print(Math.sqrt(16));    // 4.0
print(Math.pow(2, 8));   // 256.0
print(Math.floor(3.7));  // 3.0
print(Math.ceil(3.2));   // 4.0
print(Math.round(3.5));  // 4.0
print(Math.random());    // Random number between 0 and 1

// Trigonometric functions
print(Math.sin(0));      // 0.0
print(Math.cos(0));      // 1.0
print(Math.tan(0));      // 0.0
```

### Time Module (`prelude.xor`)

```xor
var Time = import("stdlib/prelude.xor");

// Current time
print(Time.now());   // Current timestamp
print(Time.nowMs()); // Current timestamp in milliseconds

// Delays
Time.wait(1);  // Wait for 1 second
```

### HTTP Module (`prelude.xor`)

```xor
var Http = import("stdlib/prelude.xor");

// HTTP requests
var response = Http.get("https://api.example.com/data");
print(response);

var status = Http.status("https://api.example.com/data");
print(status);
```

### File Module (`prelude.xor`)

```xor
var File = import("stdlib/prelude.xor");

// File operations
if (File.exists("data.txt")) {
    var content = File.read("data.txt");
    print(content);
}

File.write("output.txt", "Hello, XorLang!");
```

### OS Module (`prelude.xor`)

```xor
var Os = import("stdlib/prelude.xor");

// Environment variables
var home = Os.getenv("HOME");
print(home);

// Directory listing
var files = Os.listdir(".");
var i = 0;
while (i < files.length()) {
    print(files.get(i));
    i = i + 1;
}
```

### IO Module (`io.xor`)

```xor
var IO = import("stdlib/io.xor");

// Input/Output
var name = IO.input("Enter your name: ");
IO.println("Hello, " + name + "!");

IO.print("This is on the same line");
IO.println("This is on a new line");
```

### GUI Module (`gui.xor`)

```xor
var GUI = import("stdlib/gui.xor");

// Create a simple GUI window
var window = new GUI.Window("My App", 400, 300);
window.addLabel("Hello, XorLang!", 50, 50);
window.addButton("Click Me!", 50, 100, func() {
    print("Button clicked!");
});
window.show();
```

## Examples

### Calculator

```xor
func calculate(operation, a, b) {
    if (operation == "add") {
        return a + b;
    } else if (operation == "subtract") {
        return a - b;
    } else if (operation == "multiply") {
        return a * b;
    } else if (operation == "divide") {
        if (b == 0) {
            print("Error: Division by zero");
            return null;
        }
        return a / b;
    } else {
        print("Unknown operation: " + operation);
        return null;
    }
}

print(calculate("add", 10, 5));      // 15
print(calculate("multiply", 4, 7));  // 28
```

### Simple Web Scraper

```xor
var Http = import("stdlib/prelude.xor");
var String = import("stdlib/string.xor");

func scrapeTitle(url) {
    var content = Http.get(url);
    if (content != null) {
        var titleStart = String.indexOf(content, "<title>");
        var titleEnd = String.indexOf(content, "</title>");
        if (titleStart != -1 && titleEnd != -1) {
            return String.substring(content, titleStart + 7, titleEnd);
        }
    }
    return null;
}

var title = scrapeTitle("https://example.com");
print("Page title: " + title);
```

### File Processor

```xor
var File = import("stdlib/prelude.xor");
var String = import("stdlib/string.xor");

func processFile(filename) {
    if (File.exists(filename) == false) {
        print("File not found: " + filename);
        return;
    }
    
    var content = File.read(filename);
    var lines = String.split(content, "\n");
    var wordCount = 0;
    
    var i = 0;
    while (i < lines.length()) {
        var line = lines.get(i);
        var words = String.split(line, " ");
        wordCount = wordCount + words.length();
        i = i + 1;
    }
    
    print("Total words: " + wordCount);
}

processFile("input.txt");
```

## Command Line Interface

### Basic Usage

```bash
# Execute a file
python3 src/xorlang/cli.py script.xor

# Interactive mode
python3 src/xorlang/cli.py -i

# Execute code from command line
python3 src/xorlang/cli.py -c "print('Hello, World!')"

# Show version
python3 src/xorlang/cli.py --version
```

### Command Line Options

- `file`: XorLang source file to execute
- `-i, --interactive`: Start interactive shell (REPL)
- `-c, --command`: Execute XorLang code from command line
- `-v, --version`: Show version information

## Development

### Project Structure

```
xorlang/
├── src/xorlang/
│   ├── core/           # Core interpreter components
│   │   ├── lexer.py    # Tokenizer
│   │   ├── parser.py   # AST parser
│   │   ├── interpreter.py # Tree-walking interpreter
│   │   ├── errors.py   # Error handling
│   │   └── runner.py   # Program execution
│   ├── stdlib/         # Standard library modules
│   │   ├── prelude.xor # Core utilities
│   │   ├── string.xor  # String manipulation
│   │   ├── lists.xor   # Data structures
│   │   ├── core.xor    # Core functionality
│   │   ├── io.xor      # Input/Output
│   │   └── gui.xor     # GUI components
│   ├── cli.py          # Command line interface
│   ├── ide.py          # Integrated development environment
│   └── __init__.py     # Package initialization
├── tests/              # Test files
├── examples/           # Example programs
└── README.md           # This file
```

### Running Tests

```bash
# Run all tests
python3 src/xorlang/cli.py test_file.xor

# Run specific test
python3 src/xorlang/cli.py tests/test_math.xor
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

### Language Limitations

- No support for `static` class members (use methods instead)
- No array literals `[]` (use `new Array()` and `push()`)
- No `break` statements (use conditional loop termination)
- No logical operators `&&` and `||` (use nested `if` statements)
- No anonymous functions (use named functions)
- Limited type coercion in string concatenation

### Future Features

- Static class members
- Array literals
- Break and continue statements
- Logical operators
- Anonymous functions
- Enhanced type system
- Module system improvements
- Performance optimizations

## Documentation & Resources

### 📚 Complete Documentation
- **[Installation Guide](INSTALLATION.md)** - Comprehensive installation instructions with troubleshooting
- **[Linux Installation Guide](INSTALL_LINUX.md)** - Detailed Linux-specific installation steps
- **[Performance Optimizations](PERFORMANCE_OPTIMIZATIONS.md)** - Performance tuning and optimization guide
- **[Import System Guide](IMPORT_SYSTEM_GUIDE.md)** - Module and import system documentation
- **[Installer Guide](INSTALLER_GUIDE.md)** - Building and packaging instructions
- **[Changelog](CHANGELOG.md)** - Version history and release notes

### 🛠️ Installation & Management
- **Build from Source**: `python build.py` - Creates PyInstaller executables in `dist/`
- **Enhanced Installer**: `sudo ./install_to_opt.sh` - Automated installation with desktop integration
  - Installs to `/opt/xorlang/` with symlinks in `/usr/local/bin/`
  - Creates desktop entries, MIME types, and icon support
  - Options: `--force`, `--verbose`, `--skip-backup`, `--help`
- **Complete Uninstaller**: `sudo ./uninstall_xorlang.sh` - Safe removal with backup options
  - Removes all files, desktop entries, and system integration
  - Options: `--dry-run`, `--force`, `--no-backup`, `--verbose`, `--help`
  - Creates backup before removal for safety

### 🔗 External Links
- **[GitHub Repository](https://github.com/Mr-Ali-Jafari/Xorlang)** - Source code and development
- **[Issues](https://github.com/Mr-Ali-Jafari/Xorlang/issues)** - Bug reports and feature requests
- **[Discussions](https://github.com/Mr-Ali-Jafari/Xorlang/discussions)** - Community discussions and support
- **[Releases](https://github.com/Mr-Ali-Jafari/Xorlang/releases)** - Download pre-built packages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Ali Jafari** - [GitHub](https://github.com/Mr-Ali-Jafari)

## Acknowledgments

- Inspired by modern programming languages
- Built with Python for cross-platform compatibility
- Community contributions and feedback
- Enhanced tooling with comprehensive installer/uninstaller system

---

**XorLang v2.1.0** - A modern programming language with comprehensive tooling.
