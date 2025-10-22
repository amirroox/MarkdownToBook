<div dir="ltr">

[English version](./README.md)

</div>

<div dir="rtl">

# 📚 تدبیل کننده مارک داون به کتاب (PDF)

ابزاری بر پایه پایتون که فایل های مارک داون را تبدیل به کتاب میکنه.

## ✨ امکانات

- 📖 تبدیل چندین فایل مارک داون به یک کتاب
- 🎨 هایلایت سینتکس برای بیش از 20 زبان برنامه نویسی با استفاده از Prism.js
- 📑 تولید خودکار فهرست مطالب با لینک های قابل کلیک
- 🖼️ پشتیبانی از تصویر جلد سفارشی (تمام صفحه)
- 🌐 پشتیبانی از RTL برای متن‌های فارسی/عربی
- 📄 قالب‌بندی حرفه ایی کتاب با شماره صفحات
- 👥 پروفایل مترجمان/مشارکت کننده ها با عکس و لینک های اجتماعی
- 🔗 لینک های داخلی و خارجی قابل کلیک
- 📊 پشتیبانی از جداول، نقل قول ها و تصاویر
- ⚡ پردازش سریع عملکرد
- 🎯 رنگ ها، فونت ها و استایل های قابل تنظیم

## 📋 پیش نیاز ها

### وابستگی‌های پایتون

<div dir="ltr"> 

```bash
pip install markdown weasyprint beautifulsoup4 python-dotenv
```

</div>

### وابستگی‌های Node.js

<div dir="ltr"> 

```bash
npm install
```

</div>

## 📁 ساختار پروژه

<div dir="ltr"> 

```
project/
├── main.py                     # اسکریپت اصلی پایتون
├── package.json                # وابستگی های نود
├── assets/                     # فایل های کمکی
│   ├── highlight.js            # هایلایتر پریسم
│   ├── prism.css               # تم پریسم
│   ├── default-avatar.png      # آواتار پیشفرض مترجم
│   └── cover.jpg               # کاور پیشفرض
├── custom/                     # تنظیمات سفارشی کتاب
│   ├── cover.jpg               # تصویر کاور سفارشی
│   ├── Foreword.txt            # پیشگفتار مترجم
│   ├── translators.json        # اطلاعات مترجمان
│   └── translators1.jpg        # عکس سفارشی برای اطلاعات مترجمان
├── Book/
│   ├── markdown/               # فایل های مارک داون منبع (با شماره)
│   │   ├── 01-chapter.md
│   │   ├── 02-chapter.md
│   │   └── ...
│   └── assets/                 # تصاویر کتاب
│       └── images/
└── OutPDF/                     # پوشه خروجی (خودکار ساخته میشود)
    ├── BookTitle.pdf
    └── BookTitle.html
```

</div> 

## 🚀 شروع سریع

**۱. نصب وابستگی ها:**

<div dir="ltr"> 

```bash
pip install markdown weasyprint beautifulsoup4 python-dotenv
npm install
```

</div>

**۲. تنظیم کتاب:**
فایل `env_example.` را تغییر نام به `env.` بدهید و آن را ویرایش کنید:

<div dir="ltr"> 

```python
BOOK_TITLE = "عنوان کتاب شما"
AUTHOR = "نام نویسنده"
TRANSLATOR = "نام مترجم"
# ... سایر تنظیمات
```

</div>

**۳. آماده سازی محتوا:**
- فایل‌های مارک داون را به `Book/markdown` اضافه کنید
- تصاویر را به `Book/assets` اضافه کنید
- تصویر جلد را به `/custom` اضافه کنید (با نام `*.cover`)
- فایل `custom/Foreword.txt` را برای پیشگفتار مترجم بسازید
- مترجمان را در `custom/translators.json` تنظیم کنید

**۴. اجرا:**

<div dir="ltr"> 

```bash
python main.py
```

</div>

**۵. خروجی:**
- فایل کتاب (PDF): `OutPDF/YourBookTitle.pdf`
- فایل HTML (دیباگ): `OutPDF/YourBookTitle.html`

