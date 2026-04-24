pdfize — gerar PDF UTF-8 a partir de texto

Local: `aprendizagem/n8n`

Scripts:
- `pdfize.py` — utilitário principal. Uso:

  ```bash
  # rodar com o venv criado anteriormente
  cd aprendizagem/n8n
  . .venv_reportlab/bin/activate
  python pdfize.py -i roteiro-n8n.md -o roteiro-n8n-utf8.pdf

  # ou via stdin
  echo "Olá — não é possível" | python pdfize.py -o saida.pdf
  ```

Notas:
- O script usa `reportlab` e tenta registrar `DejaVuSans.ttf` para renderizar acentos corretamente.
- Caso o venv `.venv_reportlab` não exista, crie-o com:

  ```bash
  python3 -m venv .venv_reportlab
  . .venv_reportlab/bin/activate
  pip install reportlab
  ```
