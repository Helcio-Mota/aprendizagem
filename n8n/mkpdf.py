#!/usr/bin/env python3
import os
import textwrap

in_md = 'roteiro-n8n.md'
out_pdf = 'roteiro-n8n.pdf'

with open(in_md, 'r', encoding='utf-8') as f:
    text = f.read()

# Simplify markdown to plain text
text = text.replace('\r\n', '\n')
# Remove markdown formatting for basic PDF
import re
text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
text = re.sub(r'\*(.*?)\*', r'\1', text)
text = re.sub(r'`{3}.*?`{3}', lambda m: m.group(0).replace('\n', '\n'), text, flags=re.S)
text = re.sub(r'`([^`]*)`', r'\1', text)

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

# Escape parentheses and backslashes for PDF string literals
def esc(s):
    return s.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')

content_lines = []
content_lines.append('BT')
content_lines.append('/F1 12 Tf')
# Starting position
x = 50
y = 820
content_lines.append(f'{x} {y} Td')
line_height = 14
first = True
for line in lines:
    s = esc(line)
    # show text and move down
    content_lines.append(f'({s}) Tj')
    content_lines.append(f'0 -{line_height} Td')

content_lines.append('ET')

content = '\n'.join(content_lines) + '\n'

# Build PDF objects
objs = []
# 1: Catalog
objs.append(('1 0 obj', b'<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'))
# 2: Pages
objs.append(('2 0 obj', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n'))
# 4: Font
objs.append(('4 0 obj', b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n'))
# 5: Contents (stream)
stream = content.encode('utf-8')
stream_obj = b'<< /Length %d >>\nstream\n' % len(stream) + stream + b'endstream\nendobj\n'
# page object refers to font 4 and contents 5
page_obj = ('3 0 obj', ('<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n').encode('utf-8'))
# assemble objects in order 1,2,3,4,5
objects = [ ('1 0 obj', b'<< /Type /Catalog /Pages 2 0 R >>\nendobj\n'),
            ('2 0 obj', b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n'),
            ('3 0 obj', b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>\nendobj\n'),
            ('4 0 obj', b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n'),
            ('5 0 obj', stream_obj)
          ]

pdf = bytearray()
pdf.extend(b'%PDF-1.4\n%\xe2\xe3\xcf\xd3\n')
positions = []
for obj_id, obj_bytes in objects:
    positions.append(len(pdf))
    pdf.extend(obj_id.encode('utf-8') + b'\n')
    pdf.extend(obj_bytes)

# xref
xref_pos = len(pdf)
pdf.extend(b'xref\n')
pdf.extend(f'0 {len(objects)+1}\n'.encode('utf-8'))
pdf.extend(b'0000000000 65535 f \n')
for pos in positions:
    pdf.extend(f'{pos:010d} 00000 n \n'.encode('utf-8'))

# trailer
pdf.extend(b'trailer\n')
pdf.extend(b'<<\n')
pdf.extend(f'/Size {len(objects)+1}\n'.encode('utf-8'))
pdf.extend(b'/Root 1 0 R\n')
pdf.extend(b'>>\n')
pdf.extend(b'startxref\n')
pdf.extend(f'{xref_pos}\n'.encode('utf-8'))
pdf.extend(b'%%EOF\n')

with open(out_pdf, 'wb') as f:
    f.write(pdf)

print('Wrote', out_pdf)
