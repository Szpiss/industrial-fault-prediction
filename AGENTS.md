# 工程协作约定

## 项目与阶段

项目：《基于Web与机器学习的工业设备故障预测系统的设计与实现》。计算机科学与技术本科毕业设计。
当前为第一阶段：最小可运行全栈基础框架。只实现健康检查、数据库基础与页面占位。
未经用户明确要求，不提前实现设备 CRUD、认证、CSV 导入、预测接口、模型训练或复杂业务图表。

## 技术栈

- Python 3.12 推荐；FastAPI、Pydantic 2 / pydantic-settings、SQLAlchemy 2.0、Alembic、Uvicorn。
- 默认 SQLite，MySQL 8.4 LTS 由 Docker Compose 管理，驱动 PyMySQL。
- Vue 3 Composition API、TypeScript strict、Vite 7、Vue Router 4、Pinia 3、Element Plus、Axios。
- ECharts 6 已安装，尚未使用；scikit-learn、XGBoost、PyTorch 仅规划，禁止无故安装重依赖。
- Node 24 LTS 推荐，兼容符合 package.json engines 的 Node 22；npm + package-lock.json。
- pytest / Vitest，Ruff，ESLint 10 flat config，Prettier。

## 结构与边界

- backend/app/api：HTTP 路由与依赖注入；schemas：请求/响应数据模型。
- services：未来业务规则；repositories：未来数据库访问；models：ORM 模型。
- core：配置、日志、异常；db：Base、engine、session；main.py：应用组合。
- frontend/src/api：Axios 客户端与接口；stores：跨组件状态；router：路由。
- layouts：整体布局；views：页面；components：复用组件；types：公共类型。
- ml：独立的离线数据预处理、特征、训练、评估目录，不与 Web 生命周期耦合。
- docs：架构、环境、验证记录和后续计划；scripts：从任意工作目录可执行的辅助脚本。
- 只在有实际需求时引入额外抽象，第一阶段不创建空泛的通用 CRUD 框架。

## 编码与配置规范

- Python 4 空格、类型注解、Ruff 100 列；TS/Vue 2 空格、单引号、无分号，遵循 Prettier。
- Vue 使用 `<script setup lang="ts">`；请求通过 api 层，组件不硬编码后端域名。
- API 统一前缀 `/api/v1`；错误格式 `{ "error": { "code": "...", "message": "..." } }`。
- 使用 SQLAlchemy 2 风格；每个请求单独 session；有业务写入时显式管理事务。
- 新增 ORM 模型必须在 app/models/__init__.py 导入，让 Alembic 能发现；检查自动生成迁移后提交。
- 不使用启动时 create_all 代替迁移；迁移必须支持合理回退并在临时数据库验证。
- 配置从根目录 .env 读取；所有示例写入 .env.example；真实密码、数据、模型、日志不入 Git。
- VITE_ 变量会暴露给浏览器，禁止放密码/密钥；不要记录包含密码的数据库 URL 或 SQL 参数。
- 不修改全局 Git、Python、Node 或系统服务；系统安装/权限操作先获得用户确认。
- 修改已有成果前先检查；保留真实来源、验证记录和未完成标记，不编造预测结果或工业现场接入。

## 验证与交付

- 使用 `./scripts/check.sh` 完成后端 Ruff/pytest/pip check、前端类型/lint/format/Vitest/build。
- 行为修改应添加能发现真实回归的测试；不为纯占位组件堆砌形式化测试。
- 前端连接状态有正常、加载、断连和重试；清除失效的历史健康数据。
- 界面修改后尽量使用真实浏览器检查；截图放 output/playwright/，不跟踪浏览器缓存。
- 数据库迁移和真实启动单独验证；构建成功不能替代运行验证。
- Docker 或外部服务缺失时必须明确写“未验证”；不得把 MySQL SQL 静态生成描述为实际连接通过。
- 依赖变化同步 pyproject.toml / requirements-dev.lock 或 package.json / package-lock.json。
- 完成后更新 README 与 docs/verification.md，说明实际检查、限制和下一步。
