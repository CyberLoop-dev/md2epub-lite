#!/usr/bin/env python3
"""Convert a Markdown file to a simple EPUB 3 ebook."""
from __future__ import annotations
import argparse, html, re, sys, uuid, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

def inline(text: str) -> str:
    text=html.escape(text,quote=False)
    text=re.sub(r"`([^`]+)`",r"<code>\1</code>",text)
    text=re.sub(r"\*\*([^*]+)\*\*",r"<strong>\1</strong>",text)
    text=re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)",r"<em>\1</em>",text)
    text=re.sub(r"\[([^\]]+)\]\((https?://[^ )]+)\)",r'<a href="\2">\1</a>',text)
    return text

def render_markdown(source: str):
    lines=source.splitlines(); out=[]; toc=[]; paragraph=[]; in_code=False; code=[]; in_list=False
    def flush():
        if paragraph: out.append("<p>"+inline(" ".join(paragraph))+"</p>"); paragraph.clear()
    def close_list():
        nonlocal in_list
        if in_list: out.append("</ul>"); in_list=False
    for line in lines:
        if line.strip().startswith("```"):
            flush(); close_list()
            if in_code: out.append("<pre><code>"+html.escape("\n".join(code))+"</code></pre>"); code=[]; in_code=False
            else: in_code=True
            continue
        if in_code: code.append(line); continue
        if not line.strip(): flush(); close_list(); continue
        heading=re.match(r"^(#{1,6})\s+(.+)$",line)
        if heading:
            flush(); close_list(); level=len(heading.group(1)); label=heading.group(2).strip()
            slug=re.sub(r"[^a-z0-9]+","-",label.lower()).strip("-") or f"section-{len(toc)+1}"
            toc.append((level,label,slug)); out.append(f'<h{level} id="{slug}">{inline(label)}</h{level}>'); continue
        if re.match(r"^[-*]\s+",line):
            flush()
            if not in_list: out.append("<ul>"); in_list=True
            out.append("<li>"+inline(re.sub(r"^[-*]\s+","",line))+"</li>"); continue
        if line.startswith(">"):
            flush(); close_list(); out.append("<blockquote><p>"+inline(line[1:].strip())+"</p></blockquote>"); continue
        if re.match(r"^---+$",line.strip()):
            flush(); close_list(); out.append("<hr/>"); continue
        paragraph.append(line.strip())
    flush(); close_list()
    if in_code: out.append("<pre><code>"+html.escape("\n".join(code))+"</code></pre>")
    return "\n".join(out),toc

def build_epub(markdown: str, output: Path, title: str, author: str, language: str="en"):
    body,toc=render_markdown(markdown); uid="urn:uuid:"+str(uuid.uuid4())
    nav_items="".join(f'<li><a href="chapter.xhtml#{slug}">{html.escape(label)}</a></li>' for _,label,slug in toc)
    chapter=f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{escape(language)}"><head><title>{html.escape(title)}</title><link rel="stylesheet" type="text/css" href="styles.css"/></head><body><h1>{html.escape(title)}</h1>{body}</body></html>'''
    nav=f'''<?xml version="1.0" encoding="utf-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="{escape(language)}"><head><title>Contents</title></head><body><nav epub:type="toc" id="toc"><h1>Contents</h1><ol>{nav_items}</ol></nav></body></html>'''
    opf=f'''<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="book-id"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="book-id">{uid}</dc:identifier><dc:title>{html.escape(title)}</dc:title><dc:creator>{html.escape(author)}</dc:creator><dc:language>{escape(language)}</dc:language></metadata><manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/><item id="chapter" href="chapter.xhtml" media-type="application/xhtml+xml"/><item id="css" href="styles.css" media-type="text/css"/></manifest><spine><itemref idref="chapter"/></spine></package>'''
    container='<?xml version="1.0" encoding="UTF-8"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>'
    css="body{font-family:serif;line-height:1.6;margin:5%}h1,h2,h3{line-height:1.2}pre{white-space:pre-wrap;background:#eee;padding:1em}code{font-family:monospace}blockquote{border-left:3px solid #888;padding-left:1em;color:#555}"
    output.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output,"w") as book:
        book.writestr("mimetype","application/epub+zip",compress_type=zipfile.ZIP_STORED)
        book.writestr("META-INF/container.xml",container)
        book.writestr("OEBPS/content.opf",opf)
        book.writestr("OEBPS/nav.xhtml",nav)
        book.writestr("OEBPS/chapter.xhtml",chapter)
        book.writestr("OEBPS/styles.css",css)
    return {"output":str(output),"chapters":1,"toc_entries":len(toc),"bytes":output.stat().st_size}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("input",type=Path); ap.add_argument("-o","--output",type=Path,default=Path("book.epub"))
    ap.add_argument("--title"); ap.add_argument("--author",default="Unknown"); ap.add_argument("--language",default="en")
    args=ap.parse_args()
    try:
        source=args.input.read_text(encoding="utf-8")
        result=build_epub(source,args.output,args.title or args.input.stem,args.author,args.language)
    except OSError as exc: print(f"error: {exc}",file=sys.stderr); return 2
    print(f"Created {result['output']} ({result['bytes']} bytes; {result['toc_entries']} navigation entries)")
    return 0
if __name__=="__main__": raise SystemExit(main())
