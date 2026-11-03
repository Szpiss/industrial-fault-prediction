# 架构与扩展边界

浏览器页面 → Pinia / API 封装 → Axios `/api/v1` → Vite 开发代理 → FastAPI 路由 → SQLAlchemy session → SQLite / MySQL。

目前 health 路由直接执行一个只读 SELECT 1，不为了单个探针引入 services/repositories 的空抽象。
后续业务使用 api → services → repositories → models 的依赖方向：路由处理 HTTP，服务处理事务和规则，仓储处理 ORM 查询，schema 与 ORM 模型分离。
SQLAlchemy 使用同步 session，因此数据库访问路由用 def 由 FastAPI 在线程池运行，不在 async 路由阻塞事件循环。

配置固定从根 .env 读取，Pydantic 解析类型和 JSON 来源列表。数据库 URL 在日志与响应中不输出明文密码。
数据库故障返回 503，HTTP 错误、参数错误、未捕获异常都有统一 error 包装。服务器日志记录未捕获异常，不向客户端回传栈。
健康接口不创建业务表、不执行训练、不提供设备认证功能。默认 Swagger /docs、OpenAPI /openapi.json。

前端主布局负责导航，页面按路由懒加载。健康 store 保存本次状态，失败清除旧结果；组件只通过 api 层请求。
ECharts 安装在前端但未加载，图表组件位置见 components/charts。占位页面标记规划中，不以示例数值冒充真实运行数据。

MySQL 采用 Compose 单服务和命名卷，Web 服务保留本机开发方式，避免本阶段引入复杂容器部署。
当前迁移为空基线，后续首张设备表必须用 Alembic 建立。不要通过 create_all 让迁移与真实表结构分叉。

ML 目录独立预留：datasets 记录数据来源与许可，preprocessing 清洗，features 定义特征，training 训练，evaluation 保存评估代码与说明，models 记录制品。
后续以明确输入/输出契约接入服务层；训练过程独立运行，不能挂在 API 启动或健康请求里。大文件不进入 Git。

后续权限与操作日志需在业务需求明确后设计；当前无登录、无权限限制，仅供回环地址本地开发。
