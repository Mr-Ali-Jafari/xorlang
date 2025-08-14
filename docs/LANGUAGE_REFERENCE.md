# XorLang Language Reference | مرجع زبان XorLang

## English Reference

### Syntax Overview

XorLang uses C-style syntax with modern language features. All statements end with semicolons (`;`), though they are optional before closing braces or end of file.

### Keywords

```
var     func    return  if      else    while   for
true    false   null    import  class   new     this
```

### Operators

#### Arithmetic Operators
- `+` Addition
- `-` Subtraction  
- `*` Multiplication
- `/` Division
- `+` Unary plus
- `-` Unary minus

#### Comparison Operators
- `==` Equal to
- `!=` Not equal to
- `<` Less than
- `>` Greater than
- `<=` Less than or equal to
- `>=` Greater than or equal to

#### Assignment Operator
- `=` Assignment

### Data Types

#### Primitive Types
- **Number**: Integer or floating-point numbers
  - Examples: `42`, `3.14`, `-10`, `0.0`
- **String**: Text enclosed in single or double quotes
  - Examples: `"Hello"`, `'World'`, `"Line 1\nLine 2"`
  - Escape sequences: `\n` (newline), `\t` (tab), `\r` (carriage return), `\\` (backslash), `\"` (quote), `\'` (apostrophe)
- **Boolean**: `true` or `false`
- **Null**: `null` represents no value

#### Complex Types
- **Function**: First-class functions with closures
- **Class**: User-defined classes with methods
- **Instance**: Objects created from classes
- **Array**: Built-in array type (used internally by standard library)

### Variables

#### Declaration
```javascript
var x;                  // Declare without initialization (value is null)
var y = 42;            // Declare with initialization
var name = "XorLang";  // String variable
```

#### Assignment
```javascript
x = 100;               // Assign to existing variable
y = x + 50;           // Expression assignment
```

### Functions

#### Function Declaration
```javascript
func functionName(param1, param2) {
    // Function body
    return param1 + param2;
}
```

#### Function Call
```javascript
var result = functionName(10, 20);
```

#### Anonymous Functions (Not yet supported)
Currently, XorLang only supports named functions.

### Classes and Objects

#### Class Declaration
```javascript
class ClassName {
    func init(param1, param2) {
        this.property1 = param1;
        this.property2 = param2;
    }
    
    func method1() {
        return this.property1;
    }
    
    func method2(value) {
        this.property1 = value;
    }
}
```

#### Object Creation
```javascript
var obj = new ClassName("value1", "value2");
```

#### Property Access
```javascript
var value = obj.property1;
obj.property2 = "new value";
```

#### Method Call
```javascript
var result = obj.method1();
obj.method2("updated value");
```

### Control Flow

#### If Statement
```javascript
if (condition) {
    // Code block
} else {
    if (otherCondition) {
        // Nested if
    } else {
        // Final else
    }
}
```

#### While Loop
```javascript
while (condition) {
    // Loop body
}
```

#### For Loop
```javascript
for (initialization; condition; update) {
    // Loop body
}

// Example
for (var i = 0; i < 10; i = i + 1) {
    print(i);
}
```

### Comments

#### Single-line Comments
```javascript
// This is a single-line comment
var x = 42; // Comment at end of line
```

#### Multi-line Comments
```javascript
/*
This is a multi-line comment
that spans multiple lines
*/
```

### Import System

```javascript
import "path/to/file.xor"
```

The import statement includes the contents of another XorLang file at the current location.

---

## مرجع فارسی

### نمای کلی نحو

XorLang از نحو سبک C با ویژگی‌های زبان مدرن استفاده می‌کند. همه دستورات با نقطه‌ویرگول (`;`) پایان می‌یابند، هرچند قبل از بستن پرانتز یا انتهای فایل اختیاری است.

### کلمات کلیدی

```
var     func    return  if      else    while   for
true    false   null    import  class   new     this
```

