# XorLang Programming Language | زبان برنامه‌نویسی XorLang

<div align="center">

![XorLang Logo](https://img.shields.io/badge/XorLang-v1.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

*A modern, object-oriented programming language with zero-dependency GUI and HTTP libraries*

*زبان برنامه‌نویسی مدرن و شی‌گرا با کتابخانه‌های GUI و HTTP بدون وابستگی*

</div>

---

## English Documentation

### 🚀 Quick Start

XorLang is a modern programming language implemented in Python, featuring a complete lexer, parser, and interpreter with built-in GUI and HTTP capabilities.

#### Installation & Usage

```bash
# Clone the repository
git clone <repository-url>
cd Xorlang

# Run a XorLang program
python3 -m src.xorlang.cli examples/gui_http_example.xor

# Or use the CLI directly
python3 src/xorlang/cli.py examples/hello.xor
```

#### File Extension
- Official extension: `.xor`
- Example: `myprogram.xor`

### 💻 IDE & Editor Support

For the best development experience, we recommend using the XorLang VS Code extension, which provides syntax highlighting.

**Installation:**
1. Clone this repository.
2. Open Visual Studio Code.
3. Go to the Extensions view (`Ctrl+Shift+X` or `Cmd+Shift+X`).
4. Click the `...` menu in the top-right corner and select `Install from VSIX...`.
5. Navigate to the `vscode-extension` directory in this project and select the `.vsix` package file (you will need to package it first, see instructions below).

**Packaging the Extension:**
First, you need to install `vsce`, the official tool for packaging VS Code extensions.

```bash
npm install -g vsce
```

Then, navigate to the extension's directory and run:

```bash
cd vscode-extension
vsce package
```

This will create a `xorlang-x.x.x.vsix` file, which you can then install in VS Code.

### 📝 Language Features

#### Data Types
- **Integers**: `42`, `0`, `-10`
- **Floats**: `3.14`, `-2.5`, `0.0`
- **Strings**: `"Hello"`, `'World'` (supports `\n`, `\t`, `\r`, `\\`)
- **Booleans**: `true`, `false`
- **Null**: `null`

#### Variables & Assignment
```javascript
var x;              // Declaration
var y = 42;         // Declaration with initialization
x = "Hello";        // Assignment
```

#### Functions
```javascript
func greet(name) {
    return "Hello, " + name + "!";
}

var message = greet("World");
print(message);
```

#### Classes & Objects
```javascript
class Calculator {
    func init() {
        this.version = "1.0";
    }
    
    func add(a, b) {
        return a + b;
    }
    
    func multiply(a, b) {
        return a * b;
    }
}

var calc = new Calculator();
var result = calc.add(5, 3);
print("Result: " + result);
```

#### Control Flow
```javascript
// If-else statements
if (x > 0) {
    print("Positive");
} else {
    if (x < 0) {
        print("Negative");
    } else {
        print("Zero");
    }
}

// While loops
var i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// For loops
for (var j = 0; j < 3; j = j + 1) {
    print("Iteration: " + j);
}
```

### 🖥️ GUI Programming

XorLang includes a zero-dependency GUI library built on Python's tkinter:

```javascript
// Create a window
var window = new Window("My App", 400, 300);

// Add widgets
window.addLabel("Welcome to XorLang!", 10, 10);
window.addButton("Click Me", 10, 50, myClickHandler);

// Show the window
window.show();

func myClickHandler() {
    print("Button clicked!");
}
```

### 🌐 HTTP Programming

Built-in HTTP capabilities for web requests:

```javascript
// Make HTTP GET request
var response = http_get("https://api.example.com/data");
if (response) {
    print("Response: " + response);
} else {
    print("Request failed");
}

// Check HTTP status
var status = http_get_status("https://api.example.com/health");
print("Status: " + status);
```

### 📚 Standard Library

#### Built-in Functions
- `print(...)` - Output to console
- `len(str)` - String length
- `ord(char)` - Character to ASCII
- `chr(code)` - ASCII to character
- `__str_get__(str, index)` - Get character at index
- `time_now()` - Current timestamp
- `time_ms()` - Current time in milliseconds
- `sleep(seconds)` - Pause execution

#### Standard Libraries
- **prelude.xor** - Core utilities and functions
- **string.xor** - String manipulation utilities
- **object.xor** - Object-oriented programming helpers
- **collections.xor** - Data structure utilities
- **gui.xor** - GUI programming framework
- **http.xor** - HTTP client functionality

### 🏗️ Project Structure

```
Xorlang/
├── src/xorlang/
│   ├── core/
│   │   ├── lexer.py          # Tokenization
│   │   ├── parser.py         # Syntax analysis
│   │   ├── interpreter.py    # Code execution
│   │   ├── ast_nodes.py      # Abstract syntax tree
│   │   └── errors.py         # Error handling
│   ├── stdlib/               # Standard library
│   │   ├── prelude.xor
│   │   ├── string.xor
│   │   ├── object.xor
│   │   ├── collections.xor
│   │   ├── gui.xor
│   │   └── http.xor
│   ├── cli.py               # Command-line interface
│   └── __init__.py
├── examples/                # Example programs
├── docs/                   # Documentation
└── README.md
```

---

## مستندات فارسی

### 🚀 شروع سریع

XorLang یک زبان برنامه‌نویسی مدرن است که با پایتون پیاده‌سازی شده و دارای لکسر، پارسر و مفسر کامل با قابلیت‌های GUI و HTTP داخلی است.

#### نصب و استفاده

```bash
# کلون کردن مخزن
git clone <repository-url>
cd Xorlang

# اجرای برنامه XorLang
python3 -m src.xorlang.cli examples/gui_http_example.xor

# یا استفاده مستقیم از CLI
python3 src/xorlang/cli.py examples/hello.xor
```

#### پسوند فایل
- پسوند رسمی: `.xor`
- مثال: `myprogram.xor`

### 💻 پشتیبانی از IDE و ویرایشگر

برای بهترین تجربه توسعه، توصیه می‌کنیم از افزونه XorLang برای VS Code استفاده کنید که قابلیت برجسته‌سازی نحو (syntax highlighting) را فراهم می‌کند.

**نصب:**
۱. این مخزن را کلون کنید.
۲. Visual Studio Code را باز کنید.
۳. به بخش افزونه‌ها بروید (`Ctrl+Shift+X` یا `Cmd+Shift+X`).
۴. روی منوی `...` در گوشه بالا سمت راست کلیک کرده و `Install from VSIX...` را انتخاب کنید.
۵. به پوشه `vscode-extension` در این پروژه بروید و فایل پکیج `.vsix` را انتخاب کنید (ابتدا باید آن را پکیج کنید، به دستورالعمل زیر مراجعه کنید).

**پکیج کردن افزونه:**
ابتدا باید `vsce`، ابزار رسمی برای پکیج کردن افزونه‌های VS Code، را نصب کنید.

```bash
npm install -g vsce
```

سپس، به پوشه افزونه بروید و اجرا کنید:

```bash
cd vscode-extension
vsce package
```

این دستور یک فایل `xorlang-x.x.x.vsix` ایجاد می‌کند که می‌توانید آن را در VS Code نصب کنید.

### 📝 ویژگی‌های زبان

#### انواع داده
- **اعداد صحیح**: `42`, `0`, `-10`
- **اعداد اعشاری**: `3.14`, `-2.5`, `0.0`
- **رشته‌ها**: `"سلام"`, `'دنیا'` (پشتیبانی از `\n`, `\t`, `\r`, `\\`)
- **بولی**: `true`, `false`
- **تهی**: `null`

#### متغیرها و انتساب
```javascript
var x;              // اعلان
var y = 42;         // اعلان با مقداردهی اولیه
x = "سلام";         // انتساب
```

#### توابع
```javascript
func greet(name) {
    return "سلام، " + name + "!";
}

var message = greet("دنیا");
print(message);
```

#### کلاس‌ها و اشیاء
```javascript
class Calculator {
    func init() {
        this.version = "1.0";
    }
    
    func add(a, b) {
        return a + b;
    }
    
    func multiply(a, b) {
        return a * b;
    }
}

var calc = new Calculator();
var result = calc.add(5, 3);
print("نتیجه: " + result);
```

#### کنترل جریان
```javascript
// دستورات شرطی
if (x > 0) {
    print("مثبت");
} else {
    if (x < 0) {
        print("منفی");
    } else {
        print("صفر");
    }
}

// حلقه while
var i = 0;
while (i < 5) {
    print(i);
    i = i + 1;
}

// حلقه for
for (var j = 0; j < 3; j = j + 1) {
    print("تکرار: " + j);
}
```

### 🖥️ برنامه‌نویسی GUI

XorLang شامل کتابخانه GUI بدون وابستگی بر اساس tkinter پایتون است:

```javascript
// ایجاد پنجره
var window = new Window("برنامه من", 400, 300);

// اضافه کردن ویجت‌ها
window.addLabel("به XorLang خوش آمدید!", 10, 10);
window.addButton("کلیک کنید", 10, 50, myClickHandler);

// نمایش پنجره
window.show();

func myClickHandler() {
    print("دکمه کلیک شد!");
}
```

### 🌐 برنامه‌نویسی HTTP

قابلیت‌های HTTP داخلی برای درخواست‌های وب:

```javascript
// درخواست HTTP GET
var response = http_get("https://api.example.com/data");
if (response) {
    print("پاسخ: " + response);
} else {
    print("درخواست ناموفق");
}

// بررسی وضعیت HTTP
var status = http_get_status("https://api.example.com/health");
print("وضعیت: " + status);
```

### 📚 کتابخانه استاندارد

#### توابع داخلی
- `print(...)` - خروجی به کنسول
- `len(str)` - طول رشته
- `ord(char)` - کاراکتر به ASCII
- `chr(code)` - ASCII به کاراکتر
- `__str_get__(str, index)` - دریافت کاراکتر در ایندکس
- `time_now()` - زمان فعلی
- `time_ms()` - زمان فعلی به میلی‌ثانیه
- `sleep(seconds)` - توقف اجرا

#### کتابخانه‌های استاندارد
- **prelude.xor** - ابزارها و توابع اصلی
- **string.xor** - ابزارهای دستکاری رشته
- **object.xor** - کمک‌کننده‌های برنامه‌نویسی شی‌گرا
- **collections.xor** - ابزارهای ساختار داده
- **gui.xor** - چارچوب برنامه‌نویسی GUI
- **http.xor** - عملکرد کلاینت HTTP

### 🏗️ ساختار پروژه

```
Xorlang/
├── src/xorlang/
│   ├── core/
│   │   ├── lexer.py          # توکن‌سازی
│   │   ├── parser.py         # تحلیل نحوی
│   │   ├── interpreter.py    # اجرای کد
│   │   ├── ast_nodes.py      # درخت نحو انتزاعی
│   │   └── errors.py         # مدیریت خطا
│   ├── stdlib/               # کتابخانه استاندارد
│   │   ├── prelude.xor
│   │   ├── string.xor
│   │   ├── object.xor
│   │   ├── collections.xor
│   │   ├── gui.xor
│   │   └── http.xor
│   ├── cli.py               # رابط خط فرمان
│   └── __init__.py
├── examples/                # برنامه‌های نمونه
├── docs/                   # مستندات
└── README.md
```

---

## 🤝 Contributing | مشارکت

We welcome contributions! Please see our contributing guidelines for more information.

از مشارکت شما استقبال می‌کنیم! لطفاً راهنمای مشارکت ما را برای اطلاعات بیشتر ببینید.

## 📄 License | مجوز

This project is licensed under the MIT License.

این پروژه تحت مجوز MIT منتشر شده است.

---

<div align="center">

**Made with ❤️ for the programming community**

**با ❤️ برای جامعه برنامه‌نویسی ساخته شده**

</div> 