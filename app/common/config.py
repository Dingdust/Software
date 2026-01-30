import os

import qfluentwidgets as qfw


class Config(qfw.QConfig):
    base_url = qfw.ConfigItem("API", "BaseUrl", "https://apis.iflow.cn/v1")
    model_name = qfw.ConfigItem("API", "ModelName", "qwen-max")
    api_key = qfw.ConfigItem("API", "ApiKey", "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    theme = qfw.OptionsConfigItem(
        "UI", "Theme", qfw.Theme.AUTO, qfw.OptionsValidator(qfw.Theme), serializer=qfw.EnumSerializer(qfw.Theme))


cfg = Config()
_config_path = os.path.join(os.path.dirname(__name__), "app", "config", "config.json")
os.makedirs(os.path.dirname(_config_path), exist_ok=True)
qfw.qconfig.load(_config_path, cfg)
cfg.save()
