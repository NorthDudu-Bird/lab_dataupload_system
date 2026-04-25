#!/usr/bin/env bash
set -euo pipefail

MYSQL_HOME="/opt/homebrew/opt/mysql@8.4"
DATA_DIR="/opt/homebrew/var/mysql-lab-report"
SOCKET_FILE="/tmp/lab_report_mysql8.sock"
PID_FILE="/tmp/lab_report_mysql8.pid"
PORT="3307"

if [ ! -x "$MYSQL_HOME/bin/mysqld" ]; then
  echo "未找到 MySQL 8.4，请先执行：brew install mysql@8.4"
  exit 1
fi

if [ ! -d "$DATA_DIR/mysql" ]; then
  mkdir -p "$DATA_DIR"
  "$MYSQL_HOME/bin/mysqld" --initialize-insecure --datadir="$DATA_DIR" --user="$(whoami)"
fi

if "$MYSQL_HOME/bin/mysqladmin" -h 127.0.0.1 -P "$PORT" -u root -p123456 ping >/dev/null 2>&1; then
  echo "项目 MySQL 已在 127.0.0.1:$PORT 运行"
  exit 0
fi

echo "启动项目 MySQL 8.4：127.0.0.1:$PORT"
exec "$MYSQL_HOME/bin/mysqld" \
  --datadir="$DATA_DIR" \
  --port="$PORT" \
  --socket="$SOCKET_FILE" \
  --pid-file="$PID_FILE" \
  --bind-address=127.0.0.1 \
  --mysqlx=0

