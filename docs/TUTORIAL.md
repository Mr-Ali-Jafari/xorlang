# XorLang Tutorial | آموزش XorLang

## English Tutorial

### Getting Started

Welcome to XorLang! This tutorial will guide you through the basics of programming in XorLang, from simple variables to advanced GUI applications.

#### Your First Program

Let's start with the classic "Hello, World!" program:

```javascript
// hello.xor
print("Hello, World!");
```

Save this as `hello.xor` and run it:
```bash
python3 -m src.xorlang.cli hello.xor
```

### Variables and Data Types

#### Working with Numbers
```javascript
// Numbers can be integers or floats
var age = 25;
var price = 19.99;
var temperature = -5.5;

print("Age:", age);
print("Price: $" + price);
print("Temperature:", temperature, "°C");
```

#### Working with Strings
```javascript
var firstName = "John";
var lastName = "Doe";
var fullName = firstName + " " + lastName;

print("Full name:", fullName);
print("Name length:", len(fullName));

// Getting characters from strings
var firstChar = __str_get__(firstName, 0);
print("First character:", firstChar);
```

#### Working with Booleans
```javascript
var isStudent = true;
var hasJob = false;

if (isStudent) {
    print("Currently studying");
}

if (!hasJob) {
    print("Looking for employment");
}
```

### Functions

#### Basic Functions
```javascript
func greet(name) {
    return "Hello, " + name + "!";
}

func add(a, b) {
    return a + b;
}

func multiply(x, y) {
    var result = x * y;
    return result;
}

// Using functions
var message = greet("Alice");
print(message);

var sum = add(10, 20);
var product = multiply(5, 6);
print("Sum:", sum, "Product:", product);
```

#### Functions with Multiple Parameters
```javascript
func calculateArea(length, width, height) {
    var area = 2 * (length * width + width * height + height * length);
    return area;
}

func formatCurrency(amount, currency) {
    return currency + " " + amount;
}

var boxArea = calculateArea(10, 5, 3);
var price = formatCurrency(29.99, "$");
print("Box surface area:", boxArea);
print("Price:", price);
```

### Control Flow

#### Conditional Statements
```javascript
func checkGrade(score) {
    if (score >= 90) {
        return "A";
    } else {
        if (score >= 80) {
            return "B";
        } else {
            if (score >= 70) {
                return "C";
            } else {
                if (score >= 60) {
                    return "D";
                } else {
                    return "F";
                }
            }
        }
    }
}

var studentScore = 85;
var grade = checkGrade(studentScore);
print("Grade:", grade);
```

#### Loops
```javascript
// While loop - countdown
var count = 5;
print("Countdown:");
while (count > 0) {
    print(count);
    count = count - 1;
}
print("Blast off!");

// For loop - multiplication table
print("Multiplication table for 7:");
for (var i = 1; i <= 10; i = i + 1) {
    var result = 7 * i;
    print("7 x " + i + " = " + result);
}
```

### Object-Oriented Programming

#### Creating Classes
```javascript
class Person {
    func init(name, age) {
        this.name = name;
        this.age = age;
    }
    
    func introduce() {
        return "Hi, I'm " + this.name + " and I'm " + this.age + " years old.";
    }
    
    func haveBirthday() {
        this.age = this.age + 1;
        return "Happy birthday! Now I'm " + this.age;
    }
}

// Using the class
var person1 = new Person("Alice", 25);
var person2 = new Person("Bob", 30);

print(person1.introduce());
print(person2.introduce());

print(person1.haveBirthday());
```

#### More Complex Classes
```javascript
class BankAccount {
    func init(accountNumber, initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
    }
    
    func deposit(amount) {
        if (amount > 0) {
            this.balance = this.balance + amount;
            return "Deposited $" + amount + ". New balance: $" + this.balance;
        } else {
            return "Invalid deposit amount";
        }
    }
    
    func withdraw(amount) {
        if (amount > 0 && amount <= this.balance) {
            this.balance = this.balance - amount;
            return "Withdrew $" + amount + ". New balance: $" + this.balance;
        } else {
            return "Invalid withdrawal amount or insufficient funds";
        }
    }
    
    func getBalance() {
        return "Account " + this.accountNumber + " balance: $" + this.balance;
    }
}

var account = new BankAccount("12345", 1000);
print(account.getBalance());
print(account.deposit(250));
print(account.withdraw(100));
print(account.getBalance());
```

### GUI Programming