### عملگرها

#### عملگرهای حسابی
- `+` جمع
- `-` تفریق
- `*` ضرب
- `/` تقسیم
- `+` مثبت یگانی
- `-` منفی یگانی

#### عملگرهای مقایسه
- `==` مساوی با
- `!=` نامساوی با
- `<` کمتر از
- `>` بیشتر از
- `<=` کمتر یا مساوی با
- `>=` بیشتر یا مساوی با

#### عملگر انتساب
- `=` انتساب

### انواع داده

#### انواع اولیه
- **عدد**: اعداد صحیح یا اعشاری
  - مثال‌ها: `42`, `3.14`, `-10`, `0.0`
- **رشته**: متن محصور در کوتیشن تک یا دوتایی
  - مثال‌ها: `"سلام"`, `'دنیا'`, `"خط 1\nخط 2"`
  - دنباله‌های فرار: `\n` (خط جدید), `\t` (تب), `\r` (بازگشت کرسر), `\\` (بک‌اسلش), `\"` (کوتیشن), `\'` (آپاستروف)
- **بولی**: `true` یا `false`
- **تهی**: `null` نشان‌دهنده عدم مقدار

#### انواع پیچیده
- **تابع**: توابع درجه اول با بسته‌ها
- **کلاس**: کلاس‌های تعریف شده توسط کاربر با متدها
- **نمونه**: اشیاء ایجاد شده از کلاس‌ها
- **آرایه**: نوع آرایه داخلی (داخلی توسط کتابخانه استاندارد استفاده می‌شود)

### متغیرها

#### اعلان
```javascript
var x;                  // اعلان بدون مقداردهی اولیه (مقدار null است)
var y = 42;            // اعلان با مقداردهی اولیه
var name = "XorLang";  // متغیر رشته‌ای
```

#### انتساب
```javascript
x = 100;               // انتساب به متغیر موجود
y = x + 50;           // انتساب عبارت
```

### توابع

#### اعلان تابع
```javascript
func functionName(param1, param2) {
    // بدنه تابع
    return param1 + param2;
}
```

#### فراخوانی تابع
```javascript
var result = functionName(10, 20);
```

#### توابع ناشناس (هنوز پشتیبانی نمی‌شود)
در حال حاضر، XorLang فقط از توابع نام‌دار پشتیبانی می‌کند.

### کلاس‌ها و اشیاء

#### اعلان کلاس
```javascript
class ClassName {
    func init(param1, param2) {
        this.property1 = param1;
        this.property2 = param2;
    }
    
    func method1() {
        return this.property1;
    }
    
    func method2(value) {
        this.property1 = value;
    }
}
```

#### ایجاد شی
```javascript
var obj = new ClassName("value1", "value2");
```

#### دسترسی به ویژگی
```javascript
var value = obj.property1;
obj.property2 = "new value";
```

#### فراخوانی متد
```javascript
var result = obj.method1();
obj.method2("updated value");
```

### کنترل جریان

#### دستور if
```javascript
if (condition) {
    // بلوک کد
} else {
    if (otherCondition) {
        // if تودرتو
    } else {
        // else نهایی
    }
}
```

#### حلقه while
```javascript
while (condition) {
    // بدنه حلقه
}
```

#### حلقه for
```javascript
for (initialization; condition; update) {
    // بدنه حلقه
}

// مثال
for (var i = 0; i < 10; i = i + 1) {
    print(i);
}
```

### نظرات

#### نظرات تک‌خطی
```javascript
// این یک نظر تک‌خطی است
var x = 42; // نظر در انتهای خط
```

#### نظرات چندخطی
```javascript
/*
این یک نظر چندخطی است
که چندین خط را در بر می‌گیرد
*/
```

### سیستم import

```javascript
import "path/to/file.xor"
```

دستور import محتویات فایل XorLang دیگری را در موقعیت فعلی شامل می‌کند.
