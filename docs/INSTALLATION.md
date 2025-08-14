# XorLang Installation Guide | راهنمای نصب XorLang

## English Installation Guide

### Prerequisites

- **Python 3.8 or higher** - XorLang is implemented in Python
- **Git** (optional) - For cloning the repository

### Installation Methods

#### Method 1: Clone from Repository (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd Xorlang

# Verify installation by running an example
python3 -m src.xorlang.cli examples/gui_http_example.xor
```

#### Method 2: Download ZIP

1. Download the project as a ZIP file
2. Extract to your desired location
3. Navigate to the extracted folder
4. Run: `python3 -m src.xorlang.cli examples/gui_http_example.xor`

### Running XorLang Programs

#### Command Line Interface

```bash
# Basic usage
python3 -m src.xorlang.cli your_program.xor

# Alternative method
python3 src/xorlang/cli.py your_program.xor
```

#### IDE Integration

You can run XorLang programs from any text editor or IDE:

1. **VS Code**: Install Python extension, open terminal, run commands above
2. **PyCharm**: Configure as external tool or run in terminal
3. **Sublime Text**: Build system can be configured
4. **Vim/Emacs**: Run from command line or configure build commands

### Project Structure

After installation, your directory structure should look like:

```
Xorlang/
├── src/xorlang/           # Core interpreter
│   ├── core/              # Lexer, parser, interpreter
│   ├── stdlib/            # Standard library (.xor files)
│   └── cli.py            # Command-line interface
├── examples/              # Example programs
├── docs/                 # Documentation
└── README.md             # Main documentation
```

### Verification

Test your installation with these commands:

```bash
# Test basic functionality
python3 -m src.xorlang.cli -c "print('Hello, XorLang!');"

# Test GUI functionality (opens a window)
python3 -m src.xorlang.cli examples/gui_http_example.xor

# Test HTTP functionality
python3 -m src.xorlang.cli examples/http_test.xor
```

### Troubleshooting

#### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'src'`
**Solution**: Make sure you're running from the project root directory

**Issue**: `Permission denied` on Linux/macOS
**Solution**: Use `python3` instead of `python`, or check file permissions

**Issue**: GUI windows don't appear
**Solution**: Ensure you have tkinter installed (`sudo apt-get install python3-tk` on Ubuntu)

**Issue**: HTTP requests fail
**Solution**: Check internet connection and firewall settings

#### Getting Help

1. Check the documentation in the `docs/` folder
2. Review example programs in `examples/`
3. Ensure Python 3.8+ is installed: `python3 --version`

### Development Setup

If you want to contribute or modify XorLang:

```bash
# Clone the repository
git clone <repository-url>
cd Xorlang

# Create a virtual environment (optional but recommended)
python3 -m venv xorlang-env
source xorlang-env/bin/activate  # On Windows: xorlang-env\Scripts\activate

# Install development dependencies (if any)
# pip install -r requirements-dev.txt

# Run tests
python3 -m pytest tests/  # If test suite exists

# Make your changes and test
python3 -m src.xorlang.cli your_test_program.xor
```

---

## راهنمای نصب فارسی

### پیش‌نیازها

- **Python 3.8 یا بالاتر** - XorLang با پایتون پیاده‌سازی شده است
- **Git** (اختیاری) - برای کلون کردن مخزن

### روش‌های نصب

#### روش 1: کلون از مخزن (توصیه شده)

```bash
# کلون کردن مخزن
git clone <repository-url>
cd Xorlang

# تأیید نصب با اجرای یک مثال
python3 -m src.xorlang.cli examples/gui_http_example.xor
```

#### روش 2: دانلود ZIP

1. پروژه را به صورت فایل ZIP دانلود کنید
2. در مکان دلخواه استخراج کنید
3. به پوشه استخراج شده بروید
4. اجرا کنید: `python3 -m src.xorlang.cli examples/gui_http_example.xor`

### اجرای برنامه‌های XorLang

#### رابط خط فرمان

