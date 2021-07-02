"""Measurement decorator.

- Gives a name to the measurement based on function input parameters
    - stores labstate settings CONFIG
    - timestamps
    - function settings
- adds the measurement into a CACHE
"""

from typing import Optional, Dict, Union
import functools
import inspect
import dataclasses
import pathlib

import time
from pydantic import validate_arguments
import pandas as pd
import numpy as np
from omegaconf import OmegaConf
import omegaconf
from plab.config import PATH, logger, CONFIG


@dataclasses.dataclass
class Measurement:
    data: Optional[pd.DataFrame] = None
    metadata: Optional[Union[omegaconf.DictConfig, omegaconf.ListConfig]] = None

    def write(
        self,
        filename: Optional[str] = None,
        dirpath: pathlib.Path = PATH.labdata,
        overwrite: bool = False,
    ) -> None:
        filename = filename or f"{self.metadata.name}.csv"
        csvpath = dirpath / filename
        yamlpath = csvpath.with_suffix(".yml")
        if csvpath.exists() and not overwrite:
            raise FileExistsError(f"File {csvpath} exists")
        self.data.to_csv(csvpath)
        logger.info(f"Write {csvpath}")

        yamlpath.write_text(OmegaConf.to_yaml(self.metadata))
        logger.info(f"Write {yamlpath}")

    def read(self, name: str, dirpath: pathlib.Path = PATH.labdata) -> None:
        self.data = pd.read_csv(dirpath / f"{name}.csv")
        self.metadata = OmegaConf.load(dirpath / f"{name}.yml")

    def ls(self, glob: str = "*.csv") -> None:
        """List all measured files"""
        for csv in PATH.labdata.glob(glob):
            print(csv.stem)


CACHE: Dict[str, Measurement] = {}

_remap = {
    " ": "_",
    "'": "",
}


def measurement_without_validator(func):
    """measurement decorator.
    Adds a measurement name based on input parameters
    logs measurement metadata into CONFIG
    """

    @functools.wraps(func)
    def _measurement(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        # timestamp = time.strftime("%y%m%d%H%M%S", time.localtime())
        kwargs_copy = kwargs.copy()
        kwargs_copy.pop("description", "")
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs_copy.items()]
        name = f"{func.__name__}_{'_'.join(kwargs_repr)}"

        for k, v in _remap.items():
            name = name.replace(k, v)
        arguments = ", ".join(args_repr + kwargs_repr)

        if args:
            raise ValueError(
                f"measurement supports only Keyword args for `{func.__name__}({arguments})`"
            )

        assert callable(
            func
        ), f"{func} got decorated with @measurement! @measurement decorator is only for functions"
        sig = inspect.signature(func)
        t0 = time.time()
        logger.info(f"Starting {func.__name__}({','.join(kwargs_repr)}))")

        data = func(*args, **kwargs)

        if not isinstance(data, pd.DataFrame):
            logger.warning(f"{func.__name__} needs to return a pandas.DataFrame")

        logger.info(f"Finished {func.__name__}({','.join(kwargs_repr)}))")
        t1 = time.time()
        dt = t1 - t0

        settings = {}
        settings.update(
            **{
                p.name: p.default
                for p in sig.parameters.values()
                if not callable(p.default)
            }
        )
        settings.update(**kwargs)

        timestamp = time.strftime("%y-%m-%d_%H:%M:%S", time.localtime())
        time_dict = dict(t0=t0, t1=t1, dt=dt, timestamp=timestamp)
        metadata = OmegaConf.create(
            dict(name=name, time=time_dict, settings=settings, config=CONFIG)
        )
        measurement = Measurement(data=data, metadata=metadata)
        CACHE[name] = measurement
        return measurement

    return _measurement


def measurement(func, *args, **kwargs) -> Measurement:
    return measurement_without_validator(validate_arguments(func), *args, **kwargs)


@measurement
def demo(
    vmin: float = 0.0, vmax: float = 1.0, vsteps: int = 20, **kwargs
) -> Measurement:
    """

    Args:
        vmin: min voltage
        vmax: max voltage
        vsteps: number of steps between min and max voltage
        **kwargs: any labstate arguments that we want to log
    """
    voltages = np.linspace(vmin, vmax, vsteps)
    df = pd.DataFrame(dict(v=voltages))
    return df


if __name__ == "__main__":
    m = demo(sample="demo2")
    print(m.metadata.name)
    m.write(overwrite=True, dirpath=PATH.cwd)
