"""Store configuration
"""

from typing import Any, Dict, Iterable, Optional, Union
import os

import pathlib
from omegaconf import OmegaConf
from loguru import logger

__version__ = "0.0.1"
PathType = Union[str, pathlib.Path]
home = pathlib.Path.home()
cwd = pathlib.Path.cwd()
cwd_config = cwd / "config.yml"

home_config = home / ".config" / "piclab.yml"
config_dir = home / ".config"
config_dir.mkdir(exist_ok=True)
module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent


yamlpath_cwd = cwd / "config.yml"
yamlpath_default = module_path / "config.yml"
yamlpath_home = home / "config.yml"


def read_config(
    yamlpaths: Iterable[PathType] = (yamlpath_default, yamlpath_home, yamlpath_cwd),
) -> Dict[str, Any]:
    CONFIG = OmegaConf.create()
    for yamlpath in set(yamlpaths):
        if os.access(yamlpath, os.R_OK) and yamlpath.exists():
            logger.info(f"loading tech config from {yamlpath}")
            CONFIG_NEW = OmegaConf.load(yamlpath)
            CONFIG = OmegaConf.merge(CONFIG, CONFIG_NEW)
    return CONFIG


logger.info(f"plab {__version__}")


class Path:
    module = module_path
    repo = repo_path
    labdata = repo_path / "labdata"


def ls(glob: str = "*.csv") -> None:
    """List all measured files"""
    for csv in PATH.labdata.glob(glob):
        print(csv.stem)


PATH = Path()
__all__ = ["CONFIG", "PATH", "ls"]

if __name__ == "__main__":
    # print(PATH.labdata)
    ls()
