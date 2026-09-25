"""Build a 105 x 175 mm reader and a two-up A4 cutting file."""
from pathlib import Path
import json
from io import BytesIO
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from pypdf import PdfReader, PdfWriter, Transformation

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'output/pdf'
OUT.mkdir(parents=True, exist_ok=True)
FONT = Path('/System/Library/Fonts/Supplemental')
for name, file in [('Body','Arial.ttf'),('Bold','Arial Bold.ttf'),('Italic','Arial Italic.ttf'),('Display','Georgia.ttf')]:
    pdfmetrics.registerFont(TTFont(name, str(FONT / file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Italic',boldItalic='Bold')
W,H = 105*mm,175*mm
INK,SAGE,MUTED,LINE = map(HexColor,['#28231f','#5a6c4d','#766e61','#c9bda7'])
body = ParagraphStyle('body',fontName='Body',fontSize=8.4,leading=11.6,textColor=INK)
small = ParagraphStyle('small',parent=body,fontSize=7.1,leading=9)
title = ParagraphStyle('title',fontName='Display',fontSize=18,leading=21,textColor=SAGE)
source = ROOT/'content/book.json'
data = json.loads(source.read_text())
assert len(data) == 27, len(data)
# Verify every source glyph before authoring: no silent empty squares.
for ch in set(source.read_text()):
    if not ch.isspace() and ord(ch)>127:
        assert ord(ch) in pdfmetrics.getFont('Body').face.charToGlyph, repr(ch)
c = canvas.Canvas(str(OUT/'belarusian-lacinka-b6-slim.pdf'),pagesize=(W,H),invariant=1)
c.setTitle('Belarusian Lacinka | MD B6 Slim')
c.setAuthor('Belarusian Lacinka')
c.drawImage(str(ROOT/'assets/cover.png'),0,0,width=W,height=H)
c.showPage()

def p(text,y,style=body,x=9*mm,width=87*mm,floor=49*mm,gap=3.1*mm):
    obj=Paragraph(escape(text).replace('\n','<br/>'),style)
    _,height=obj.wrap(width,H)
    if y-height<floor:
        raise ValueError(f'Overflow on page {c.getPageNumber()}: {text[:50]}')
    obj.drawOn(c,x,y-height)
    return y-height-gap

for number,page in enumerate(data,2):
    c.setFillColor(HexColor('#f8f2e5')); c.rect(0,0,W,H,fill=1,stroke=0)
    scene=page.get('scene',min(5,(number-2)//4))
    # Clip a single vignette from the original six-scene watercolor sheet.
    size=(22 if 'poem' in page else 32)*mm
    left=74*mm if 'poem' in page else (W-size)/2
    bottom=15*mm
    c.saveState()
    clip=c.beginPath();clip.rect(left,bottom,size,size);c.clipPath(clip,stroke=0)
    c.drawImage(str(ROOT/'assets/stork-scenes.png'),left-(scene%3)*size,bottom-(1-scene//3)*size,width=3*size,height=2*size)
    c.restoreState()
    c.setFillColor(SAGE);c.setFont('Body',6.6)
    c.drawString(9*mm,H-11*mm,page['kicker'].upper())
    y=p(page['title'],H-17*mm,title)
    c.setStrokeColor(LINE); c.line(9*mm,y+mm,96*mm,y+mm)
    y-=3*mm
    if 'poem' in page:
        verse=ParagraphStyle('verse',parent=body,fontName='Display',fontSize=9,leading=10.8)
        for stanza in page['poem']:
            y=p(stanza,y,verse,floor=30*mm,gap=2*mm)
        p(page['poem_note'],y-2*mm,ParagraphStyle('note',parent=small,fontSize=6,leading=7.7),width=62*mm,floor=15*mm)
    if 'rows' in page:
        rows=[[Paragraph(escape(cell),small) for cell in row] for row in page['rows']]
        table=Table(rows,colWidths=[87*mm/len(rows[0])]*len(rows[0]))
        table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#eeeade')),('LINEBELOW',(0,0),(-1,-1),.35,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
        _,th=table.wrap(87*mm,H)
        table.drawOn(c,9*mm,y-th); y-=th+4*mm
    for paragraph in page.get('paragraphs',[]): y=p(paragraph,y,small if number>=27 else body)
    if 'callout' in page:
        y-=mm
        y=p(page['callout'],y,ParagraphStyle('callout',parent=body,fontName='Italic',textColor=SAGE))
    for line in range(page.get('lines',0)):
        if y<51*mm: break
        c.setStrokeColor(LINE);c.setLineWidth(.35);c.line(9*mm,y,96*mm,y);y-=7*mm
    c.setStrokeColor(LINE);c.line(9*mm,12*mm,96*mm,12*mm)
    c.setFillColor(MUTED);c.setFont('Body',6)
    c.drawString(9*mm,8*mm,'BELARUSIAN LACINKA')
    c.drawRightString(96*mm,8*mm,str(number))
    c.showPage()
c.save()

# Exact B6 Slim, no scaling: two pages on landscape A4, with cutting marks.
r=PdfReader(OUT/'belarusian-lacinka-b6-slim.pdf');out=PdfWriter()
aw,ah=297*mm,210*mm
xs=[(297-210-6)/2*mm,(297-210-6)/2*mm+111*mm]
y=(ah-H)/2
for start in range(0,len(r.pages),2):
    sheet=out.add_blank_page(aw,ah)
    for x,page in zip(xs,r.pages[start:start+2]):
        sheet.merge_transformed_page(page,Transformation().translate(x,y))
    buffer=BytesIO();marks=canvas.Canvas(buffer,pagesize=(aw,ah))
    marks.setLineWidth(.35);marks.setStrokeColor(MUTED)
    for x in xs:
        for cx in [x,x+W]:
            for cy in [y,y+H]:
                dx=-1 if cx==x else 1;dy=-1 if cy==y else 1
                marks.line(cx+dx*mm,cy,cx+dx*3*mm,cy)
                marks.line(cx,cy+dy*mm,cx,cy+dy*3*mm)
    marks.setFont('Body',6);marks.drawCentredString(aw/2,6*mm,f'B6 Slim 105 x 175 mm | 100% | {start+1}-{min(start+2,len(r.pages))} | one-sided')
    marks.save();buffer.seek(0);sheet.merge_page(PdfReader(buffer).pages[0])
out.add_metadata({'/Title':'Belarusian Lacinka - B6 Slim, 2-up A4','/Author':'Belarusian Lacinka'})
out.write(OUT/'belarusian-lacinka-b6-slim-on-a4.pdf')
assert len(r.pages)==28
for f in sorted(OUT.glob('*.pdf')): print(f)
