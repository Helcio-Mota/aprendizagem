#!/usr/bin/env python3
import sys, json, os, datetime
cfg_path = os.path.join(os.path.dirname(__file__), 'autosave_config.json')
try:
    cfg = json.load(open(cfg_path))
except Exception:
    cfg = {"enabled": True, "threshold_lines": 15, "output_dir": "TEMP"}
text = sys.stdin.read()
lines = text.count('\n') + (1 if text and not text.endswith('\n') else 0)
if not cfg.get('enabled', True):
    print('autosave disabled', file=sys.stderr)
    sys.exit(0)
if lines < cfg.get('threshold_lines', 15):
    print(f'skipping save: {lines} lines < threshold', file=sys.stderr)
    sys.exit(0)
outdir = os.path.join(os.path.dirname(__file__), cfg.get('output_dir', 'TEMP'))
if not os.path.isabs(outdir):
    outdir = os.path.join(os.path.dirname(__file__), cfg.get('output_dir', 'TEMP'))
os.makedirs(outdir, exist_ok=True)
ts = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
fname = f'assistant_response_{ts}.html'
path = os.path.join(outdir, fname)
html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Resposta do Assistente — {ts}</title>
<style>body{{font-family:Arial,Helvetica,sans-serif;line-height:1.4;padding:20px;color:#222}}pre{{background:#f6f8fa;padding:12px;border-radius:6px;overflow:auto;white-space:pre-wrap}}</style>
</head>
<body>
<h1>Resposta do Assistente — {ts}</h1>
<pre>{text}</pre>
</body>
</html>'''
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('saved', path);
import subprocess;
try:
    subprocess.run([str(Path(__file__).parent / 'convert_htmls_to_pdf.sh',), Path(path).name], check=True)
except Exception:
    pass