## ⚙️ تنظیمات

### جزئیات کتاب

<div dir="ltr"> 

```python
BOOK_TITLE="اسم کتاب"
AUTHOR="نویسنده"
PUBLISHER="منتشرکننده"
TRANSLATOR="مترجم"
SOURCE_LANG="زبان مبدا"
TARGET_LANG="زبان مقصد"
YEAR_TRANSLATE="سال انتشار ترجمه (عدد)"
REV_NUMBER="نسخه کناب (عدد)"
SOURCE="اسم کامل کتاب"
YEAR_PUB="سال انشتار کتاب (عدد)"
```

</div>

### استایل ها

<div dir="ltr"> 

```python
COLOR_HEADER = "#007BA7"    # سر تیترها و عنوانین
COLOR_CODE = "#007BA7"      # حاشیه بلوک های کد
COLOR_TABLE = "#007BA7"     # سرتیتر جداول
MAIN_FONT = "12pt"          # اندازه فونت پایه
```

</div>

### مسیرها

<div dir="ltr"> 

```python
BOOK_DIR = "Book/markdown"              # مسیر مارک داون کتاب
ASSETS_BOOK_DIR = "Book/assets"         # مسیر عکس های کتاب
OUTPUT_DIR = "OutPDF"                   # خروجی کتاب
```

</div>

## 👥 پروفایل مترجمان

فایل `custom/translators.json` را بسازید:

<div dir="ltr"> 

```json
[
  {
    "name": "دانیال",
    "role": "مترجم و طراح",
    "image": "assets/dani.jpg",
    "email": "amirroox@yahoo.com",
    "linkedin": "https://www.linkedin.com/in/amirroox",
    "github": "https://github.com/amirroox",
    "telegram": "@you_113",
    "website": "https://amirroox.ir"
  }
]
```

</div>

**فیلدهای پشتیبانی شده:**
- `name` - نام کامل مترجم
- `role` - عنوان شغلی/نقش (مثلا "مترجم"، "طراح کتاب")
- `image` - مسیر عکس یا URL (اختیاری، در صورت نبود از عکس پیش فرض استفاده میشود)
- `email` - ایمیل
- `linkedin` - آدرس پروفایل لینکدین
- `github` - آدرس پروفایل گیت هاب
- `telegram` - نام کاربری تلگرام (با یا بدون @)
- `website` - وب سایت شخصی

## 📝 امکانات مارک داون

### بلوک‌های کد با هایلایت سینتکس

<div dir="ltr"> 

````markdown
```python
def hello():
    print("سلام ایران آزاد")
```

```c#
static void Main() {
    Console.WriteLine("سلام");
}
```

```javascript
const greet = () => {
    console.log("سلام");
};
```
````

</div>

**زبان های پشتیبانی شده:**

Python, JavaScript, TypeScript, Java, C#, C, C++, Go, Rust, PHP, Ruby, Swift, Kotlin, HTML, CSS, SQL, JSON, YAML, XML, Bash, PowerShell, Docker, Git, Markdown

**نام‌های مستعار زبان ها:**
- `csharp` ← `c#`
- `javascript` ← `js`
- `typescript` ← `ts`
- `python` ← `py`
- `bash` ← `sh`
- `yaml` ← `yml`

### تصاویر

<div dir="ltr"> 

```markdown
![متن جایگزین](../assets/images/diagram.png)

<div align="center">
![تصویر وسط‌چین](../assets/images/logo.png)
</div>
```

</div>

### جداول

<div dir="ltr"> 

```markdown
| سرتیتر ۱ | سرتیتر ۲ | سرتیتر ۳ |
|----------|----------|----------|
| سلول ۱   | سلول ۲   | سلول ۳   |
| سلول ۴   | سلول ۵   | سلول ۶   |
```

</div>

### لینک ها

<div dir="ltr"> 

```markdown
[لینک خارجی](https://example.com)
[لینک داخلی](#chapter-1)
```

</div>

### نقش قول ها

<div dir="ltr"> 

```markdown
> این یک نکته مهم است
> که چند خط دارد
```

