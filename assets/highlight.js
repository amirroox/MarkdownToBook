const Prism = require('prismjs');
const loadLanguages = require('prismjs/components/');

loadLanguages([
    'python', 'javascript', 'java', 'csharp', 'css', 'html', 'markup',
    'c', 'cpp', 'go', 'rust', 'php', 'ruby', 'swift', 'kotlin',
    'typescript', 'sql', 'bash', 'powershell', 'json', 'yaml',
    'markdown', 'xml', 'docker', 'git'
]);

const fs = require('fs');
const path = require('path');

function detectLanguage(code) {
    if (/\b(def|import|class|print)\b/.test(code)) return 'python';
    if (/\b(function|const|let|var|=>)\b/.test(code)) return 'javascript';
    if (/\b(public class|void|static)\b/.test(code)) return 'java';
    if (/\b(using|namespace|void Main)\b/.test(code)) return 'csharp';
    if (/<html|<!DOCTYPE/.test(code)) return 'html';
    if (/[{}]|margin:|padding:/.test(code) && !/\bdef\b/.test(code)) return 'css';
    return 'markup';
}

const languageAliases = {
    'c#': 'csharp',
    'cs': 'csharp',
    'js': 'javascript',
    'ts': 'typescript',
    'py': 'python',
    'sh': 'bash',
    'yml': 'yaml',
    'md': 'markdown'
};

function normalizeLanguage(lang) {
    if (!lang) return null;
    const normalized = lang.toLowerCase().trim();
    return languageAliases[normalized] || normalized;
}

function highlightCode(code, language) {
    language = normalizeLanguage(language);

    if (!language) {
        language = detectLanguage(code);
    }

    const grammar = Prism.languages[language] || Prism.languages.markup;
    const highlighted = Prism.highlight(code, grammar, language);

    return `<pre class="language-${language}"><code class="language-${language}">${highlighted}</code></pre>`;
}

const args = process.argv.slice(2);

if (args.length === 0) {
    console.error('Usage: node highlight.js <code> [language]');
    process.exit(1);
}

const code = args[0];
const language = args[1] || null;

const highlighted = highlightCode(code, language);
console.log(highlighted);