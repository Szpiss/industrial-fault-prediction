# 机器学习模块

未来按 preprocessing → features → training → evaluation 管理离线训练流程，models 存储模型说明，datasets 存储有来源授权的数据。

暂不安装 scikit-learn、XGBoost、PyTorch，不实现模型训练或推理。后续独立管理 ML 依赖，避免拖慢 Web 服务环境。大型数据与模型权重默认不进入 Git。
