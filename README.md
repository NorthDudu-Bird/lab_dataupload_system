# 实验室数据上报系统

实验室数据上报系统是一个前后端分离的信息系统设计实验课项目，覆盖用户管理、实验室管理、设备管理、数据上报、审核、公告与统计分析。系统内置 `admin`、`reviewer`、`reporter` 三类角色，支持 JWT 登录鉴权与基础权限控制。

## 技术栈

- 后端：Python 3.11、Flask、Flask-JWT-Extended、Flask-SQLAlchemy、Flask-CORS、PyMySQL、Marshmallow、Werkzeug 密码哈希
- 数据库：MySQL 8.x，字符集 `utf8mb4`
- 前端：Vue 3、Vite、Vue Router、Pinia、Axios、Element Plus、ECharts

## 项目结构

```text
.
├── backend
│   ├── app
│   │   ├── common
│   │   ├── decorators
│   │   ├── models
│   │   ├── routes
│   │   ├── schemas
│   │   ├── services
│   │   └── utils
│   ├── sql
│   │   └── lab_report_system.sql
│   ├── uploads
│   ├── .env.example
│   ├── requirements.txt
│   └── run.py
├── frontend
│   ├── src
│   │   ├── api
│   │   ├── components
│   │   ├── layout
│   │   ├── router
│   │   ├── stores
│   │   ├── utils
│   │   └── views
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 功能模块

- 登录与权限：JWT 登录、退出、路由守卫、角色菜单、禁用账号拦截。
- 用户管理：admin 可新增、编辑、删除、启用禁用、重置密码。
- 实验室管理：admin 可维护，reviewer 可查看。
- 设备管理：admin 可维护，reviewer 可查看，支持按实验室筛选。
- 数据上报：reporter/admin 可新增；reporter 只能修改或删除本人待审核记录；已审核记录禁止修改。
- 审核管理：admin/reviewer 可审核待审核记录，支持通过、驳回与审核意见。
- 公告管理：admin 可发布、编辑、删除；普通用户可查看已发布公告。
- 首页统计：上报总数、待审核、已通过、已驳回、异常上报、实验室统计、日期趋势、设备状态分布。

## 环境要求

- Python 3.11
- MySQL 8.x
- Node.js 18+ 与 npm 9+

当前项目代码统一使用 UTF-8。数据库导入时建议确认客户端字符集为 `utf8mb4`。

## 数据库导入

1. 启动 MySQL。
2. 在项目根目录执行：

```bash
/opt/homebrew/opt/mysql@8.4/bin/mysql -h 127.0.0.1 -P 3307 -uroot -p123456 < backend/sql/lab_report_system.sql
```

脚本会创建数据库 `lab_report_system`，并插入初始化用户、实验室、设备、上报记录和公告数据。

本机已配置项目专用 MySQL 8.4：

- 数据目录：`/opt/homebrew/var/mysql-lab-report`
- 端口：`3307`
- root 密码：`123456`
- 不覆盖原有 MariaDB 数据目录 `/opt/homebrew/var/mysql`

## 后端启动

1. 进入后端目录：

```bash
cd backend
```

2. 创建并启用 Python 3.11 虚拟环境：

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

4. 创建本地环境变量文件：

```bash
cp .env.example .env
```

按本机 MySQL 配置修改 `.env` 中的 `DB_USER`、`DB_PASSWORD`、`DB_HOST`、`DB_PORT`。

5. 启动服务：

```bash
python run.py
```

后端默认访问地址：`http://127.0.0.1:5001`

macOS 上 `5000` 端口常被系统 AirPlay/ControlCenter 占用，因此本项目默认使用 `5001`。

本机已经额外提供脚本，便于演示时启动服务：

```bash
./scripts/start_mysql8.sh
./scripts/start_backend.sh
./scripts/start_frontend.sh
```

如果需要停止项目专用 MySQL：

```bash
./scripts/stop_mysql8.sh
```

## 前端启动

1. 进入前端目录：

```bash
cd frontend
```

2. 安装依赖：

```bash
npm install
```

3. 启动开发服务：

```bash
npm run dev
```

前端默认访问地址：`http://127.0.0.1:5173`

## 默认账号

| 角色 | 用户名 | 密码 |
| --- | --- | --- |
| 系统管理员 | admin | admin123 |
| 审核员 | reviewer | 123456 |
| 上报员 | reporter1 | 123456 |
| 上报员 | reporter2 | 123456 |

数据库中的密码已使用 Werkzeug 兼容格式加密保存。

## 接口简要说明

统一返回格式：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

主要接口：

- `POST /api/auth/login` 登录
- `GET /api/auth/profile` 当前用户信息
- `GET/POST/PUT/DELETE /api/users` 用户管理
- `PATCH /api/users/{id}/status` 启用或禁用用户
- `PATCH /api/users/{id}/password/reset` 重置密码
- `GET/POST/PUT/DELETE /api/labs` 实验室管理
- `GET/POST/PUT/DELETE /api/equipments` 设备管理
- `GET/POST/PUT/DELETE /api/reports` 上报记录
- `POST /api/reports/upload` 附件上传
- `GET /api/reviews` 审核列表
- `POST /api/reviews/{id}/audit` 审核通过或驳回
- `GET/POST/PUT/DELETE /api/notices` 公告管理
- `GET /api/dashboard` 首页统计

需要登录的接口请在请求头携带：

```text
Authorization: Bearer <token>
```

## 常见问题排查

- 登录提示数据库连接失败：检查 `.env` 中 MySQL 用户名、密码、端口和数据库名。
- 中文乱码：确认 MySQL 数据库、表和连接字符串均使用 `utf8mb4`。
- 前端请求 404：确认 Vite 代理已启动，后端运行在 `127.0.0.1:5001`。
- 前端登录后立即跳回登录页：检查后端 `JWT_SECRET_KEY` 是否稳定，浏览器本地存储是否被清理。
- 删除实验室或用户失败：该数据可能已被设备或上报记录引用，建议改为禁用或先处理关联数据。
- 附件无法访问：确认 `backend/uploads/` 目录存在，并且后端服务仍在运行。

## 交付前主流程

1. 使用 `reporter1 / 123456` 登录，新增一条上报记录。
2. 在上报列表编辑该待审核记录。
3. 使用 `reviewer / 123456` 登录，在审核管理中通过或驳回该记录。
4. 再次使用 reporter 登录，确认已审核记录不可编辑。
5. 使用 admin 或 reviewer 查看首页统计，确认数量和图表已更新。
