# XorLang API Reference | مرجع API زبان XorLang

## English API Reference

### Built-in Functions

#### Core Functions

##### `print(...args)`
Outputs values to the console.
- **Parameters**: Any number of values
- **Returns**: `null`
- **Example**:
```javascript
print("Hello, World!");
print("Value:", 42, "Boolean:", true);
```

##### `len(string)`
Returns the length of a string.
- **Parameters**: `string` - The string to measure
- **Returns**: Integer length
- **Example**:
```javascript
var text = "Hello";
var length = len(text); // Returns 5
```

##### `ord(character)`
Returns the ASCII code of a character.
- **Parameters**: `character` - Single character string
- **Returns**: Integer ASCII code
- **Example**:
```javascript
var code = ord("A"); // Returns 65
```

##### `chr(code)`
Returns the character corresponding to an ASCII code.
- **Parameters**: `code` - Integer ASCII code
- **Returns**: Single character string
- **Example**:
```javascript
var char = chr(65); // Returns "A"
```

##### `__str_get__(string, index)`
Returns the character at a specific index in a string.
- **Parameters**: 
  - `string` - The source string
  - `index` - Zero-based index position
- **Returns**: Single character string
- **Example**:
```javascript
var char = __str_get__("Hello", 1); // Returns "e"
```

#### Time Functions

##### `time_now()`
Returns the current timestamp in seconds since Unix epoch.
- **Parameters**: None
- **Returns**: Float timestamp
- **Example**:
```javascript
var now = time_now();
print("Current time:", now);
```

##### `time_ms()`
Returns the current timestamp in milliseconds since Unix epoch.
- **Parameters**: None
- **Returns**: Integer timestamp in milliseconds
- **Example**:
```javascript
var now_ms = time_ms();
print("Current time (ms):", now_ms);
```

##### `sleep(seconds)`
Pauses execution for the specified number of seconds.
- **Parameters**: `seconds` - Number of seconds to sleep (can be float)
- **Returns**: `null`
- **Example**:
```javascript
print("Before sleep");
sleep(2.5); // Sleep for 2.5 seconds
print("After sleep");
```

#### HTTP Functions

##### `http_get(url)`
Makes an HTTP GET request to the specified URL.
- **Parameters**: `url` - String URL to request
- **Returns**: String response body or `null` if failed
- **Example**:
```javascript
var response = http_get("https://api.example.com/data");
if (response) {
    print("Response:", response);
} else {
    print("Request failed");
}
```

##### `http_get_status(url)`
Makes an HTTP GET request and returns only the status code.
- **Parameters**: `url` - String URL to request
- **Returns**: Integer HTTP status code or `null` if failed
- **Example**:
```javascript
var status = http_get_status("https://api.example.com/health");
print("Status code:", status);
```

#### GUI Functions

##### `gui_create_window(title, width, height)`
Creates a new GUI window.
- **Parameters**: 
  - `title` - String window title
  - `width` - Integer window width in pixels
  - `height` - Integer window height in pixels
- **Returns**: Integer window ID
- **Example**:
```javascript
var window_id = gui_create_window("My App", 400, 300);
```

##### `gui_add_label(window_id, text, x, y)`
Adds a text label to a window.
- **Parameters**:
  - `window_id` - Integer window ID
  - `text` - String label text
  - `x` - Integer X position
  - `y` - Integer Y position
- **Returns**: `null`
- **Example**:
```javascript
gui_add_label(window_id, "Hello, World!", 10, 10);
```

##### `gui_add_button(window_id, text, x, y, callback)`
Adds a clickable button to a window.
- **Parameters**:
  - `window_id` - Integer window ID
  - `text` - String button text
  - `x` - Integer X position
  - `y` - Integer Y position
  - `callback` - Function to call when clicked
- **Returns**: `null`
- **Example**:
```javascript
func onButtonClick() {
    print("Button was clicked!");
}

gui_add_button(window_id, "Click Me", 10, 50, onButtonClick);
```

##### `gui_show_window(window_id)`
Displays a window and starts the GUI event loop.
- **Parameters**: `window_id` - Integer window ID
- **Returns**: `null`
- **Example**:
```javascript
gui_show_window(window_id);
```

### Standard Library Classes

#### Window Class (gui.xor)

##### Constructor
```javascript
var window = new Window(title, width, height);
```

##### Methods

###### `addLabel(text, x, y)`
Adds a label to the window.
- **Parameters**: `text` (string), `x` (number), `y` (number)

###### `addButton(text, x, y, callback)`
Adds a button to the window.
- **Parameters**: `text` (string), `x` (number), `y` (number), `callback` (function)

###### `show()`
Displays the window.

#### String Utilities (string.xor)

##### `startsWith(str, prefix)`
Checks if a string starts with a prefix.

##### `endsWith(str, suffix)`
Checks if a string ends with a suffix.

##### `contains(str, substring)`
Checks if a string contains a substring.

##### `toUpperCase(str)`
Converts a string to uppercase.

##### `toLowerCase(str)`
Converts a string to lowercase.

##### `trim(str)`
Removes whitespace from both ends of a string.

#### Collection Utilities (collections.xor)

##### Array Class
Provides array functionality with methods like `push`, `pop`, `get`, `set`, `size`.

##### List Class
Dynamic list implementation with utility methods.

---

## مرجع API فارسی

### توابع داخلی

#### توابع اصلی

