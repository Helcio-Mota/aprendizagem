#!/usr/bin/env bash
set -e
cp "/home/aprimoraia/.openclaw/backups/openclaw-before-qwen2.5-3b-20260419-163813.json" "/home/aprimoraia/.openclaw/openclaw.json"
systemctl --user restart openclaw-gateway.service
echo 'Configuração anterior restaurada com sucesso.'