#### Creating Your First Window
```javascript
// Simple GUI application
var window = new Window("My First App", 400, 300);

// Add some text
window.addLabel("Welcome to XorLang GUI!", 50, 50);
window.addLabel("This is a simple application", 50, 80);

// Add a button
func onButtonClick() {
    print("Hello from GUI!");
}

window.addButton("Click Me", 50, 120, onButtonClick);

// Show the window
window.show();
```

#### Interactive GUI Application
```javascript
class Calculator {
    func init() {
        this.result = 0;
        this.window = new Window("Calculator", 300, 200);
        this.setupUI();
    }
    
    func setupUI() {
        this.window.addLabel("Simple Calculator", 50, 20);
        this.window.addLabel("Result: 0", 50, 50);
        
        this.window.addButton("Add 10", 50, 80, this.add10);
        this.window.addButton("Subtract 5", 150, 80, this.subtract5);
        this.window.addButton("Reset", 100, 120, this.reset);
    }
    
    func add10() {
        this.result = this.result + 10;
        print("Result:", this.result);
    }
    
    func subtract5() {
        this.result = this.result - 5;
        print("Result:", this.result);
    }
    
    func reset() {
        this.result = 0;
        print("Calculator reset");
    }
    
    func show() {
        this.window.show();
    }
}

var calc = new Calculator();
calc.show();
```

### HTTP Programming

#### Making Web Requests
```javascript
func fetchQuote() {
    print("Fetching inspirational quote...");
    
    var response = http_get("https://api.quotable.io/random");
    
    if (response) {
        print("Raw response:", response);
        
        // Simple JSON parsing (looking for "content" field)
        var content = "";
        var i = 0;
        var len_response = len(response);
        var inQuotes = false;
        var foundContent = false;
        
        while (i < len_response) {
            var char = __str_get__(response, i);
            
            if (char == '"') {
                inQuotes = !inQuotes;
            } else {
                if (inQuotes && foundContent) {
                    if (char == '"') {
                        break;
                    }
                    content = content + char;
                } else {
                    if (!inQuotes) {
                        // Look for "content": pattern
                        if (char == 'c') {
                            var substr = "";
                            for (var j = 0; j < 7; j = j + 1) {
                                if (i + j < len_response) {
                                    substr = substr + __str_get__(response, i + j);
                                }
                            }
                            if (substr == "content") {
                                foundContent = true;
                                i = i + 9; // Skip 'content":"'
                                continue;
                            }
                        }
                    }
                }
            }
            i = i + 1;
        }
        
        if (content != "") {
            print("Quote:", content);
        } else {
            print("Could not parse quote from response");
        }
    } else {
        print("Failed to fetch quote");
    }
}

// Check if a website is accessible
func checkWebsite(url) {
    var status = http_get_status(url);
    if (status) {
        if (status == 200) {
            print(url + " is accessible (Status: " + status + ")");
        } else {
            print(url + " returned status: " + status);
        }
    } else {
        print(url + " is not accessible");
    }
}

// Usage
fetchQuote();
checkWebsite("https://www.google.com");
checkWebsite("https://httpstat.us/404");
```

### Combining GUI and HTTP

#### Web-Enabled GUI Application
```javascript
class WeatherApp {
    func init() {
        this.window = new Window("Weather App", 400, 300);
        this.setupUI();
    }
    
    func setupUI() {
        this.window.addLabel("Simple Weather App", 50, 20);
        this.window.addLabel("Click to fetch weather data", 50, 60);
        
        this.window.addButton("Get Weather", 50, 100, this.fetchWeather);
        this.window.addButton("Check Status", 200, 100, this.checkAPI);
    }
    
    func fetchWeather() {
        print("Fetching weather data...");
        
        // Using a public weather API (example)
        var response = http_get("https://api.openweathermap.org/data/2.5/weather?q=London&appid=demo");
        
        if (response) {
            print("Weather data received!");
            print("Response:", response);
        } else {
            print("Failed to fetch weather data");
            print("Note: This example uses a demo API key");
        }
    }
    
    func checkAPI() {
        print("Checking API status...");
        var status = http_get_status("https://api.openweathermap.org");
        
        if (status) {
            print("API Status:", status);
        } else {
            print("API is not accessible");
        }
    }
    
    func show() {
        this.window.show();
    }
}

var app = new WeatherApp();
app.show();
```

### Best Practices

#### Code Organization
```javascript
// Use meaningful variable names
var userAge = 25;          // Good
var a = 25;                // Bad

// Use functions to organize code
func calculateTax(income, rate) {
    return income * rate;
}

func formatMoney(amount) {
    return "$" + amount;
}

// Use classes for related functionality
class ShoppingCart {
    func init() {
        this.items = 0;
        this.total = 0;
    }
    
    func addItem(price) {
        this.items = this.items + 1;
        this.total = this.total + price;
    }
    
    func getTotal() {
        return this.total;
    }
}
```

