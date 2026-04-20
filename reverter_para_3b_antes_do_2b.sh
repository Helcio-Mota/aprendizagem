#!/usr/bin/env bash
set -e
cp "/home/aprimoraia/.openclaw/backups/pre-2b-quant-20260419-223534/openclaw.json" "/home/aprimoraia/.openclaw/openclaw.json"
systemctl --user restart openclaw-gateway.service
echo 'Rollback para o estado anterior ao 2B concluído.'
