<div dir="rtl">

[نسخه فارسی](./readme_fa.md)

</div>

# 📚 Markdown to PDF Book Converter

A powerful Python-based tool that converts Markdown files into professionally formatted PDF books with syntax highlighting, table of contents, custom cover pages, and multi-language support.

## ✨ Features

- 📖 Converts multiple Markdown files into a single PDF book
- 🎨 Syntax highlighting for 20+ programming languages using Prism.js
- 📑 Automatic table of contents generation with clickable links
- 🖼️ Custom cover image support (full-page)
- 🌐 RTL (Right-to-Left) support for Persian/Arabic text
- 📄 Professional book formatting with page numbers
- 👥 Translator/contributor profiles with photos and social links
- 🔗 Clickable internal and external links
- 📊 Support for tables, blockquotes, and images
- ⚡ Fast processing with performance metrics
- 🎯 Customizable colors, fonts, and styling

## 📋 Requirements

### Python Dependencies
```bash
pip install markdown weasyprint beautifulsoup4 python-dotenv Jinja2
```

### Node.js Dependencies
```bash
npm install
```

## 📁 Project Structure

```
project/
├── main.py                      # Main Python script
├── package.json                 # Node.js dependencies
├── assets/                      # Helper assets
│   ├── highlight.js             # Prism highlighter
│   ├── prism.css                # Prism CSS theme (optional)
│   ├── default-avatar.png       # Default translator avatar
    └── cover.jpg                # Default Cover
├── custom/                      # Custom book settings
│   ├── cover.jpg                # Custom cover image
│   ├── Foreword.txt             # Translator's foreword
│   └── translators.json         # Translator information
    └── translators1.jpg         # Custom photo for translators' information
├── Book/
│   ├── markdown/                # Markdown source files (With Number)
│   │   ├── 01-chapter.md
│   │   ├── 02-chapter.md
│   │   └── ...
│   └── assets/                  # Book images/assets
│       └── images/
└── OutPDF/                      # Output directory (auto-created)
    ├── BookTitle.pdf
    └── BookTitle.html
```

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install markdown weasyprint beautifulsoup4 python-dotenv Jinja2
   npm install
   ```

2. **Configure your book:**
   Rename the file `env_example.` to `env.` and edit it:
   ```python
   BOOK_TITLE = "Your Book Title"
   AUTHOR = "Author Name"
   TRANSLATOR = "Translator Name"
   # ... other settings
   ```

3. **Prepare content:**
   - Add Markdown files to `Book/markdown/`
   - Add images to `Book/assets/`
   - Add cover image to `custom/` (named `cover.*`)
   - Create `custom/Foreword.txt` for translator's preface
   - Configure translators in `custom/translators.json`

4. **Run the converter:**
   ```bash
   python main.py
   ```

5. **Output:**
   - PDF: `OutPDF/YourBookTitle.pdf`
   - Debug HTML: `OutPDF/YourBookTitle.html`

## ⚙️ Configuration

### Book Details
```python
BOOK_TITLE="Book Title"
AUTHOR="Author"
PUBLISHER="Publisher"
TRANSLATOR="Translator"
SOURCE_LANG="Source Language"
TARGET_LANG="Target Language"
YEAR_TRANSLATE="Year of Translation Publication (Number)"
REV_NUMBER="Release Number (Number)"
SOURCE="Full Book Name"
YEAR_PUB="Year of Book Publication (Number)"
```

### Styling
```python
DIRECTION="rtl"                     # Direction (rtl Or ltr)
COLOR_HEADER="#007BA7"              # Headers and titles color
COLOR_CODE="#007BA7"                # Code block borders color
COLOR_TABLE="#007BA7"               # Table headers color
MAIN_FONT="12pt"                    # Base font size
PAGE_COUNTER_COLOR="#666"           # counter page color
PAGE_COUNTER_FONT="10pt"            # counter page font size
```

### Paths
```python
BOOK_DIR = "Book/markdown"          # Book markdown path
ASSETS_BOOK_DIR = "Book/assets"     # Book images path
OUTPUT_DIR = "OutPDF"               # Book output
```

## 👥 Translator Profiles

Create `custom/translators.json`:

```json
[
  {
    "name": "Daniel",
    "role": "Translator and designer",
    "image": "custom/danial.jpg",
    "email": "amirroox@yahoo.com",
    "linkedin": "https://www.linkedin.com/in/amirroox",
    "github": "https://github.com/amirroox",
    "telegram": "@you_113",
    "website": "https://amirroox.ir"
  }
]
```

**Supported fields:**
- `name` - Translator's full name
- `role` - Job title/role (e.g., "Translator", "PDF Designer")
- `image` - Path to photo or URL (optional, uses default if missing)
- `email` - Contact email
- `linkedin` - LinkedIn profile URL
- `github` - GitHub profile URL
- `telegram` - Telegram username (with or without @)
- `website` - Personal website URL

## 📝 Markdown Features

### Code Blocks with Syntax Highlighting

````markdown
```python
def hello():
    print("Hello Free IRAN")
