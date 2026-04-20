#!/usr/bin/env bash
set -e
cp "/home/aprimoraia/.openclaw/backups/rollback-3b-lento-20260419-171007/openclaw.json" "/home/aprimoraia/.openclaw/openclaw.json"
systemctl --user restart openclaw-gateway.service
echo 'Rollback do setup 3B lento concluído.'