##### `print(...args)`
مقادیر را در کنسول چاپ می‌کند.
- **پارامترها**: هر تعداد مقدار
- **بازگشت**: `null`
- **مثال**:
```javascript
print("سلام دنیا!");
print("مقدار:", 42, "بولی:", true);
```

##### `len(string)`
طول یک رشته را برمی‌گرداند.
- **پارامترها**: `string` - رشته برای اندازه‌گیری
- **بازگشت**: طول عدد صحیح
- **مثال**:
```javascript
var text = "سلام";
var length = len(text); // 4 برمی‌گرداند
```

##### `ord(character)`
کد ASCII یک کاراکتر را برمی‌گرداند.
- **پارامترها**: `character` - رشته تک کاراکتری
- **بازگشت**: کد ASCII عدد صحیح
- **مثال**:
```javascript
var code = ord("A"); // 65 برمی‌گرداند
```

##### `chr(code)`
کاراکتر مربوط به کد ASCII را برمی‌گرداند.
- **پارامترها**: `code` - کد ASCII عدد صحیح
- **بازگشت**: رشته تک کاراکتری
- **مثال**:
```javascript
var char = chr(65); // "A" برمی‌گرداند
```

##### `__str_get__(string, index)`
کاراکتر در ایندکس مشخص در رشته را برمی‌گرداند.
- **پارامترها**: 
  - `string` - رشته منبع
  - `index` - موقعیت ایندکس مبتنی بر صفر
- **بازگشت**: رشته تک کاراکتری
- **مثال**:
```javascript
var char = __str_get__("سلام", 1); // "ل" برمی‌گرداند
```

#### توابع زمان

##### `time_now()`
زمان فعلی را بر حسب ثانیه از Unix epoch برمی‌گرداند.
- **پارامترها**: هیچ
- **بازگشت**: زمان اعشاری
- **مثال**:
```javascript
var now = time_now();
print("زمان فعلی:", now);
```

##### `time_ms()`
زمان فعلی را بر حسب میلی‌ثانیه از Unix epoch برمی‌گرداند.
- **پارامترها**: هیچ
- **بازگشت**: زمان عدد صحیح به میلی‌ثانیه
- **مثال**:
```javascript
var now_ms = time_ms();
print("زمان فعلی (میلی‌ثانیه):", now_ms);
```

##### `sleep(seconds)`
اجرا را برای تعداد مشخصی ثانیه متوقف می‌کند.
- **پارامترها**: `seconds` - تعداد ثانیه برای خواب (می‌تواند اعشاری باشد)
- **بازگشت**: `null`
- **مثال**:
```javascript
print("قبل از خواب");
sleep(2.5); // 2.5 ثانیه بخواب
print("بعد از خواب");
```

#### توابع HTTP

##### `http_get(url)`
درخواست HTTP GET به URL مشخص شده ارسال می‌کند.
- **پارامترها**: `url` - رشته URL برای درخواست
- **بازگشت**: بدنه پاسخ رشته یا `null` در صورت شکست
- **مثال**:
```javascript
var response = http_get("https://api.example.com/data");
if (response) {
    print("پاسخ:", response);
} else {
    print("درخواست ناموفق");
}
```

##### `http_get_status(url)`
درخواست HTTP GET ارسال می‌کند و فقط کد وضعیت را برمی‌گرداند.
- **پارامترها**: `url` - رشته URL برای درخواست
- **بازگشت**: کد وضعیت HTTP عدد صحیح یا `null` در صورت شکست
- **مثال**:
```javascript
var status = http_get_status("https://api.example.com/health");
print("کد وضعیت:", status);
```

#### توابع GUI

##### `gui_create_window(title, width, height)`
پنجره GUI جدید ایجاد می‌کند.
- **پارامترها**: 
  - `title` - عنوان پنجره رشته
  - `width` - عرض پنجره عدد صحیح به پیکسل
  - `height` - ارتفاع پنجره عدد صحیح به پیکسل
- **بازگشت**: شناسه پنجره عدد صحیح
- **مثال**:
```javascript
var window_id = gui_create_window("برنامه من", 400, 300);
```

##### `gui_add_label(window_id, text, x, y)`
برچسب متنی به پنجره اضافه می‌کند.
- **پارامترها**:
  - `window_id` - شناسه پنجره عدد صحیح
  - `text` - متن برچسب رشته
  - `x` - موقعیت X عدد صحیح
  - `y` - موقعیت Y عدد صحیح
- **بازگشت**: `null`
- **مثال**:
```javascript
gui_add_label(window_id, "سلام دنیا!", 10, 10);
```

##### `gui_add_button(window_id, text, x, y, callback)`
دکمه قابل کلیک به پنجره اضافه می‌کند.
- **پارامترها**:
  - `window_id` - شناسه پنجره عدد صحیح
  - `text` - متن دکمه رشته
  - `x` - موقعیت X عدد صحیح
  - `y` - موقعیت Y عدد صحیح
  - `callback` - تابع برای فراخوانی هنگام کلیک
- **بازگشت**: `null`
- **مثال**:
```javascript
func onButtonClick() {
    print("دکمه کلیک شد!");
}

gui_add_button(window_id, "کلیک کن", 10, 50, onButtonClick);
```

##### `gui_show_window(window_id)`
پنجره را نمایش می‌دهد و حلقه رویداد GUI را شروع می‌کند.
- **پارامترها**: `window_id` - شناسه پنجره عدد صحیح
- **بازگشت**: `null`
- **مثال**:
```javascript
gui_show_window(window_id);
```
