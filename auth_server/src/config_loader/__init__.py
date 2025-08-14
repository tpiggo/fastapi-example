import itertools
import os
from pathlib import Path
from typing import TypeVar, Any

from pydantic import BaseModel
from yaml import loader, load
import glob
import logging

T = TypeVar("T", bound=BaseModel)

logger = logging.getLogger(__name__)


def _merge(item: dict[str, Any], built_item: dict[str, Any]):
    if not built_item:
        return {**item}
    for key in item:
        if not built_item.get(key):
            built_item[key] = item[key]
        elif isinstance(item[key], dict) and isinstance(built_item[key], dict):
            _merge(item[key], built_item[key])
        else:
            built_item[key] = item[key]

    return built_item


def configuration_properties(model: type[T]):
    import sys
    _this_module = sys.modules[__name__]
    _root_dir = Path(os.path.abspath(__file__)).parent.parent
    root_dir = Path(_root_dir) / model.__module__.split(".")[0] / "resources"

    environments = os.environ.get("PROFILES", "").split(",")
    config_files = glob.glob("*.yaml", root_dir=root_dir)
    files: dict[str | None, Path] = {}

    for config_file in map(Path, config_files):
        file_name_split = config_file.stem.split(".")
        if len(file_name_split) > 2:
            print(f"Skipping {str(config_file)}")
            continue
        f_name, f_ext = file_name_split if len(file_name_split) == 2 else file_name_split[-1], None
        if f_name == "application":
            files[f_ext] = config_file
    loaded_config: dict[str, Any] = {}

    def map_env_to_files(_env: str | None):
        return root_dir / files[_env] if _env in files else None

    for path in filter(lambda _path: _path is not None, map(map_env_to_files, [None] + environments)):
        with open(path, "r") as f:
            next_item = load(f, loader.FullLoader)
            logger.debug(f"using config in file {path}")
            loaded_config = _merge(next_item, loaded_config)
    built = model(**loaded_config)

    def _loader() -> T:
        return built

    return _loader
