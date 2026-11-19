<div align="center">

![Markdown to EPUB Lite banner](https://capsule-render.vercel.app/api?type=waving&color=0:#4338ca,100:#0f766e&height=170&section=header&text=Markdown%20to%20EPUB%20Lite&fontSize=34&fontColor=ffffff)

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=18&pause=1000&color=0f766e&center=true&vCenter=true&width=720&lines=Turn%20Markdown%20into%20a%20portable%20ebook%3BEPUB%203%20with%20no%20dependencies" alt="Typing SVG" />

[![MIT](https://img.shields.io/badge/license-MIT-0f766e.svg)](LICENSE)
[![Python](https://img.shields.io/badge/language-Python-blue.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/CyberLoop-dev/md2epub-lite?style=flat)](https://github.com/CyberLoop-dev/md2epub-lite/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/CyberLoop-dev/md2epub-lite)](https://github.com/CyberLoop-dev/md2epub-lite/commits/main)

**A tiny Markdown-to-EPUB 3 converter with no external packages.**

<img src="assets/illustration.svg" alt="Markdown to EPUB Lite illustration" width="560" />

</div>

## 🧭 Overview

Markdown to EPUB Lite converts a practical subset of Markdown into a valid EPUB 3 archive. It creates the required package metadata, navigation document, XHTML chapter, stylesheet, and correctly ordered mimetype entry.

## ✨ Features

- 📘 Builds an EPUB 3 archive from one Markdown file.
- 🧱 Supports headings, paragraphs, lists, blockquotes, and fenced code.
- 🧭 Generates a navigation table of contents from headings.
- 📦 Uses only Python's standard library and zipfile.
- 🔒 Converts local files without network access.

## 🖥️ Demo

```bash
python main.py examples/chapter.md -o chapter.epub --title "A Small Guide" --author "Example Author"
```
Open the generated EPUB in any compatible ebook reader.

## 🚀 Quick Start

```bash
git clone https://github.com/CyberLoop-dev/md2epub-lite.git
cd md2epub-lite
python main.py examples/chapter.md -o chapter.epub
```

## 🧱 Tech Stack

- 🐍 Python 3.10+
- 📦 Standard library: html, uuid, zipfile, xml-safe string generation

## 🗂️ Folder Structure

```text
md2epub-lite/
├── main.py
├── examples/chapter.md
├── tests/test_main.py
├── pyproject.toml
├── assets/illustration.svg
├── .gitignore
└── README.md
```

## 🛣️ Roadmap

- [x] EPUB 3 package and navigation
- [x] Basic Markdown blocks
- [ ] Inline image embedding

## 🤝 Contributing

Issues and pull requests are welcome. Please include a clear reproduction or sample input and keep changes focused.

## 📄 License

Released under the [MIT License](LICENSE).

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:#0f766e,100:#4338ca&height=100&section=footer)

</div>
