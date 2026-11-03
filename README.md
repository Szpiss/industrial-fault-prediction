# 工业设备故障预测系统

《基于Web与机器学习的工业设备故障预测系统的设计与实现》本科毕业设计工程。

当前交付为**第一阶段最小可运行框架**：前端请求后端健康接口，后端实际检查数据库；业务页面均为占位。
未实现设备 CRUD、用户认证、数据导入、模型训练、风险预测或告警。未接入真实工业设备。

## 技术栈

| 部分 | 技术 |
| --- | --- |
| 后端 | Python 3.12 推荐、FastAPI、Pydantic 2、SQLAlchemy 2.0、Alembic、Uvicorn |
| 数据库 | SQLite 默认；MySQL 8.4 LTS 可选，使用 PyMySQL 驱动 |
| 前端 | Vue 3、TypeScript、Vite 7、Vue Router 4、Pinia 3、Element Plus、Axios |
| 可视化 | ECharts 6 已安装，尚未绘制业务图表 |
| 质量工具 | pytest、Vitest、Ruff、ESLint 10、Prettier |
| 工程 | Git、Python venv、npm lockfile、Docker Compose（MySQL） |
| ML 规划 | scikit-learn、XGBoost、PyTorch；当前未安装、未训练 |

具体可复现依赖见 `backend/requirements-dev.lock` 和 `frontend/package-lock.json`。

