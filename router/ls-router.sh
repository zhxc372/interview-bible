#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ "$#" -eq 0 ]; then
  echo '用法：./router/ls-router.sh "我要准备 MVCC 的面试知识卡"'
  exit 1
fi

python3 "$SCRIPT_DIR/router.py" "$@"
