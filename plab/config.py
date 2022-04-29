"""Store CONFIG
"""

from typing import Any, Optional, Union
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


def read_config() -> Union[omegaconf.DictConfig, omegaconf.ListConfig]:
    """Read CONFIG from a datapath and overwrites with highest priority.

    As well as data from

    - yamlpath_cwd (higher priority)
    - yamlpath_default
    - yamlpath_home: a file in ~/.plab.yml

    """
    yamlpath = PATH.cwd / "config.yml"
    if os.access(yamlpath, os.R_OK) and yamlpath.exists():
        logger.info(f"loading config from {yamlpath}")
        return omegaconf.OmegaConf.load(yamlpath)
    else:
        return omegaconf.OmegaConf.create()


def write_config(yamlpath: PathType) -> None:
    """Read CONFIG in YAML format."""
    config_str = omegaconf.OmegaConf.to_yaml(CONFIG)
    yamlpath = pathlib.Path(yamlpath)
    yamlpath.write_text(config_str)


CONFIG = read_config()


def ls(glob: str = "*.csv") -> None:
    """List all measured files"""
    for csv in PATH.labdata.glob(glob):
        print(csv.stem)


CONFIG.version = __version__


logger.info(f"plab {__version__}")
__all__ = ["CONFIG", "PATH", "ls", "write_config", "read_config"]

if __name__ == "__main__":
    # print(PATH.labdata)
    ls()
