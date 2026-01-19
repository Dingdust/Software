import os

from qfluentwidgets import qconfig
from qfluentwidgets import QConfig, ConfigItem


class Config(QConfig):
    base_url = ConfigItem("API", "BaseUrl", "https://apis.iflow.cn/v1")
    api_key = ConfigItem("API", "ApiKey", "")
    model_name = ConfigItem("API", "ModelName", "qwen-max")

cfg = Config()
_config_path = os.path.join(os.path.dirname(__name__), "config", "config.json")
os.makedirs(os.path.dirname(_config_path), exist_ok=True)
qconfig.load(_config_path, cfg)
cfg.save()
