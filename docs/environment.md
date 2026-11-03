# 开发环境检查

检查日期：2026-11-03（Asia/Shanghai）。未修改全局 Python、Node、Git 或系统服务。

| 项目 | 本机发现 | 本次选择 / 状态 |
| --- | --- | --- |
| 系统 | macOS 26.4，Darwin 25.4.0 | Apple Silicon arm64 |
| Python | 3.14.6 / 3.12.13，Homebrew | 使用 `/opt/homebrew/bin/python3.12` 创建 backend/.venv |
| Node | 全局 25.8.1 | 复用已有随附 24.22.1 LTS，项目脚本临时调整 PATH |
| npm | 11.11.0 | npm install / ci；提交 package-lock.json |
| pnpm | 已存在随附可执行文件 | 本项目统一 npm，不混用锁文件 |
| uv / yarn | 未找到 | 非必需，不安装 |
| Git | 2.53.0 | 新建独立 main 仓库，未修改全局配置、未推送 |
| Docker / Compose | CLI 不存在，未发现 Docker Desktop / OrbStack | 未安装，容器运行未验证 |
| MySQL | Homebrew 9.6.0 客户端，3306 无监听 | 未启动或修改系统数据库；8.4 容器连接未验证 |
| SQLite | Python 内置支持 | 本阶段使用，可实际迁移与连接 |

Node 24 路径：`/Users/cuing/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node`。
项目脚本优先使用当前已选的 Node 22/24，再尝试该已有路径。此路径是本机便利配置，其他电脑使用普通 Node 24 + npm 即可。

缺少 Docker 时推荐先使用 SQLite。需要 MySQL 后，再按 Docker 官方文档安装 Apple Silicon 版 Docker Desktop、启动后验证 docker version / docker compose version。
这属于系统软件安装，应由用户确认后进行；本次没有进行权限修改或后台服务安装。

新开发者如无 Python，可选择 Python.org 的 Python 3.12 安装包或已有 Homebrew 的 python@3.12；如无 Node，选择 Node.js 24 LTS 或已有版本管理器。
这些安装步骤不由项目 bootstrap 自动执行，避免影响全局环境。优先复用已有兼容版本。

参考：[Vue 官方环境要求](https://vuejs.org/guide/quick-start)、[FastAPI 数据库说明](https://fastapi.tiangolo.com/tutorial/sql-databases/)、[Docker Compose 数据库示例](https://docs.docker.com/learn/content/run-a-multi-container-app-with-compose/)。
