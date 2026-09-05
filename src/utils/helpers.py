from pathlib import Path
import yaml
from typing import Dict, Any

def get_project_root() -> Path:
    """Returns absolute path to the project root directory."""
    return Path(__file__).resolve().parent.parent.parent

def load_yaml_config(file_path: str) -> Dict[str, Any]:
    """Loads YAML configuration file."""
    path = Path(file_path)
    if not path.is_absolute():
        path = get_project_root() / path
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
