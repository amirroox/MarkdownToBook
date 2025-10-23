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
from jinja2 import Environment, FileSystemLoader

load_dotenv()
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
LOG_FLAG = os.getenv("LOG_FLAG", "False").lower() == "true"
ASSETS_DIR = "assets"
CUSTOM_DIR = "custom"
BOOK_DIR = os.getenv("BOOK_DIR")
ASSETS_BOOK_DIR = os.getenv("ASSETS_BOOK_DIR")
OUTPUT_DIR = os.getenv("OUTPUT_DIR")
NAME_OUTPUT = BOOK_TITLE
OUTPUT_FILE = os.path.join(OUTPUT_DIR, f"{NAME_OUTPUT}.pdf")

# Foreword
FOREWORD = ""
if not FOREWORD:
    with open(f'./{CUSTOM_DIR}/Foreword.txt', 'r', encoding='UTF-8') as file:
        FOREWORD = file.read()

# Translators
TRANSLATORS = []
DEFAULT_TRANSLATOR_IMAGE = f"{ASSETS_DIR}/default-avatar.png"
if os.path.exists(f'{CUSTOM_DIR}/translators.json'):
    with open(f'{CUSTOM_DIR}/translators.json', 'r', encoding='utf-8') as f:
        TRANSLATORS = json.load(f)

# Convert translator image paths to file URIs
for translator in TRANSLATORS:
    if 'image' in translator:
        img_path = translator['image']

        if not img_path.startswith(('http://', 'https://')):
            if os.path.exists(img_path):
                if os.name == 'nt':
                    file_uri = 'file:///' + os.path.abspath(img_path).replace('\\', '/')
                else:
                    file_uri = 'file://' + pathname2url(os.path.abspath(img_path))
                translator['image'] = file_uri
            else:
                print(f"Warning: Translator image not found: {img_path}")
                if os.path.exists(DEFAULT_TRANSLATOR_IMAGE):
                    if os.name == 'nt':
                        file_uri = 'file:///' + os.path.abspath(DEFAULT_TRANSLATOR_IMAGE).replace('\\', '/')
                    else:
                        file_uri = 'file://' + pathname2url(os.path.abspath(DEFAULT_TRANSLATOR_IMAGE))
                    translator['image'] = file_uri

# Convert default image path
if os.path.exists(DEFAULT_TRANSLATOR_IMAGE):
    if os.name == 'nt':
        DEFAULT_TRANSLATOR_IMAGE = 'file:///' + os.path.abspath(DEFAULT_TRANSLATOR_IMAGE).replace('\\', '/')
    else:
        DEFAULT_TRANSLATOR_IMAGE = 'file://' + pathname2url(os.path.abspath(DEFAULT_TRANSLATOR_IMAGE))

# Style
DIRECTION = "ltr" if os.getenv("DIRECTION").lower() != "rtl" else "rtl"
COLOR_HEADER = os.getenv("COLOR_HEADER")
COLOR_CODE = os.getenv("COLOR_CODE")
COLOR_TABLE = os.getenv("COLOR_TABLE")
MAIN_FONT = os.getenv("MAIN_FONT")
PAGE_COUNTER_COLOR = os.getenv("PAGE_COUNTER_COLOR")
PAGE_COUNTER_FONT = os.getenv("PAGE_COUNTER_FONT")

# Assets
PRISM_CSS_PATH = f"{ASSETS_DIR}/prism.css"
NODE_HIGHLIGHTER = f"{ASSETS_DIR}/highlight.js"

os.makedirs(OUTPUT_DIR, exist_ok=True)

PROJECT_ROOT = os.path.dirname(os.path.abspath(BOOK_DIR))
if not PROJECT_ROOT:
    PROJECT_ROOT = os.getcwd()

print(f"Project Root: {PROJECT_ROOT}")
print(f"Book Directory: {os.path.abspath(BOOK_DIR)}")
print(f"Assets Directory: {os.path.abspath(ASSETS_BOOK_DIR)}")

# Cover image
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

# Prism CSS
PRISM_DEFAULT_PATH = f"{ASSETS_DIR}/prism_default.css"
prism_css = ""

if os.path.exists(PRISM_CSS_PATH):
    with open(PRISM_CSS_PATH, "r", encoding="utf-8") as f:
        prism_css = f.read()
    print(f"Loaded Prism CSS from: {PRISM_CSS_PATH}")
elif os.path.exists(PRISM_DEFAULT_PATH):
    with open(PRISM_DEFAULT_PATH, "r", encoding="utf-8") as f:
        prism_css = f.read()
    print(f"Loaded Prism CSS from: {PRISM_DEFAULT_PATH}")
else:
    print(f"Prism CSS not found, using fallback")


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

    return re.sub(pattern_h, replace_img, markdown_text)


def normalize_language(lang):
    aliases = {
        'c#': 'csharp', 'cs': 'csharp', 'js': 'javascript',
        'ts': 'typescript', 'py': 'python', 'sh': 'bash',
        'yml': 'yaml', 'md': 'markdown'
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
        cmd = ['node', NODE_HIGHLIGHTER, code]
        if language:
            cmd.append(language)
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5, encoding='utf-8')
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print(f"Node error: {result.stderr}")
    except Exception as e:
        print(f"Node highlighting failed: {e}")
    return None


