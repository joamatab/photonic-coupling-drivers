from typing import Iterable, Union, Optional
from time import strftime, localtime
import pandas as pd
import numpy as np
from tqdm import tqdm
import qontrol
from plab.config import logger, CONFIG
from plab.measurement import measurement, Measurement
from plab.smu.smu_control import smu_control


@measurement
def sweep_current(
    imin: float = 0, imax: float = 50e-3, steps: int = 20, n: int = 1
) -> pd.DataFrame:
    """Sweep current and measure voltage. works only for q8iv

    Args:
        imin: min current
        imax: max current
        steps: number of steps
        n: number of channels to sweep
    """
    currents = np.linspace(imin, imax, steps)
    df = pd.DataFrame(dict(i=currents))

    if isinstance(n, int):
        channels = range(n)
    else:
        channels = n
    for channel in channels:
        currents = np.zeros_like(currents)
        # set all channels to zero
        q.v[:] = 0
        for j, voltage in enumerate(currents):
            q.i[channel] = float(voltage)
            measured_voltage = q.v[channel]
            measured_current = q.i[channel]
            currents[j] = measured_current

        df[f"i_{channel}"] = currents
    return df


def get_current(channel: int, voltage: float) -> float:
    """Sets voltage for a channel and returns measured current.

    Args:
        channel:
        voltage:

    """
    q = smu_qontrol()
    q.v[channel] = float(voltage)
    return q.i[channel]


def zero_voltage() -> None:
    """Sets all voltage channels to zero."""
    q = smu_qontrol()
    q.v[:] = 0
    return


if __name__ == "__main__":
    zero_voltage()
    # print(get_current(62, 0.1))
    # m = sweep_voltage(vmax=3, channels=(1,))
    # m.write()
