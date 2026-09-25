"""Structural publication checks; visual and linguistic review remain separate."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from pypdf import PdfReader
import json
import re

ROOT=Path(__file__).resolve().parents[1]
reader=PdfReader(ROOT/'output/pdf/belarusian-lacinka-b6-slim.pdf')
printout=PdfReader(ROOT/'output/pdf/belarusian-lacinka-b6-slim-on-a4.pdf')
assert len(reader.pages)==34 and len(printout.pages)==17
art={4,9,16,21,27,32}
texts=[];link_count=0;fonts=set()
for n,page in enumerate(reader.pages,1):
    assert abs(float(page.mediabox.width)-105/25.4*72)<.01
    assert abs(float(page.mediabox.height)-175/25.4*72)<.01
    assert len(page.images)==(1 if n in art or n==1 else 0)
    text=page.extract_text();texts.append(text)
    if n>1: assert text.strip().endswith(str(n)),n
    for font in page['/Resources'].get('/Font',{}).get_object().values():
        font=font.get_object();name=str(font.get('/BaseFont',''));fonts.add(name)
        assert not any(old in name for old in ['Arial','Georgia'])
        if font.get('/Subtype')=='/TrueType':
            assert 'Noto' in name
            assert '/FontFile2' in font['/FontDescriptor']
    for annot in page.get('/Annots',[]):
        annot=annot.get_object()
        assert annot['/Subtype']=='/Link'
        action=annot['/A'];assert action['/S']=='/URI'
        assert str(action['/URI']).startswith('https://')
        link_count+=1
    assert '/AA' not in page
assert link_count>=35,link_count
assert 'čytańnie' in texts[6] and 'cytańnie' not in texts[6]
assert 'page 24' in texts[21]
assert 'Noto Sans' in texts[33] and '0.5' in texts[33]
assert texts[1].count('I viecier, i sokał, i ja —')==2
assert 'vietru—vichury' in texts[28]
assert 'Voli, voli' not in '\n'.join(texts)
assert 'research/sources.md' not in '\n'.join(texts)
for r in [reader,printout]:
    root=r.trailer['/Root']
    assert '/OpenAction' not in root and '/AA' not in root
    assert not list(r.attachments)
    assert '/JavaScript' not in root.get('/Names',{})
for i,page in enumerate(printout.pages):
    assert abs(float(page.mediabox.width)-297/25.4*72)<.01
    assert abs(float(page.mediabox.height)-210/25.4*72)<.01
    text=page.extract_text()
    for original in texts[2*i:2*i+2]:
        assert re.sub(r'\s+','',original) in re.sub(r'\s+','',text)

class Links(HTMLParser):
    def __init__(self): super().__init__();self.links=[]
    def handle_starttag(self,tag,attrs):
        assert tag not in ['script','iframe','object','embed']
        for key,value in attrs:
            assert not key.startswith('on')
            if key in ['src','href']:self.links.append((tag,value))

manifest=json.loads((ROOT/'output/release-manifest.json').read_text())
public=manifest['public_files']
for filename in ['index.html','sources.html']:
    html=(ROOT/public[filename]).read_text();parser=Links();parser.feed(html)
    assert '0.5' in html
    assert 'educational and research purposes' in html
    assert '/Users/' not in html and '/home/' not in html
    for tag,url in parser.links:
        if urlsplit(url).scheme:
            assert tag=='a' and url.startswith('https://'),url
            assert ')' not in unquote(url).split(' ')[0] or '(' in unquote(url)
        else: assert url in public,(filename,url)
print(f'PASS: 34 B6 Slim pages, 17 A4 sheets, 6 art pages, {link_count} HTTPS reference links; Noto fonts embedded; active PDF content absent; website links resolve within allowlist.')
print('Fonts:',', '.join(sorted(fonts)))
