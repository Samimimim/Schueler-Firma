import json


def get_settings():
    with open('../data/settings.json', 'r') as f:
        settings = json.load(f)
        return settings


def save_settings(settings):
    with open('..\data\settings.json', 'w') as f:
        json.dump(settings, f, indent=4)


def update_setting(key, value):
    settings = get_settings()
    if key in settings:
        settings[key] = value
        save_settings(settings)
        return True
    else:
        return False 
    
    
def get_setting(key):
    settings = get_settings()
    return settings.get(key, None)
