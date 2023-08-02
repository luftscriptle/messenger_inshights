import easydict
import yaml


def get_config(config_path: str) -> dict:
    with open(config_path) as yfile:
        config = yaml.safe_load(yfile)
    return easydict.EasyDict(config)
