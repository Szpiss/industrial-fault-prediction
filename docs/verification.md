# 第一阶段验收记录

验收日期：2026-11-03（Asia/Shanghai）。项目路径：`/Users/cuing/industrial-fault-prediction`。
结论：SQLite 本地开发的最小全栈链路已运行通过；Docker / MySQL 8.4 实际运行未验证。

## 已完成的模块

- FastAPI 入口、版本化路由、环境配置、基础日志、CORS、统一异常响应、OpenAPI / Swagger。
- SQLAlchemy 2 Base 与请求 session；SQLite / MySQL 配置切换；Alembic 空基线迁移。
- Vue 3 + TypeScript + Vite；Router、Pinia、Element Plus、Axios 与健康检查状态显示。
- 左侧导航、顶部栏、Dashboard、设备管理 / 数据分析 / 故障预测 / 告警占位页、404。
- ECharts 已安装且预留图表组件位置；ML 六个目录仅预留，没有安装或运行训练依赖。
- MySQL 8.4 Compose 文件、配置示例、依赖锁、启动/检查脚本、README 和 AGENTS.md。
- 独立 Git main 仓库已初始化；未推送，未更改全局 Git 配置。

## 实际执行与结果

| 检查 | 结果 | 证据 / 范围 |
| --- | --- | --- |
| 新建 Python 3.12 虚拟环境，按锁文件安装，再以 editable 安装后端 | 通过 | output/clean-python-install.log；全新环境下 11 项 pytest 通过 |
| ./scripts/bootstrap.sh | 通过 | output/bootstrap.log；保留现有 .env，迁移 SQLite，npm ci 成功 |
| pytest | 11 通过，无警告 | 健康检查、真实 SQLite SELECT 1、数据库故障 503、404、422、500、Swagger/OpenAPI、CORS、配置与迁移往返 |
| Ruff lint / format | 通过 | output/check.log，23 个 Python 文件格式检查通过 |
| pip check | 通过 | 未发现依赖冲突；全新环境也检查通过 |
| Vue / TypeScript 类型检查 | 通过 | vue-tsc 同时检查应用及 Vite 配置 |
| ESLint / Prettier | 通过 | ESLint 10，无警告；所有前端文件格式通过 |
| Vitest | 3 通过 | 成功响应、失败清除旧结果并重试恢复、抑制重复请求 |
| 前端生产构建 | 通过 | Vite 7.3.7，生成 dist；构建成功不代表生产部署已验收 |
| npm ci | 通过 | 通过 bootstrap 重建 node_modules，锁文件可用 |
| npm audit | 0 项 | output/npm-audit.json；仅代表本次审计时已知 npm 公告情况 |
| Alembic upgrade / current / check | 通过 | 开发 SQLite head 为 0001_baseline，无待生成 schema 差异 |
| Alembic 临时数据库 upgrade → downgrade → upgrade | 通过 | pytest，版本表状态正确；当前没有业务表 |
| MySQL 方言离线生成迁移 SQL | 通过 | 生成 alembic_version 建表及基线版本写入；没有连接 MySQL |
| Compose YAML 解析 | 通过 | 使用项目已有 Prettier YAML 解析器；没有运行 docker compose config |
| FastAPI 实际启动 | 通过 | Uvicorn 监听 127.0.0.1:8000；健康接口、/docs HTTP 200 |
| Vite 实际启动 | 通过 | 127.0.0.1:5173 返回 HTTP 200 |
| 浏览器 Axios → Vite 代理 → FastAPI → SQLite | 通过 | 浏览器健康请求 HTTP 200；Dashboard 显示“后端服务运行正常”和数据库“检查通过” |
| 四个业务页面导航与 404 返回 | 通过 | Playwright 操作真实页面，检查 URL、页面标题与占位文本 |
| 实际停止后端后重新检查 | 通过 | 显示“后端连接异常”及连接排查提示；原成功数据清空 |
| 重启后端后重新检查 | 通过 | 恢复“后端服务运行正常” |
| 桌面 1440×1000 与手机 390×844 | 通过 | 逐张查看截图，手机无横向溢出，导航展开与切换正常 |
| 直接刷新 /devices | 通过 | 浏览器刷新后仍展示设备管理占位页 |
| shell 语法与本地秘密忽略 | 通过 | bash -n；.env 权限 600；Git 忽略 .env、.venv、node_modules、数据库及 output |

本地截图位于（未进入 Git）：

- `output/playwright/dashboard-desktop.png`
- `output/playwright/dashboard-mobile.png`
- `output/playwright/backend-offline.png`
- `output/playwright/backend-recovered.png`

正常页面未观察到 Vue 运行时错误。首次 Vite 依赖预构建会刷新页面；停止后端的故障测试会产生预期的代理请求错误，均未作为业务成功结果处理。

## 已处理的问题

1. 本机代理导致 npm 超时：仅对本次依赖安装临时去除代理环境变量，复用官方 npm 缓存，不改全局网络配置。最终 npm ci 成功。
2. 当前 Starlette 的测试客户端优先使用 HTTPX2：开发依赖改用 httpx2，消除兼容弃用警告；全新环境 pytest 通过。
3. ESLint 9 已提示停止支持：改用兼容 Vue/TypeScript 插件的 ESLint 10，并验证 lint 与 build。
4. npm 审计发现 minimatch 10.2.6 的开发工具依赖问题：通过 overrides 固定 11.0.1，随后完整检查通过，npm audit 为 0。详见 [官方公告](https://github.com/advisories/GHSA-g3hv-75wg-m249)。未使用会降级主要工具的 audit fix --force。
5. 后端自动重载范围限定 app，避免安装虚拟环境包时触发无关重载。

## 未验证与限制

- **未验证：Docker / Compose 实际配置展开、MySQL 8.4 镜像拉取、容器健康检查、实际 MySQL 连接及迁移。** 本机没有 Docker CLI / Desktop，未执行系统级安装；MySQL 9.6 客户端存在，但 3306 没有服务监听。
- **未验证：生产部署、跨机器访问、完整业务、认证权限和机器学习效果。** 这些不属于第一阶段；当前只供本地开发。
- Python 锁文件在 macOS arm64 / Python 3.12 验证，其他 OS / Python 版本尚未验证。
- 验收后已停止临时前后端服务和验收浏览器，8000 / 5173 不再被本次任务占用。使用 README 的两个启动脚本即可重新打开。

## 下一阶段建议

先做设备台账闭环：最小字段与状态定义 → 设备 ORM 与迁移 → 仓储/服务 → 增删改查 API 及测试 → 前端设备列表、搜索、表单与空态。
完成后再决定数据导入契约和训练数据来源。不要在设备与数据基础尚未确认时直接开发 LSTM 或展示虚构预测指标。
