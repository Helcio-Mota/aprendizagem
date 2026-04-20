#!/usr/bin/env bash
set -e
TITLE=${1:-"Resposta do Assistente"}
TS=$(date +%Y%m%d-%H%M%S)
OUT_FILE="$PWD/assistant_response_${TS}.html"
cat > "$OUT_FILE" <<EOF
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>${TITLE} — $TS</title>
<style>body{font-family:Arial,Helvetica,sans-serif;line-height:1.4;padding:20px;color:#222}pre{background:#f6f8fa;padding:12px;border-radius:6px;overflow:auto}</style>
</head>
<body>
<h1>${TITLE}</h1>
<pre>
$(cat -)
</pre>
<p>Salvo em: ${OUT_FILE}</p>
</body>
</html>
EOF

echo "Saved $OUT_FILE"