```

```c#
static void Main() {
    Console.WriteLine("Hello");
}
```

```javascript
const greet = () => {
    console.log("Hello");
};
```
````

**Supported Languages:**
Python, JavaScript, TypeScript, Java, C#, C, C++, Go, Rust, PHP, Ruby, Swift, Kotlin, HTML, CSS, SQL, JSON, YAML, XML, Bash, PowerShell, Docker, Git, Markdown

**Language Aliases:**
- `c#` → `csharp`
- `js` → `javascript`
- `ts` → `typescript`
- `py` → `python`
- `sh` → `bash`
- `yml` → `yaml`

### Images

```markdown
![Alt text](../assets/images/diagram.png)

<div align="center">
![Centered Image](../assets/images/logo.png)
</div>
```

### Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

### Links

```markdown
[External Link](https://example.com)
[Internal Link](#chapter-1)
```

### Blockquotes

```markdown
> This is an important note
> that spans multiple lines
```

## 🎨 Customization

### Change Theme Colors

Edit the color constants in `main.py`:
```python
COLOR_HEADER = "#FF5733"  # Red theme
COLOR_CODE = "#FF5733"
COLOR_TABLE = "#FF5733"
```

### Change Fonts

```python
MAIN_FONT = "14pt"  # Larger text
```

Or edit the CSS `font-family` in the HTML template section.

### Custom Prism Theme

1. Download a Prism CSS theme from [prismjs.com](https://prismjs.com/)
2. Save as `assets/prism.css`
3. The script will automatically load it

## 🔧 Advanced Features

### Debug Mode

Enable detailed logging:
```python
LOG_FLAG = True
```

### Performance Tracking

Execution time is automatically displayed:
```
Elapsed: 00:00:15.234
```

### Image Path Resolution

Supports multiple path formats:
- Relative: `../assets/image.png`
- Absolute: `/path/to/image.png`
- URLs: `https://example.com/image.png`

### Custom Foreword

Create `custom/Foreword.txt` with translator's preface text.

## 🐛 Troubleshooting

### Issue: "Node highlighting failed"
**Solution:** Ensure Node.js is installed and `npm install` has been run.

### Issue: Images not displaying
**Solution:** 
- Check image paths are correct relative to markdown files
- Ensure images exist in `Book/assets/`
- Verify image file extensions

### Issue: Unicode/Emoji rendering
**Solution:** 
- Emojis appear black & white in PDF (WeasyPrint limitation)
- Use emoji fonts or accept monochrome rendering

### Issue: Cover not full-page
**Solution:** 
- Verify cover image resolution (recommended: 2480×3508 for A4 at 300 DPI)

## 📖 Output Structure

The generated PDF contains:

1. **Cover Page** - Full-page cover image
2. **Info Page** - Book details, translator, publication info
3. **Foreword** - Translator's preface
4. **Contributor Profiles** - Translator/team information with photos
5. **Copyright Notice** - Rights information
6. **Table of Contents** - Clickable chapter links with page numbers
7. **Chapters** - Your formatted content

## 🎯 Performance

Typical processing times:
- Small book (10 chapters, 50 pages): ~5-10 seconds
- Medium book (20 chapters, 200 pages): ~15-30 seconds
- Large book (40+ chapters, 500+ pages): ~45-90 seconds

Performance depends on:
- Number of code blocks (syntax highlighting)
- Number and size of images
- System specifications

## 📜 License [MIT](./LICENSE)

Free to use and modify for personal and commercial projects.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional language support
- More styling themes
- Performance optimizations
- Enhanced image handling

## 🙏 Credits

- **Markdown Processing:** [Python-Markdown](https://python-markdown.github.io/)
- **PDF Generation:** [WeasyPrint](https://weasyprint.org/)
- **Syntax Highlighting:** [Prism.js](https://prismjs.com/)
- **HTML Parsing:** [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)
- **Templating Engine:** [Jinja](https://jinja.palletsprojects.com/en/stable/)

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section
2. Review the configuration options
3. Examine the debug HTML output
4. Verify all dependencies are installed

---

**Made with ❤️ for creating beautiful technical books**