</div>

## 🎨 سفارشی سازی

### تغییر رنگ های تم

ثابت های رنگ را در `main.py` ویرایش کنید:

<div dir="ltr"> 

```python
COLOR_HEADER = "#FF5733"  # تم قرمز
COLOR_CODE = "#FF5733"
COLOR_TABLE = "#FF5733"
```

</div>

### تغییر فونت‌ها

<div dir="ltr"> 

```python
MAIN_FONT = "14pt"  # متن بزرگ‌تر
```

</div>

یا `font-family` را در بخش CSS قالب HTML ویرایش کنید.

### تم سفارشی Prism

۱. یک تم CSS Prism از [prismjs.com](https://prismjs.com/) دانلود کنید
۲. با نام `assets/prism.css` ذخیره کنید
۳. اسکریپت به طور خودکار آن را بارگذاری میکند

## 🔧 امکانات پیشرفته

### حالت دیباگ

فعال سازی لاگ گیری در فایل `env.`:

<div dir="ltr"> 

```python
LOG_FLAG = True
```

</div>

### ردیابی عملکرد

زمان اجرا به طور خودکار نمایش داده میشود:
```
Elapsed: 00:00:15.234
```

### تشخیص مسیر تصویر

پشتیبانی از فرمت های مسیر مختلف:
- نسبی: `assets/image.png/..`
- مطلق: `path/to/image.png/`
- لینک: `https://example.com/image.png`

### پیشگفتار سفارشی

فایل `custom/Foreword.txt` را با متن پیشگفتار مترجم بسازید.

## 🐛 عیب‌یابی

### مشکل: "Node highlighting failed"
**راه‌حل:** مطمئن شوید Node.js نصب است و `npm install` اجرا شده است.

### مشکل: تصاویر نمایش داده نمیشوند
**راه‌حل:** 
- مسیرهای تصویر را نسبت به فایل‌های مارک داون بررسی کنید
- اطمینان حاصل کنید تصاویر در `/Book/assets` وجود دارند
- پسوند فایل های تصویر را بررسی کنید

### مشکل: رندر یونیکد/ایموجی
**راه‌حل:** 
- ایموجی ها در PDF سیاه و سفید ظاهر می‌شوند (محدودیت WeasyPrint)
- از فونت های ایموجی استفاده کنید یا رندر تک رنگ را بپذیرید

### مشکل: جلد تمام صفحه نیست
**راه‌حل:** 
- رزولوشن تصویر جلد را بررسی کنید (توصیه شده: 2480×3508 برای A4 در 300 DPI)

## 📖 ساختار خروجی

کتاب (PDF) تولید شده شامل:

1. **صفحه جلد** - تصویر جلد تمام صفحه
2. **صفحه اطلاعات** - جزئیات کتاب، مترجم، اطلاعات انتشار
3. **پیشگفتار** - مقدمه مترجم
4. **پروفایل مشارکت کننده ها** - اطلاعات مترجم/تیم با عکس
5. **اطلاعیه کپی رایت** - اطلاعات حقوقی
6. **فهرست مطالب** - لینک های فصل قابل کلیک با شماره صفحه
7. **فصل ها** - محتوای قالب بندی شده

## 🎯 عملکرد

زمان‌های پردازش معمولی:
- کتاب کوچک (۱۰ فصل، ۵۰ صفحه): ~۵-۱۰ ثانیه
- کتاب متوسط (۲۰ فصل، ۲۰۰ صفحه): ~۱۵-۳۰ ثانیه
- کتاب بزرگ (۴۰+ فصل، ۵۰۰+ صفحه): ~۴۵-۹۰ ثانیه

عملکرد بستگی دارد به:
- تعداد بلوک‌های کد (هایلایت سینتکس)
- تعداد و اندازه تصاویر
- مشخصات سیستم

## 📜 مجوز [MIT](./LICENSE)

رایگان برای استفاده و تغییر در پروژه‌های شخصی و تجاری.

---

**با ❤️ ساخته شده برای ایجاد کتاب‌های فنی زیبا**

</div>