import os
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent.parent

CONFIG_PATH = os.environ.get('CONFIG_PATH', BASE_DIR / 'config.yaml')

def load_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

config = load_config()
