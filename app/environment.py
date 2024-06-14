import os
import yaml


def resolve_code_path(parts=[]):
    path_components = [os.path.dirname(__file__), ".."]
    path_components.extend(parts)
    return os.path.join(*path_components)


os.environ["CONFIG_DIR"] = resolve_code_path(["config"])


def get_config():
    config_dir = os.environ["CONFIG_DIR"]
    config = {}
    with open(os.path.join(config_dir, "common.yml")) as common_config_file:
        config = yaml.safe_load(common_config_file)
    return config
