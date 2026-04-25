#!/usr/bin/env bash
set -euo pipefail

MYSQL_HOME="/opt/homebrew/opt/mysql@8.4"
PORT="3307"

"$MYSQL_HOME/bin/mysqladmin" -h 127.0.0.1 -P "$PORT" -u root -p123456 shutdown
echo "项目 MySQL 已停止"

