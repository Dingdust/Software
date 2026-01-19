import os

from qfluentwidgets import qconfig
from qfluentwidgets import QConfig, ConfigItem, Theme, EnumSerializer, OptionsConfigItem, OptionsValidator


class Config(QConfig):
    base_url = ConfigItem("API", "BaseUrl", "https://apis.iflow.cn/v1")
    model_name = ConfigItem("API", "ModelName", "qwen-max")
    api_key = ConfigItem("API", "ApiKey", "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    theme = OptionsConfigItem(
        "UI", "Theme", Theme.AUTO, OptionsValidator(Theme), serializer=EnumSerializer(Theme))

cfg = Config()
_config_path = os.path.join(os.path.dirname(__name__), "config", "config.json")
os.makedirs(os.path.dirname(_config_path), exist_ok=True)
qconfig.load(_config_path, cfg)
cfg.save()
