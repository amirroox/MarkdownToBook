import os
import re
import markdown
from weasyprint import HTML
import warnings
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.request import pathname2url
import glob
import subprocess
import json
import time
from dotenv import load_dotenv

load_dotenv()
# Start Time
start_time = time.perf_counter()

warnings.filterwarnings("ignore")

# Details
BOOK_TITLE = os.getenv("BOOK_TITLE")
AUTHOR = os.getenv("AUTHOR")
PUBLISHER = os.getenv("PUBLISHER")
TRANSLATOR = os.getenv("TRANSLATOR")
SOURCE_LANG = os.getenv("SOURCE_LANG")
TARGET_LANG = os.getenv("TARGET_LANG")
YEAR_TRANSLATE = os.getenv("YEAR_TRANSLATE")
REV_NUMBER = os.getenv("REV_NUMBER")
SOURCE = os.getenv("SOURCE")
YEAR_PUB = os.getenv("YEAR_PUB")

# Config
LOG_FLAG = os.getenv("LOG_FLAG")
ASSETS_DIR = os.getenv("ASSETS_DIR")
CUSTOM_DIR = os.getenv("CUSTOM_DIR")
BOOK_DIR = os.getenv("BOOK_DIR")
ASSETS_BOOK_DIR = os.getenv("ASSETS_BOOK_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
NAME_OUTPUT = BOOK_TITLE
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{NAME_OUTPUT}.pdf")

FOREWORD = ""
if not FOREWORD:
    with open(f'./{CUSTOM_DIR}/Foreword.txt', 'r', encoding='UTF-8') as file:
        FOREWORD = file.read()

TRANSLATORS = []
DEFAULT_TRANSLATOR_IMAGE = f"{ASSETS_DIR}/default-avatar.png"
if os.path.exists(f'{CUSTOM_DIR}/translators.json'):
    with open(f'{CUSTOM_DIR}/translators.json', 'r', encoding='utf-8') as f:
        TRANSLATORS = json.load(f)

# Style
COLOR_HEADER = os.getenv("COLOR_HEADER")
COLOR_CODE = os.getenv("COLOR_CODE")
COLOR_TABLE = os.getenv("COLOR_TABLE")
MAIN_FONT = os.getenv("MAIN_FONT")

# Assets
PRISM_CSS_PATH = f"{ASSETS_DIR}/prism.css"
PRISM_JS_PATH = f"{ASSETS_DIR}/prism.js"
NODE_HIGHLIGHTER = f"{ASSETS_DIR}/highlight.js"

os.makedirs(OUTPUT_DIR, exist_ok=True)

PROJECT_ROOT = os.path.dirname(os.path.abspath(BOOK_DIR))
if not PROJECT_ROOT:
    PROJECT_ROOT = os.getcwd()

print(f"Project Root: {PROJECT_ROOT}")
print(f"Book Directory: {os.path.abspath(BOOK_DIR)}")
print(f"Assets Directory: {os.path.abspath(ASSETS_BOOK_DIR)}")
print(f"Helper Directory: {os.path.abspath(ASSETS_DIR)}")

cover_image_path = f"{ASSETS_DIR}/cover.jpg"
if os.path.exists(f"{CUSTOM_DIR}"):
    cover_patterns = [
        os.path.join(f"{CUSTOM_DIR}", "cover.*"),
        os.path.join(f"{CUSTOM_DIR}", "Cover.*"),
        os.path.join(f"{CUSTOM_DIR}", "COVER.*")
    ]
    for pattern in cover_patterns:
        matches = glob.glob(pattern)
        if matches:
            cover_image_path = matches[0]
            print(f"Found cover image: {cover_image_path}")
            break

prism_css = ""
if os.path.exists(PRISM_CSS_PATH):
    with open(PRISM_CSS_PATH, "r", encoding="utf-8") as f:
        prism_css = f.read()
    print(f"Loaded Prism CSS from: {PRISM_CSS_PATH}")
else:
    print(f"Prism CSS not found, using fallback")
    prism_css = """
code[class*="language-"],
pre[class*="language-"] {
    color: #ccc;
    background: none;
    font-family: Consolas, Monaco, 'Andale Mono', 'Ubuntu Mono', monospace;
    font-size: 9pt;
    text-align: left;
    white-space: pre;
    word-spacing: normal;
    word-break: normal;
    word-wrap: normal;
    line-height: 1.5;
    tab-size: 4;
    hyphens: none;
}

pre[class*="language-"] {
    padding: 1em;
    margin: .5em 0;
    overflow: auto;
}

:not(pre) > code[class*="language-"],
pre[class*="language-"] {
    background: #2d2d2d;
}

:not(pre) > code[class*="language-"] {
    padding: .1em;
    border-radius: .3em;
    white-space: normal;
}

.token.comment,
.token.block-comment,
.token.prolog,
.token.doctype,
.token.cdata {
    color: #999;
}

.token.punctuation {
    color: #ccc;
}

.token.tag,
.token.attr-name,
.token.namespace,
.token.deleted {
    color: #e2777a;
}

.token.function-name {
    color: #6196cc;
}

.token.boolean,
.token.number,
.token.function {
    color: #f08d49;
}

.token.property,
.token.class-name,
.token.constant,
.token.symbol {
    color: #f8c555;
}

.token.selector,
.token.important,
.token.atrule,
.token.keyword,
.token.builtin {
    color: #cc99cd;
}

.token.string,
.token.char,
.token.attr-value,
.token.regex,
.token.variable {
    color: #7ec699;
}

.token.operator,
.token.entity,
.token.url {
    color: #67cdcc;
}

.token.important,
.token.bold {
    font-weight: bold;
}

.token.italic {
    font-style: italic;
}

.token.entity {
    cursor: help;
}

.token.inserted {
    color: green;
}
"""


def format_seconds(s: float) -> str:
    hrs, rem = divmod(int(s), 3600)
    mins, secs = divmod(rem, 60)
    millis = int((s - int(s)) * 1000)
    return f"{hrs:02d}:{mins:02d}:{secs:02d}.{millis:03d}"


def contains_persian(text):
    persian_pattern = re.compile(r'[\u0600-\u06FF]')
    return bool(persian_pattern.search(text))


def preprocess_markdown(markdown_text):
    pattern_h = r'(<div[^>]*>)\s*!\[([^\]]*)\]\(([^\)]+)\)\s*(</div>)'

    def replace_img(match):
        div_open = match.group(1)
        alt_text = match.group(2)
        image_path = match.group(3)
        div_close = match.group(4)
        return f'{div_open}<img src="{image_path}" alt="{alt_text}" />{div_close}'

    markdown_text = re.sub(pattern_h, replace_img, markdown_text)
    return markdown_text


def normalize_language(lang):
    aliases = {
        'c#': 'csharp',
        'cs': 'csharp',
        'js': 'javascript',
        'ts': 'typescript',
        'py': 'python',
        'sh': 'bash',
        'yml': 'yaml',
        'md': 'markdown'
    }
    if not lang:
        return None
    normalized = lang.lower().strip()
    return aliases.get(normalized, normalized)


def detect_language(code_text):
    if any(keyword in code_text for keyword in ["def ", "import ", "class ", "print("]):
        return "python"
    elif any(keyword in code_text for keyword in ["function ", "const ", "let ", "var ", "=>"]):
        return "javascript"
    elif any(keyword in code_text for keyword in ["public class", "void ", "static "]):
        return "java"
    elif any(keyword in code_text for keyword in ["using ", "namespace ", "void Main"]):
        return "csharp"
    elif "<html" in code_text or "<!DOCTYPE" in code_text:
        return "html"
    elif any(keyword in code_text for keyword in ["{", "}", "margin:", "padding:"]) and "def " not in code_text:
        return "css"
    else:
        return "markup"


def highlight_with_node(code, language=None):
    if not os.path.exists(NODE_HIGHLIGHTER):
        return None

    try:
        if language:
            result = subprocess.run(
                ['node', NODE_HIGHLIGHTER, code, language],
                capture_output=True,
                text=True,
                timeout=5,
                encoding='utf-8'
            )
        else:
            result = subprocess.run(
                ['node', NODE_HIGHLIGHTER, code],
                capture_output=True,
                text=True,
                timeout=5,
                encoding='utf-8'
            )

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Node error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Node highlighting failed: {e}")

    return None


def apply_prism_highlighting(HTML_content):
    soup_1 = BeautifulSoup(HTML_content, "html.parser")

    for pre in soup_1.find_all("pre"):
        code = pre.find("code")
        if code:
            existing_classes_h = code.get("class", [])
            has_language = any(cls.startswith("language-") for cls in existing_classes_h)

            code_text = code.get_text()
            language = None

            if has_language:
                raw_lang = next(
                    (cls.replace("language-", "") for cls in existing_classes_h if cls.startswith("language-")), None)
                language = normalize_language(raw_lang)

            if not language:
                language = detect_language(code_text)

            code["class"] = [f"language-{language}"]

            highlighted = highlight_with_node(code_text, language)

            if highlighted:
                code.clear()
                code.append(BeautifulSoup(highlighted, "html.parser"))
                if LOG_FLAG:
                    print(f"Highlighted with Node: {language}")

            pre_classes = pre.get("class", [])
            if f"language-{language}" not in pre_classes:
                pre["class"] = pre_classes + [f"language-{language}"]

    return str(soup_1)


chapters = []
chapter_titles = []

for root, dirs, files in os.walk(BOOK_DIR):
    for file in sorted(files):
        if file.endswith(".md"):
            full_path = os.path.join(root, file)
            chapters.append(full_path)

            with open(full_path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                if first_line.startswith("#"):
                    title = first_line.lstrip("#").strip()
                else:
                    title = os.path.splitext(file)[0]
                chapter_titles.append(title)

cover_image_src = ""
if cover_image_path:
    if os.name == 'nt':
        cover_image_src = 'file:///' + os.path.abspath(cover_image_path).replace('\\', '/')
    else:
        cover_image_src = 'file://' + pathname2url(os.path.abspath(cover_image_path))

html_content = f"""
<html lang="fa">
<head>
<meta charset="utf-8">
<style>
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;700&display=swap');

@page {{
    size: A4;
    margin: 1cm 1cm 2cm 1cm;

    @bottom-center {{
        content: counter(page);
        font-family: 'Vazirmatn', 'Segoe UI Emoji', 'Noto Color Emoji', 'Apple Color Emoji', sans-serif;
        font-size: 10pt;
        color: #666;
    }}
}}

@page cover {{
    margin: 0;
    @bottom-center {{
        content: none;
    }}
}}

@page toc {{
    @bottom-center {{
        content: none;
    }}
}}

body {{
    direction: rtl;
    text-align: justify;
    font-family: 'Vazirmatn', 'Segoe UI Emoji', 'Noto Color Emoji', 'Apple Color Emoji', sans-serif;
    font-size: {MAIN_FONT}; /* Main Font Text */
    line-height: 1.5;
    color: #222;
    background-color: #fff;
    margin: 0;
    padding: 0;
}}

.cover {{
    page: cover;
    width: 210mm;
    height: 297mm;
    margin: 0;
    padding: 0;
    page-break-after: always;
    overflow: hidden;
}}

.cover-image {{
    width: 100%;
    height: 100%;
    min-width: 100%;
    min-height: 100%;
    object-fit: cover;
    margin: 0;
    padding: 0;
    display: block;
}}

.info-page {{
    page-break-after: always;
    text-align: center;
    padding: 40px;
}}

.info-page h1 {{
    font-size: 30pt;
    color: {COLOR_HEADER};
    margin: 40px 0;
    text-align: left;
}}

.info-page .author {{
    font-size: 18pt;
    color: #666;
    margin: 20px 0;
}}

.info-page .author span{{
    color: {COLOR_HEADER};
}}

.info-page .page-count {{
    font-size: 16pt;
    color: #999;
    margin-top: 40px;
}}

.toc {{
    page: toc;
    page-break-after: always;
    padding: 20px;
}}

.toc h1 {{
    text-align: center;
    color: {COLOR_HEADER};
    font-size: 28pt;
    margin-bottom: 40px;
}}

.toc-item {{
    margin: 15px 0;
    padding: 10px;
    border-bottom: 1px dotted #ccc;
    display: flex;
    justify-content: space-between;
    font-size: 13pt;
}}

.toc-item .title {{
    flex: 1;
}}

.toc-item .page-num {{
    margin-left: 20px;
    color: #666;
}}

.chapter {{
    page-break-before: always;
}}

h1, h2, h3 {{
    color: {COLOR_HEADER};
    margin-top: 1.4em;
    text-align: right;
    page-break-after: avoid;
}}

h1 {{
    font-size: 24pt;
    border-bottom: 3px solid {COLOR_HEADER};
    padding-bottom: 10px;
}}

h2 {{
    font-size: 18pt;
}}

h3 {{
    font-size: 14pt;
}}

p {{
    text-align: justify;
    word-wrap: break-word;
    margin: 10px 0;
    text-indent: 20px;
}}

a {{
    color: #1a73e8 !important;
    text-decoration: underline !important;
}}

a:visited {{
    color: #1a73e8 !important;
}}

a.ltr-link {{
    direction: ltr;
    display: inline-block;
    unicode-bidi: embed;
}}

img {{
    display: block;
    margin: 1.5em auto;
    max-width: 90%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    page-break-inside: avoid;
}}

code {{
    background: #f4f4f4;
    padding: 2px 6px;
    border-radius: 3px;
    font-family: Consolas, Monaco, 'Andale Mono', monospace;
    color: #c7254e;
    font-size: 10pt;
}}

pre {{
    background: #2d2d2d;
    padding: 15px;
    border-radius: 5px;
    font-family: Consolas, Monaco, 'Andale Mono', monospace;
    direction: ltr;
    text-align: left;
    overflow-x: auto;
    white-space: pre-wrap;
    page-break-inside: avoid;
    border-left: 4px solid {COLOR_CODE};
    margin: 20px 0;
    line-height: 1.5;
}}

pre code {{
    background: transparent;
    padding: 0;
    color: #ccc;
    font-size: 9pt;
    display: block;
}}

{prism_css}

hr {{
    display: none;
}}

blockquote {{
    border-right: 4px solid {COLOR_CODE};
    margin: 1.5em 10px;
    padding: 10px 20px;
    background: #fafafa;
    font-style: italic;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    page-break-inside: avoid;
}}

th, td {{
    border: 1px solid #ddd;
    padding: 10px;
    text-align: right;
}}

th {{
    background-color: {COLOR_TABLE};
    color: white;
}}

div[align="center"] {{
    text-align: center;
}}

div[align="center"] img {{
    margin-left: auto;
    margin-right: auto;
}}
</style>
</head>
<body>

<div class="cover">
"""

if cover_image_src:
    html_content += f'    <img src="{cover_image_src}" class="cover-image" alt="Cover" />\n'

html_content += f"""</div>

<div class="info-page">
    <h1>{BOOK_TITLE}</h1>
    <!-- Translator -->
    <div class="author">مترجم: <span>{TRANSLATOR}</span></div>
    <div class="author">سال ترجمه: <span>{YEAR_TRANSLATE}</span></div>
    <div class="author">زبان مبدا: <span>{SOURCE_LANG}</span> - زبان مقصد: <span>{TARGET_LANG}</span></div>
    <div class="author">شماره ویرایش: <span>{REV_NUMBER}</span></div>
    <div class="author">منبع ترجمه: <span>{SOURCE}</span></div>
    <div class="author">نویسنده: <span>{AUTHOR}</span></div>
    <div class="author">انتشارات: <span>{PUBLISHER}</span></div>
    <div class="author">سال انتشار: <span>{YEAR_PUB}</span></div>
    <div class="page-count">تعداد بخش ها: {len(chapter_titles)}</div>
</div>

<div class="info-page">
    <h1>پیشگفتار مترجم</h1>
    <div class="author">{FOREWORD}</div>
</div>

<div class="info-page">
    <h1>ارتباط با ما</h1>
"""

for translator in TRANSLATORS:
    html_content += f"""
    <div style="margin: 20px 0; padding: 15px; border: 2px solid {COLOR_HEADER}; border-radius: 10px; display: flex; align-items: center; gap: 5%;">
"""

    if 'image' in translator:
        img_src = translator.get('image', DEFAULT_TRANSLATOR_IMAGE)

        if not img_src.startswith(('http://', 'https://')):
            if os.path.exists(img_src):
                if os.name == 'nt':
                    img_src = 'file:///' + os.path.abspath(img_src).replace('\\', '/')
                else:
                    img_src = 'file://' + pathname2url(os.path.abspath(img_src))
            else:
                img_src = DEFAULT_TRANSLATOR_IMAGE

        if img_src:
            html_content += f"""
                <div style="flex-shrink: 0;">
                    <img src="{img_src}" style="width: 100px; height: 100px; border-radius: 50%; object-fit: cover;" />
                </div>
            """

    html_content += '<div style="flex: 1; text-align: right;">'

    if 'name' in translator:
        html_content += f'<div style="font-size: 16pt; font-weight: bold; margin-bottom: 5px; color: {COLOR_HEADER};">{translator["name"]}</div>'

    if 'role' in translator:
        html_content += f'<div style="font-size: 12pt; color: #666; margin-bottom: 10px;">{translator["role"]}</div>'

    if 'email' in translator:
        html_content += f'<div style="font-size: 10pt; margin: 3px 0;">ایمیل: <a href="mailto:{translator["email"]}">{translator["email"]}</a></div>'

    if 'linkedin' in translator:
        html_content += f'<div style="font-size: 10pt; margin: 3px 0;">لینکدین: <a href="{translator["linkedin"]}" class="ltr-link">{translator["linkedin"]}</a></div>'

    if 'github' in translator:
        html_content += f'<div style="font-size: 10pt; margin: 3px 0;">گیت هاب: <a href="{translator["github"]}" class="ltr-link">{translator["github"]}</a></div>'

    if 'telegram' in translator:
        html_content += f'<div style="font-size: 10pt; margin: 3px 0;">تلگرام: <a href="https://t.me/{translator["telegram"].replace("@", "")}" class="ltr-link">{translator["telegram"]}</a></div>'

    if 'website' in translator:
        html_content += f'<div style="font-size: 10pt; margin: 3px 0;">وب‌سایت: <a href="{translator["website"]}" class="ltr-link">{translator["website"]}</a></div>'

    html_content += """
    </div>
    </div>
"""

html_content += """
<h4 style='text-align: center'>کلیه حقوق این ترجمه محفوظ و تحت حمایت قانون حق تکثیر است.</h4>
</div>

<div class="toc">
    <h1>فهرست مطالب</h1>
"""

for i, title in enumerate(chapter_titles, 1):
    anchor_id = f"chapter-{i}"
    html_content += f"""
    <div class="toc-item">
        <a href="#{anchor_id}" class="title">بخش {i}: {title}</a>
    </div>
"""

html_content += "</div>"

for i, md_path in enumerate(chapters):
    if LOG_FLAG:
        print(f"\nProcessing: {os.path.basename(md_path)}")

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    md_text = preprocess_markdown(md_text)

    html_body = markdown.markdown(
        md_text,
        extensions=[
            "fenced_code",
            "tables",
            "toc",
            "nl2br",
            "extra"
        ]
    )

    soup = BeautifulSoup(html_body, "html.parser")
    md_dir = os.path.dirname(os.path.abspath(md_path))

    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue

        src = src.replace("%20", " ")
        if LOG_FLAG:
            print(f"Image: {src}")

        if src.startswith(("http://", "https://", "data:", "file://")):
            if LOG_FLAG:
                print(f"Already absolute")
            continue

        levels_up = md_path.count(os.sep) - BOOK_DIR.count(os.sep)
        img_path = os.path.normpath(os.path.join(md_dir, src))

        if "../" in src:
            up_count = src.count("../")
            remaining_path = src.replace("../", "")
            current = md_dir
            for _ in range(up_count):
                current = os.path.dirname(current)
            img_path = os.path.normpath(os.path.join(current, remaining_path))

        if LOG_FLAG:
            print(f"Trying: {img_path}")

        if os.path.exists(img_path):
            if os.name == 'nt':
                file_uri = 'file:///' + img_path.replace('\\', '/')
            else:
                file_uri = 'file://' + pathname2url(img_path)

            img["src"] = file_uri
            if LOG_FLAG:
                print(f"Found!")
        else:
            print(f"Not found: {img_path}")

    for link in soup.find_all("a"):
        link_text = link.get_text()
        if not contains_persian(link_text):
            existing_classes = link.get("class", [])
            link["class"] = existing_classes + ["ltr-link"]

    html_body = str(soup)
    html_body = apply_prism_highlighting(html_body)

    anchor_id = f"chapter-{i + 1}"
    html_content += f"<div class='chapter' id='{anchor_id}'>{html_body}</div>"

html_content += "</body></html>"

debug_html_file = os.path.join(OUTPUT_DIR, f"{NAME_OUTPUT}.html")
with open(debug_html_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"\nHTML: {debug_html_file}")

base_uri = Path(PROJECT_ROOT).as_uri() + "/"
print(f"\nBase URI: {base_uri}")

HTML(string=html_content, base_url=base_uri).write_pdf(OUTPUT_FILE)

print(f"\nPDF created: {OUTPUT_FILE}")

# End Time
end_time = time.perf_counter()
print("Elapsed:", format_seconds(end_time - start_time))