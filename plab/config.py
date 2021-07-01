"""Store CONFIG
"""

from typing import Any, Dict, Optional, Union
import os

import pathlib
import omegaconf
from loguru import logger

__version__ = "0.0.1"
PathType = Union[str, pathlib.Path]


class Path:
    module = pathlib.Path(__file__).parent.absolute()
    repo = module.parent
    labdata = repo / "labdata"
    home = pathlib.Path.home()
    cwd = pathlib.Path.cwd()


PATH = Path()


def read_config(yamlpath: Optional[PathType] = None) -> omegaconf.DictConfig:
    """Read CONFIG."""
    yamlpath_cwd = PATH.cwd / "config.yml"
    yamlpath_default = PATH.module / "config.yml"
    yamlpath_home = PATH.home / "config.yml"

    yamlpath = yamlpath or []
    yamlpaths = [yamlpath_default, yamlpath_home, yamlpath_cwd] + yamlpath
    CONFIG = omegaconf.OmegaConf.create()
    for yamlpath in yamlpaths:
        if os.access(yamlpath, os.R_OK) and yamlpath.exists():
            logger.info(f"loading config from {yamlpath}")
            CONFIG_NEW = omegaconf.OmegaConf.load(yamlpath)
            CONFIG = omegaconf.OmegaConf.merge(CONFIG, CONFIG_NEW)
    return CONFIG


CONFIG = read_config()


def ls(glob: str = "*.csv") -> None:
    """List all measured files"""
    for csv in PATH.labdata.glob(glob):
        print(csv.stem)


logger.info(f"plab {__version__}")
__all__ = ["CONFIG", "PATH", "ls"]

if __name__ == "__main__":
    # print(PATH.labdata)
    ls()