```bash
# استفاده پایه
python3 -m src.xorlang.cli your_program.xor

# روش جایگزین
python3 src/xorlang/cli.py your_program.xor
```

#### یکپارچگی IDE

می‌توانید برنامه‌های XorLang را از هر ویرایشگر متن یا IDE اجرا کنید:

1. **VS Code**: افزونه Python نصب کنید، ترمینال باز کنید، دستورات بالا را اجرا کنید
2. **PyCharm**: به عنوان ابزار خارجی پیکربندی کنید یا در ترمینال اجرا کنید
3. **Sublime Text**: سیستم build قابل پیکربندی است
4. **Vim/Emacs**: از خط فرمان اجرا کنید یا دستورات build پیکربندی کنید

### ساختار پروژه

پس از نصب، ساختار دایرکتوری شما باید به این شکل باشد:

```
Xorlang/
├── src/xorlang/           # مفسر اصلی
│   ├── core/              # لکسر، پارسر، مفسر
│   ├── stdlib/            # کتابخانه استاندارد (فایل‌های .xor)
│   └── cli.py            # رابط خط فرمان
├── examples/              # برنامه‌های نمونه
├── docs/                 # مستندات
└── README.md             # مستندات اصلی
```

### تأیید

نصب خود را با این دستورات تست کنید:

```bash
# تست عملکرد پایه
python3 -m src.xorlang.cli -c "print('سلام، XorLang!');"

# تست عملکرد GUI (پنجره باز می‌کند)
python3 -m src.xorlang.cli examples/gui_http_example.xor

# تست عملکرد HTTP
python3 -m src.xorlang.cli examples/http_test.xor
```

### عیب‌یابی

#### مشکلات رایج

**مشکل**: `ModuleNotFoundError: No module named 'src'`
**راه‌حل**: مطمئن شوید از دایرکتوری ریشه پروژه اجرا می‌کنید

**مشکل**: `Permission denied` در Linux/macOS
**راه‌حل**: از `python3` به جای `python` استفاده کنید، یا مجوزهای فایل را بررسی کنید

**مشکل**: پنجره‌های GUI ظاهر نمی‌شوند
**راه‌حل**: مطمئن شوید tkinter نصب است (`sudo apt-get install python3-tk` در Ubuntu)

**مشکل**: درخواست‌های HTTP ناموفق
**راه‌حل**: اتصال اینترنت و تنظیمات فایروال را بررسی کنید

#### دریافت کمک

1. مستندات موجود در پوشه `docs/` را بررسی کنید
2. برنامه‌های نمونه در `examples/` را مرور کنید
3. مطمئن شوید Python 3.8+ نصب است: `python3 --version`

### تنظیم توسعه

اگر می‌خواهید در XorLang مشارکت کنید یا آن را تغییر دهید:

```bash
# کلون کردن مخزن
git clone <repository-url>
cd Xorlang

# ایجاد محیط مجازی (اختیاری اما توصیه شده)
python3 -m venv xorlang-env
source xorlang-env/bin/activate  # در ویندوز: xorlang-env\Scripts\activate

# نصب وابستگی‌های توسعه (در صورت وجود)
# pip install -r requirements-dev.txt

# اجرای تست‌ها
python3 -m pytest tests/  # در صورت وجود مجموعه تست

# تغییرات خود را انجام دهید و تست کنید
python3 -m src.xorlang.cli your_test_program.xor
```

---

## Platform-Specific Notes | نکات مخصوص پلتفرم

### Windows

```cmd
# Use py launcher if available
py -3 -m src.xorlang.cli your_program.xor

# Or use python directly
python -m src.xorlang.cli your_program.xor
```

### macOS

```bash
# Ensure Python 3 is used
python3 -m src.xorlang.cli your_program.xor

# If you have Homebrew Python
/usr/local/bin/python3 -m src.xorlang.cli your_program.xor
```

### Linux

```bash
# Standard installation
python3 -m src.xorlang.cli your_program.xor

# If tkinter is missing (for GUI features)
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo yum install tkinter         # CentOS/RHEL
sudo pacman -S tk                # Arch Linux
```
