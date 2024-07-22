import json
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent.parent

def get_secret(
        key:str,
        default_value : Optional[str] = None,
        json_path : str = str(BASE_DIR/"secrets.json")
):
    with open(json_path) as f:
        secrets = json.loads(f.read())

    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        else:
            raise EnvironmentError(f"set the {key} environment variable")
        

MONGO_URL = get_secret("MONGO_URL")
MONGO_DB_NAME = get_secret("MONGO_DB_NAME")