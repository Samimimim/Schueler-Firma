import json

CONFIG_PATH = "./config/settings.json"


def get_settings():
    with open(CONFIG_PATH, "r") as f:
        settings = json.load(f)
        return settings


def save_settings(settings):
    with open(CONFIG_PATH, "w") as f:
        json.dump(settings, f, indent=4)


def update_setting(key, value):
    settings = get_settings()
    if key in settings:
        settings[key] = value
        save_settings(settings)
        return True
    else:
        return False


def get_setting(keys):
    settings = get_settings()
    if isinstance(keys, list):
        value = settings
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return None
        return value
    return settings.get(keys, None)
