#!/usr/bin/env python3
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
import os
import textwrap

ROOT = os.path.dirname(__file__)
md_file = os.path.join(ROOT, 'roteiro-n8n.md')
out_pdf = os.path.join(ROOT, 'roteiro-n8n-utf8.pdf')

with open(md_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Simple markdown -> plain text: remove bold/italic/backticks
import re
text = re.sub(r'\*\*(.*?)\*\*', r"\1", text)
text = re.sub(r'\*(.*?)\*', r"\1", text)
text = re.sub(r'`{3}.*?`{3}', lambda m: m.group(0).replace('`',''), text, flags=re.S)
text = re.sub(r'`([^`]*)`', r"\1", text)

lines = []
for para in text.split('\n\n'):
    for line in para.split('\n'):
        if line.strip()=='':
            lines.append('')
        else:
            wrapped = textwrap.wrap(line, width=90)
            if not wrapped:
                lines.append('')
            else:
                lines.extend(wrapped)
    lines.append('')

# Register DejaVu Sans if available
font_paths = [
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
]
font_path = None
for p in font_paths:
    if os.path.exists(p):
        font_path = p
        break

c = canvas.Canvas(out_pdf, pagesize=A4)
width, height = A4
if font_path:
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))
    font_name = 'DejaVu'
else:
    font_name = 'Helvetica'

c.setFont(font_name, 12)
margin_left = 50
margin_top = height - 50
x = margin_left
y = margin_top
line_height = 14
for line in lines:
    if y < 50:
        c.showPage()
        c.setFont(font_name, 12)
        y = margin_top
    c.drawString(x, y, line)
    y -= line_height

c.save()
print('Wrote', out_pdf)
