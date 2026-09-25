"""Generate an accessible, script-free HTML reading edition from the book source."""
from html import escape
import json

def build_reader(root):
    data=json.loads((root/'content/book.json').read_text())
    art_before={4:0,8:1,14:2,18:3,23:4,27:5}
    descriptions=['A stork walking through a meadow','A stork in flight','A stork bringing a twig to its nest','Two storks together in their nest','A stork with its chicks','A family of storks flying together']
    pages=[('Cover','<img class="cover" src="cover.png" alt="Watercolor stork in a nest below the letter Ŭ">')]
    def p(text):return '<p>'+escape(text).replace('\n','<br>')+'</p>'
    for old,page in enumerate(data,2):
        if old in art_before:
            scene=art_before[old]
            pages.append((descriptions[scene],'<div class="art" role="img" aria-label="'+descriptions[scene]+'" style="background-position:'+str((scene%3)*50)+'% '+str((scene//3)*100)+'%"></div>'))
        body='<p class="kicker">'+escape(page['kicker'])+'</p><h2>'+escape(page['title'])+'</h2>'
        if 'poem' in page:body+='<div class="poem" lang="be-Latn">'+''.join(p(s) for s in page['poem'])+'</div>'+p(page['poem_note'])
        if 'rows' in page:
            body+='<div class="tablewrap"><table><thead><tr>'+''.join('<th scope="col">'+escape(c)+'</th>' for c in page['rows'][0])+'</tr></thead><tbody>'
            body+=''.join('<tr>'+''.join('<td>'+escape(c)+'</td>' for c in row)+'</tr>' for row in page['rows'][1:])+'</tbody></table></div>'
        body+=''.join(p(t) for t in page.get('paragraphs',[]))
        if 'callout' in page:body+='<div class="callout">'+p(page['callout'])+'</div>'
        pages.append((page['title'],body))
    assert len(pages)==34
    toc='<details id="contents"><summary>Contents · 34 pages</summary><ol>'+''.join('<li><a href="#page-'+str(i)+'">'+escape(t)+'</a></li>' for i,(t,_) in enumerate(pages,1))+'</ol></details>'
    sections=[]
    for i,(title,body) in enumerate(pages,1):
        nav=('<a href="#page-'+str(i-1)+'">← Previous</a>' if i>1 else '<span></span>')+'<a href="#contents">'+str(i)+' / 34 · Contents</a>'+('<a href="#page-'+str(i+1)+'">Next →</a>' if i<34 else '<a href="index.html">Home</a>')
        sections.append('<section class="page" id="page-'+str(i)+'" aria-label="Page '+str(i)+': '+escape(title,quote=True)+'">'+body+'<nav class="pagination" aria-label="Page '+str(i)+' navigation">'+nav+'</nav></section>')
    html='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Read online | Belarusian Lacinka</title><meta name="description" content="Read all 34 pages of Belarusian Lacinka online: alphabet, history, poetry and watercolor storks.">
<style>
*{box-sizing:border-box}body{margin:0;background:#e9e3d7;color:#28231f;font:18px/1.65 Georgia,serif}a{color:#4c603e;text-underline-offset:4px}a:focus-visible,summary:focus-visible{outline:3px solid #5a6c4d;outline-offset:4px}header{background:#f8f2e5;padding:16px 24px;border-bottom:1px solid #c9bda7}header nav{max-width:680px;margin:auto;display:flex;gap:20px;flex-wrap:wrap}main{max-width:720px;margin:32px auto;padding:0 16px}.page{background:#f8f2e5;margin:28px 0;padding:42px;box-shadow:0 4px 20px #28231f12;scroll-margin-top:16px}h1,h2{color:#5a6c4d;line-height:1.2;font-weight:normal}h2{font-size:32px;border-bottom:1px solid #c9bda7;padding-bottom:18px}.kicker{font:12px/1.5 system-ui,sans-serif;text-transform:uppercase;letter-spacing:.08em;color:#5a6c4d}.cover{display:block;width:100%;height:auto}.art{width:100%;aspect-ratio:1;background-image:url(stork-scenes.png);background-size:300% 200%;margin:50px 0}.poem{font-size:19px}.poem p{margin:0 0 20px}.callout{color:#5a6c4d;font-style:italic}.pagination{border-top:1px solid #c9bda7;margin-top:34px;padding-top:18px;display:flex;justify-content:space-between;gap:12px;font:13px/1.6 system-ui,sans-serif}.tablewrap{overflow-x:auto}table{width:100%;border-collapse:collapse;font:15px/1.6 system-ui,sans-serif}th,td{padding:8px;border-bottom:1px solid #c9bda7;text-align:left}th{background:#eeeade}details{background:#f8f2e5;padding:20px}summary{cursor:pointer}footer{font:14px/1.7 system-ui,sans-serif;padding:20px 4px}footer p{max-width:650px}@media(max-width:520px){body{font-size:17px}.page{padding:24px 20px}h2{font-size:27px}.poem{font-size:16px}.pagination{font-size:12px}main{padding:0 10px}}@media print{header,details,.pagination,footer{display:none}.page{break-after:page;box-shadow:none;margin:0}body{background:white}}
</style></head><body><header><nav aria-label="Book navigation"><a href="index.html">Belarusian Lacinka</a><a href="#contents">Contents</a><a href="belarusian-lacinka-b6-slim.pdf" download>Download PDF</a><a href="belarusian-lacinka-b6-slim-on-a4.pdf" download>Print on A4</a></nav></header><main><h1>A small book with room for flight</h1><p>English explanations · Belarusian examples · Edition 0.5</p>'''+toc+''.join(sections)+'''<footer><p>The information provided is intended solely for educational and research purposes. It is not an official language standard.</p><p><a href="sources.html">Sources and editorial notes</a> · <a href="rights.txt">Rights and font notices</a></p><p>Numbered references correspond to the bibliography. The PDF also includes direct source links. Illustrations are AI-generated.</p></footer></main></body></html>'''
    (root/'publishing/read.html').write_text(html)