#### Error Handling
```javascript
func safeHttpRequest(url) {
    print("Making request to:", url);
    
    var response = http_get(url);
    if (response) {
        print("Success! Response length:", len(response));
        return response;
    } else {
        print("Request failed for:", url);
        return null;
    }
}

func safeDivision(a, b) {
    if (b == 0) {
        print("Error: Division by zero!");
        return null;
    }
    return a / b;
}
```

---

## آموزش فارسی

### شروع کار

به XorLang خوش آمدید! این آموزش شما را از مبانی برنامه‌نویسی در XorLang، از متغیرهای ساده تا برنامه‌های پیشرفته GUI راهنمایی می‌کند.

#### اولین برنامه شما

بیایید با برنامه کلاسیک "سلام دنیا!" شروع کنیم:

```javascript
// hello.xor
print("سلام دنیا!");
```

این را به عنوان `hello.xor` ذخیره کنید و اجرا کنید:
```bash
python3 -m src.xorlang.cli hello.xor
```

### متغیرها و انواع داده

#### کار با اعداد
```javascript
// اعداد می‌توانند صحیح یا اعشاری باشند
var age = 25;
var price = 19.99;
var temperature = -5.5;

print("سن:", age);
print("قیمت: $" + price);
print("دما:", temperature, "°C");
```

#### کار با رشته‌ها
```javascript
var firstName = "علی";
var lastName = "احمدی";
var fullName = firstName + " " + lastName;

print("نام کامل:", fullName);
print("طول نام:", len(fullName));

// دریافت کاراکترها از رشته‌ها
var firstChar = __str_get__(firstName, 0);
print("اولین کاراکتر:", firstChar);
```

#### کار با بولی‌ها
```javascript
var isStudent = true;
var hasJob = false;

if (isStudent) {
    print("در حال تحصیل");
}

if (!hasJob) {
    print("به دنبال کار");
}
```

### توابع

#### توابع پایه
```javascript
func greet(name) {
    return "سلام، " + name + "!";
}

func add(a, b) {
    return a + b;
}

func multiply(x, y) {
    var result = x * y;
    return result;
}

// استفاده از توابع
var message = greet("علی");
print(message);

var sum = add(10, 20);
var product = multiply(5, 6);
print("مجموع:", sum, "حاصل‌ضرب:", product);
```

### برنامه‌نویسی GUI

#### ایجاد اولین پنجره
```javascript
// برنامه GUI ساده
var window = new Window("اولین برنامه من", 400, 300);

// اضافه کردن متن
window.addLabel("به GUI زبان XorLang خوش آمدید!", 50, 50);
window.addLabel("این یک برنامه ساده است", 50, 80);

// اضافه کردن دکمه
func onButtonClick() {
    print("سلام از GUI!");
}

window.addButton("کلیک کنید", 50, 120, onButtonClick);

// نمایش پنجره
window.show();
```

### برنامه‌نویسی HTTP

#### انجام درخواست‌های وب
```javascript
func fetchQuote() {
    print("دریافت نقل قول الهام‌بخش...");
    
    var response = http_get("https://api.quotable.io/random");
    
    if (response) {
        print("پاسخ خام:", response);
        // پردازش ساده JSON
        // ... کد پردازش
    } else {
        print("دریافت نقل قول ناموفق");
    }
}

fetchQuote();
```

### بهترین روش‌ها

#### سازماندهی کد
```javascript
// از نام‌های معنادار برای متغیرها استفاده کنید
var userAge = 25;          // خوب
var a = 25;                // بد

// از توابع برای سازماندهی کد استفاده کنید
func calculateTax(income, rate) {
    return income * rate;
}

// از کلاس‌ها برای عملکردهای مرتبط استفاده کنید
class ShoppingCart {
    func init() {
        this.items = 0;
        this.total = 0;
    }
    
    func addItem(price) {
        this.items = this.items + 1;
        this.total = this.total + price;
    }
}
```

### نتیجه‌گیری

XorLang زبانی قدرتمند و انعطاف‌پذیر است که امکان ایجاد برنامه‌های متنوع از ساده تا پیچیده را فراهم می‌کند. با ترکیب قابلیت‌های GUI و HTTP، می‌توانید برنامه‌های تعاملی و متصل به وب ایجاد کنید.

برای یادگیری بیشتر، مثال‌های موجود در پوشه `examples/` را بررسی کنید و با ویژگی‌های مختلف زبان آزمایش کنید!
