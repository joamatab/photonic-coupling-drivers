from typing import Iterable, Union
import pydantic
import pytest
import pandas as pd
import numpy as np
import plab
from plab.config import write_config, PATH
from plab.measurement import measurement


@measurement
def demo(
    vmin: float = 0.0,
    vmax: float = 1.0,
    vsteps: int = 20,
    channels: Union[Iterable[int], int] = (0,),
    **kwargs
) -> pd.DataFrame:
    """

    Args:
        vmin: min voltage
        vmax: max voltage
        vsteps: number of steps between min and max voltage
        **kwargs: any labstate arguments that we want to log
    """
    voltages = np.linspace(vmin, vmax, vsteps)
    return pd.DataFrame(dict(v=voltages))


def test_validator_error():
    with pytest.raises(pydantic.ValidationError):
        demo(vmin="wrong")


if __name__ == "__main__":
    m = demo(vstep=21.5555, channels=1)
    m.write(overwrite=True, dirpath=PATH.cwd)
    # test_validator_error()
