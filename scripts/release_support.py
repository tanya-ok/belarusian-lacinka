"""Build public source notes and record exact release inputs and outputs."""
from pathlib import Path
from hashlib import sha256
from html import escape
from urllib.parse import quote
import json
import re

EDITION = '0.5'
PUBLIC = {
    'index.html': 'publishing/index.html',
    'read.html': 'publishing/read.html',
    'stork-scenes.png': 'assets/stork-scenes.png',
    'sources.html': 'publishing/sources.html',
    'rights.txt': 'publishing/rights.txt',
    'font-license.txt': 'assets/fonts/OFL.txt',
    'cover.png': 'assets/cover.png',
    'belarusian-lacinka-b6-slim.pdf': 'output/pdf/belarusian-lacinka-b6-slim.pdf',
    'belarusian-lacinka-b6-slim-on-a4.pdf': 'output/pdf/belarusian-lacinka-b6-slim-on-a4.pdf',
}

def input_paths(root):
    files=['content/book.json','research/sources.md','README.md','requirements.txt',
           'publishing/index.html','publishing/rights.txt','publishing/pages.yml.example']
    files += [str(p.relative_to(root)) for p in (root/'scripts').glob('*.py')]
    files += [str(p.relative_to(root)) for p in (root/'.github/workflows').glob('*.yml')]
    files += [str(p.relative_to(root)) for p in (root/'assets').rglob('*') if p.is_file()]
    return sorted(set(files))

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def inline(text):
    pattern=r'\[([^\]]+)\]\((https://(?:[^\s()]|\([^\s()]*\))*)\)'
    pieces=[];pos=0
    for m in re.finditer(pattern,text):
        pieces.append(escape(text[pos:m.start()]))
        pieces.append('<a href="'+escape(quote(m[2],safe=':/?=&%#'),quote=True)+'">'+escape(m[1])+'</a>')
        pos=m.end()
    pieces.append(escape(text[pos:]))
    return ''.join(pieces)

def finish_release(root):
    from build_reader import build_reader
    build_reader(root)
    fragments=[]
    for line in (root/'research/sources.md').read_text().splitlines():
        if not line.strip(): continue
        if line.startswith('# '): fragments.append('<h1>'+inline(line[2:])+'</h1>')
        elif line.startswith('## '): fragments.append('<h2>'+inline(line[3:])+'</h2>')
        else: fragments.append('<p>'+inline(line)+'</p>')
    html='''<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sources | Belarusian Lacinka</title>
<style>body{background:#f8f2e5;color:#28231f;font:17px/1.7 Georgia,serif;margin:0}main{max-width:850px;margin:40px auto;padding:0 24px}a,h1,h2{color:#5a6c4d}a{overflow-wrap:anywhere}h1{line-height:1.2}footer{border-top:1px solid #c9bda7;margin-top:32px}</style>
<main><a href="index.html">Back to the book</a>'''+''.join(fragments)+'''
<footer><p>The information provided is intended solely for educational and research purposes.</p>
<a href="rights.txt">Rights and font notices</a></footer></main></html>'''
    (root/'publishing/sources.html').write_text(html)
    manifest={'edition':EDITION,
              'inputs':{p:digest(root/p) for p in input_paths(root)},
              'outputs':{p:digest(root/p) for p in sorted(set(PUBLIC.values()))},
              'public_files':PUBLIC}
    (root/'output/release-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