def apply_prism_highlighting(HTML_content):
    soup_1 = BeautifulSoup(HTML_content, "html.parser")
    for pre in soup_1.find_all("pre"):
        code = pre.find("code")
        if code:
            existing_classes_h = code.get("class", [])  # noqa
            has_language = any(cls.startswith("language-") for cls in existing_classes_h)
            code_text = code.get_text()
            language = None

            if has_language:
                raw_lang = next(
                    (cls.replace("language-", "") for cls in existing_classes_h if cls.startswith("language-")), None)
                language = normalize_language(raw_lang)

            if not language:
                language = detect_language(code_text)

            code["class"] = [f"language-{language}"]  # noqa
            highlighted = highlight_with_node(code_text, language)

            if highlighted:
                code.clear()
                code.append(BeautifulSoup(highlighted, "html.parser"))
                if LOG_FLAG:
                    print(f"Highlighted with Node: {language}")

            pre_classes = pre.get("class", [])  # noqa
            if f"language-{language}" not in pre_classes:
                pre["class"] = pre_classes + [f"language-{language}"]  # noqa

    return str(soup_1)


# Load chapters
chapters = []
chapter_titles = []

for root, dirs, files in os.walk(BOOK_DIR):
    for file in sorted(files):
        if file.endswith(".md"):
            full_path = os.path.join(root, file)
            chapters.append(full_path)
            with open(full_path, "r", encoding="utf-8") as f:
                first_line = f.readline().strip()
                title = first_line.lstrip("#").strip() if first_line.startswith("#") else os.path.splitext(file)[0]
                chapter_titles.append(title)

# Cover image URI
cover_image_src = ""
if cover_image_path:
    if os.name == 'nt':
        cover_image_src = 'file:///' + os.path.abspath(cover_image_path).replace('\\', '/')
    else:
        cover_image_src = 'file://' + pathname2url(os.path.abspath(cover_image_path))

# Process chapters
chapters_html = ""
for i, md_path in enumerate(chapters):
    if LOG_FLAG:
        print(f"\nProcessing: {os.path.basename(md_path)}")

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    md_text = preprocess_markdown(md_text)
    html_body = markdown.markdown(md_text, extensions=["fenced_code", "tables", "toc", "nl2br", "extra"])
    soup = BeautifulSoup(html_body, "html.parser")
    md_dir = os.path.dirname(os.path.abspath(md_path))

    # Process images
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
            file_uri = 'file:///' + img_path.replace('\\', '/') if os.name == 'nt' else 'file://' + pathname2url(
                img_path)
            img["src"] = file_uri
            if LOG_FLAG:
                print(f"Found!")
        else:
            print(f"Not found: {img_path}")

    # Process links
    for link in soup.find_all("a"):
        link_text = link.get_text()
        if not contains_persian(link_text):
            existing_classes = link.get("class", [])  # noqa
            link["class"] = existing_classes + ["ltr-link"]  # noqa

    html_body = str(soup)
    html_body = apply_prism_highlighting(html_body)
    anchor_id = f"chapter-{i + 1}"
    chapters_html += f"<div class='chapter' id='{anchor_id}'>{html_body}</div>"

# Setup Jinja2
env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('book_template.html')
html_content = template.render(
    book_title=BOOK_TITLE,
    author=AUTHOR,
    publisher=PUBLISHER,
    translator=TRANSLATOR,
    source_lang=SOURCE_LANG,
    target_lang=TARGET_LANG,
    year_translate=YEAR_TRANSLATE,
    rev_number=REV_NUMBER,
    source=SOURCE,
    year_pub=YEAR_PUB,
    direction=DIRECTION,
    color_header=COLOR_HEADER,
    color_code=COLOR_CODE,
    color_table=COLOR_TABLE,
    main_font=MAIN_FONT,
    page_counter_font=PAGE_COUNTER_FONT,
    page_counter_color=PAGE_COUNTER_COLOR,
    prism_css=prism_css,
    cover_image_src=cover_image_src,
    chapter_titles=chapter_titles,
    chapters_html=chapters_html,
    translators=TRANSLATORS,
    default_translator_image=DEFAULT_TRANSLATOR_IMAGE,
    foreword=FOREWORD
)

# Save debug HTML
debug_html_file = os.path.join(OUTPUT_DIR, f"{NAME_OUTPUT}.html")
with open(debug_html_file, "w", encoding="utf-8") as f:
    f.write(html_content)
print(f"\nHTML: {debug_html_file}")

# Generate PDF
base_uri = Path(PROJECT_ROOT).as_uri() + "/"
print(f"\nBase URI: {base_uri}")
HTML(string=html_content, base_url=base_uri).write_pdf(OUTPUT_FILE)
print(f"\nPDF created: {OUTPUT_FILE}")

end_time = time.perf_counter()
print("Elapsed:", format_seconds(end_time - start_time))