开发工具依赖通过 npm overrides 固定 `minimatch=11.0.1`，对应 [GHSA-g3hv-75wg-m249](https://github.com/advisories/GHSA-g3hv-75wg-m249) 的修复版本；已通过 ESLint、类型检查、测试与构建验证。上游工具采用修复版本后可评估移除覆盖。

## 目录

```text
industrial-fault-prediction/
├── backend/
│   ├── app/
│   │   ├── api/v1/        # API 路由，当前仅 health
│   │   ├── core/          # 环境配置、日志、异常
│   │   ├── db/            # ORM Base、engine 与 session
│   │   ├── models/        # ORM 模型注册，当前无业务表
│   │   ├── schemas/       # Pydantic 响应结构
│   │   ├── services/      # 业务逻辑预留
│   │   ├── repositories/  # 数据访问预留
│   │   └── main.py
│   ├── alembic/           # 空基线迁移及版本目录
│   ├── data/              # 忽略的本地 SQLite 数据
│   ├── tests/
│   ├── pyproject.toml
│   └── requirements-dev.lock
├── frontend/src/
│   ├── api/               # Axios 与健康接口
│   ├── assets/            # 全局样式
│   ├── components/        # 通用占位组件、charts 扩展说明
│   ├── layouts/           # 侧栏、顶栏、页面区域
│   ├── router/            # 路由、懒加载、404
│   ├── stores/            # 健康状态与重试
│   ├── types/
│   ├── views/             # Dashboard 与四个业务占位页
│   └── App.vue
├── ml/                    # datasets / preprocessing / features /
│                          # models / training / evaluation
├── docs/                  # 架构、环境与验收记录
├── scripts/               # 初始化、启动、检查
├── docker-compose.yml     # 仅 MySQL 8.4 开发服务
├── .env.example           # 根目录唯一配置示例
└── AGENTS.md              # 后续协作规范与阶段约束
```

## 快速启动：SQLite，无需 Docker

前提：Python 3.12 与 Node 24 LTS + npm；Node 22 也须满足 package.json 的最低小版本。
已有合适版本即可，不需要升级全局软件。`.nvmrc` / `.node-version` 指定推荐主版本 24。

```bash
cd /path/to/industrial-fault-prediction
./scripts/bootstrap.sh
```

脚本只创建项目虚拟环境、复制尚不存在的 `.env`、安装锁定依赖、升级当前配置数据库到迁移 head。
默认寻找 `python3.12`；其他兼容解释器可通过 `PYTHON_BIN=/path/to/python ./scripts/bootstrap.sh` 指定。
当前电脑脚本可复用 Codex 随附的 Node 24，仅对子进程调整 PATH，不修改 shell 配置。
其他电脑请先用已有版本管理工具选择 Node 24；脚本不自动安装系统软件。

然后打开两个终端：

```bash
# 终端一，在项目根目录
./scripts/backend.sh

# 终端二，在项目根目录
./scripts/frontend.sh
```

- 前端：[http://127.0.0.1:5173](http://127.0.0.1:5173)
- 健康接口：[http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
- Swagger：[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI：[http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

Dashboard 自动显示“后端服务运行正常”。停止后端再点“重新检查”应显示错误；重新启动后再次检查可恢复。
两个终端使用 Ctrl+C 停止服务。服务仅绑定回环地址，供本机开发。

### 等价的手动安装和启动

```bash
cp .env.example .env  # 已存在时不要覆盖
python3.12 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements-dev.lock
backend/.venv/bin/python -m pip install --no-deps --no-build-isolation -e backend
cd backend
.venv/bin/alembic upgrade head
.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

另一个终端先选 Node 24，再进入 `frontend`：

```bash
npm ci
npm run dev
```

## 环境变量与连接方式

后端固定读取仓库根目录 `.env`，启动工作目录不会改变 SQLite 路径。
前端 Vite 同样读取根目录 `.env`；修改后应重启对应服务。

| 变量 | 用途 / 默认值 |
| --- | --- |
| APP_NAME / APP_ENV / LOG_LEVEL | 应用名、运行环境、日志等级 |
| CORS_ORIGINS | JSON 数组，仅允许列出的前端来源 |
| DATABASE_BACKEND | `sqlite` 默认，或 `mysql` |
| SQLITE_PATH | `backend/data/development.db`，相对项目根目录 |
| DATABASE_URL | 可选优先覆盖；只接受 sqlite 或 mysql+pymysql |
| MYSQL_HOST / MYSQL_PORT | 本机连接默认 `127.0.0.1:3307` |
| MYSQL_DATABASE / MYSQL_USER | MySQL 开发库名与普通应用账号 |
| MYSQL_PASSWORD / MYSQL_ROOT_PASSWORD | 自行设置；示例为空，真实值不提交 |
| VITE_API_BASE_URL | 默认 `/api/v1`，浏览器经 Vite 代理调用 |
| API_PROXY_TARGET | 默认 `http://127.0.0.1:8000`，仅 Vite 服务端读取 |

Vite 的开发与 preview 服务均代理 `/api`。构建后的静态文件自身不提供代理；未来部署需要反向代理或显式配置 API 地址与 CORS。
`VITE_` 变量会打入浏览器资源，禁止放密码。`.env`、数据库、日志和权重已被 Git 忽略。
可选 DATABASE_URL 示例格式：`mysql+pymysql://user:URL_ENCODED_PASSWORD@127.0.0.1:3307/database?charset=utf8mb4`。
推荐使用 MYSQL_* 字段，SQLAlchemy 自动正确处理密码中的特殊字符。

## MySQL 8.4 开发环境（可选）

当前验收机器没有 Docker，以下容器启动与 MySQL 实际连接**未验证**。系统已有 MySQL 9.6 客户端，无 3306 服务监听，不能作为 MySQL 8 的验证证据。

如需容器，在获得安装许可后按 [Docker 官方 Mac 安装说明](https://docs.docker.com/desktop/setup/install/mac-install/) 安装 Apple Silicon 版 Docker Desktop 并启动。
不需要覆盖系统 MySQL，也不需要全局安装 Python/MySQL 驱动。

1. 编辑根 `.env`，填写两个不同的本地随机密码。保持 `DATABASE_URL=` 为空。
2. 将 `DATABASE_BACKEND=sqlite` 改为 `DATABASE_BACKEND=mysql`。
3. 在根目录执行：

```bash
docker compose up -d mysql
docker compose ps
docker compose logs --tail=50 mysql
```

等待 mysql 显示 healthy，再运行迁移与后端：

```bash
cd backend
.venv/bin/alembic upgrade head
.venv/bin/alembic current
# 然后从根目录启动 ./scripts/backend.sh
```

容器端口映射为 `127.0.0.1:3307:3306`，避免和系统 3306 冲突。
root 密码只用于容器初始化；应用使用 MYSQL_USER 普通账号。Compose 的健康检查使用该账号实际执行 SELECT 1。
MySQL 8.4 镜像使用本机架构，不强制 amd64 模拟。

```bash
docker compose stop mysql   # 暂停并保留数据
# docker compose down       # 移除容器/网络，命名数据卷仍保留
```

不要随意使用 `down -v`，它会删除开发数据库。已有数据卷的初始化密码不会随 `.env` 自动改变，应使用 SQL 修改账号密码。
切回 SQLite 时设置 `DATABASE_BACKEND=sqlite`、清空 DATABASE_URL，重启后端，并对 SQLite 再执行迁移。

## 数据库迁移

```bash
cd backend
.venv/bin/alembic upgrade head
.venv/bin/alembic current
.venv/bin/alembic check
# 新模型添加后，在 app/models/__init__.py 导入，生成并人工审查迁移
.venv/bin/alembic revision --autogenerate -m "describe schema change"
# 仅在可丢弃开发数据库谨慎回退
.venv/bin/alembic downgrade -1
```

当前 head 为 `0001_baseline`，仅建立迁移链和 Alembic 版本表，没有任何业务表；不在启动时调用 create_all。
健康接口执行 SELECT 1，表示 API 和数据库可用，不表示所有未来业务迁移已就绪。

## 自动化检查

```bash
# 项目根目录，一次执行全部检查
./scripts/check.sh

# 也可分别执行
cd backend
.venv/bin/pytest -q
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/python -m pip check
```

前端（先选择 Node 24）：

```bash
cd frontend
npm run typecheck
npm run lint
npm run format:check
npm test
npm run build
npm run preview   # 可选：构建后在 4173 预览，API 仍要求后端运行
```

后端测试使用内存/临时 SQLite，不写入开发数据库，包含数据库失败、异常格式、CORS、文档与迁移往返。
前端 Vitest 检查成功、失败后的旧状态清理、重试恢复和重复请求抑制。
真实浏览器验收记录见 [docs/verification.md](docs/verification.md)。

格式化：`backend/.venv/bin/ruff format backend`；前端 `npm run format`。
更新 Python 依赖时在 backend 运行：

```bash
.venv/bin/pip-compile --extra dev --strip-extras --allow-unsafe --no-emit-index-url --no-emit-trusted-host --output-file requirements-dev.lock pyproject.toml
```

依赖锁在 Python 3.12/macOS arm64 验证；其他平台首次运行应执行完整检查，缺少匹配 wheel 时检查 Python 版本，勿直接取消版本约束。

## 常见问题

- **前端提示连接失败**：先访问 8000 健康接口，再检查根 .env 的 API_PROXY_TARGET。Vite 日志 ECONNREFUSED 通常表示后端未启动。
- **返回 503**：API 可访问但数据库不可用，检查数据库服务、端口、用户密码和 DATABASE_BACKEND；不会把连接密码返回浏览器。
- **跨域失败**：默认使用 Vite 同源代理；若直接访问后端，CORS_ORIGINS 要精确包含实际协议、域名、端口，且为 JSON 数组。
- **端口占用**：先确认占用者，不结束未知进程。后端脚本可加 `--port 8001`，同时修改 API_PROXY_TARGET；改前端端口时更新 CORS。
- **SQLite 目录或迁移问题**：默认 data 目录由 engine 创建，执行 alembic upgrade head；不要提交本地 .db 文件。
- **Node 版本不兼容**：优先 Node 24 LTS；本机 ./scripts/frontend.sh 会复用已有随附 Node，不要求修改全局 Node 25。
- **pip 系统环境限制**：所有 pip 操作使用 backend/.venv/bin/python，避免 PEP 668 和全局包冲突。
- **Docker 命令不存在**：直接走 SQLite 流程；Docker 的缺失不影响本阶段主要链路。
- **MySQL 密码报错**：新容器首次运行要设置两个密码；已有卷需核对原密码，不要通过删除卷排错。
- **代理/下载超时**：检查本机网络与 npm/pip 已有代理配置后重试，不把认证代理地址写进 Git。
- **刷新业务路径 404**：Vite 开发服务已支持 history fallback，未来静态托管应配置 fallback 到 index.html。

## 下一阶段

建议先实现设备台账：确定最小字段、设备状态枚举和唯一编号 → ORM + 可回退迁移 → repository/service → CRUD API 与测试 → 设备列表和表单。
随后再做 CSV 导入与数据质量校验，基于有来源的数据训练 Logistic Regression / SVM / XGBoost，最后接入风险评分、可视化、告警和权限。
LSTM 应在时序采样与基线评估稳定后决定，不在工程初始化阶段安装。

详细设计见 [docs/architecture.md](docs/architecture.md)，机器环境见 [docs/environment.md](docs/environment.md)，后续约束见 [AGENTS.md](AGENTS.md)。
