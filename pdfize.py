#!/usr/bin/env python3
"""
pdfize.py — Generate UTF-8 PDF from stdin or a text/markdown file.
Usage:
  # From a file
  ./pdfize.py -i input.md -o output.pdf

  # From stdin
  echo "Hello — texto com acentos: Não é possível" | ./pdfize.py -o output.pdf

This script prefers to be run with the virtualenv at .venv_reportlab (created earlier):
  . .venv_reportlab/bin/activate && python pdfize.py -i roteiro-n8n.md

It uses DejaVu Sans if available to render UTF-8 correctly.
"""
import argparse
import os
import sys
import textwrap

try:
    from reportlab.pdfgen import canvas
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.pagesizes import A4
except Exception:
    sys.exit('reportlab not available. Run with .venv_reportlab/bin/python or install reportlab.')


def load_text(path):
    if path:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return sys.stdin.read()


def markdown_to_plain(text):
    import re
    text = text.replace('\r\n', '\n')
    text = re.sub(r'\*\*(.*?)\*\*', r"\1", text)
    text = re.sub(r'\*(.*?)\*', r"\1", text)
    text = re.sub(r'`{3}.*?`{3}', lambda m: m.group(0).replace('`',''), text, flags=re.S)
    text = re.sub(r'`([^`]*)`', r"\1", text)
    return text


def find_dejavu():
    candidates = [
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/local/share/fonts/DejaVuSans.ttf',
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def make_pdf(text, out_path):
    lines = []
    for para in text.split('\n\n'):
        for line in para.split('\n'):
            if line.strip() == '':
                lines.append('')
            else:
                wrapped = textwrap.wrap(line, width=90)
                if not wrapped:
                    lines.append('')
                else:
                    lines.extend(wrapped)
        lines.append('')

    font_path = find_dejavu()
    c = canvas.Canvas(out_path, pagesize=A4)
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


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-i', '--input', help='input text/markdown file (default: stdin)')
    p.add_argument('-o', '--output', help='output PDF path', required=True)
    args = p.parse_args()

    text = load_text(args.input)
    text = markdown_to_plain(text)
    make_pdf(text, args.output)
    print('Wrote', args.output)


if __name__ == '__main__':
    main()
