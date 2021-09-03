from typing import Iterable, Union, Callable
from time import strftime, localtime
import pandas as pd
import numpy as np
from tqdm import tqdm
import qontrol
from plab.config import logger, CONFIG
from plab.measurement import measurement, Measurement
from plab.smu.smu_qontrol import smu_qontrol


@measurement
def sweep_voltage(
    vmin: float = 0.0,
    vmax: float = 2.0,
    vsteps: int = 3,
    channels: Union[Iterable[int], int] = 64,
    get_instrument: Callable = smu_qontrol,
    **kwargs,
) -> Measurement:
    """Sweep voltage and measure current.

    Args:
        vmin: min voltage
        vmax: max voltage
        vsteps: number of steps
        channels: number of channels to sweep or specific channels (iterable)
        **kwargs: captures labstate metadata in @measurement
    """
    q = get_instrument()
    voltages = np.linspace(vmin, vmax, vsteps)
    df = pd.DataFrame(dict(v=voltages))

    if isinstance(channels, int):
        channels = range(channels)

    for channel in tqdm(channels):
        currents = np.zeros_like(voltages)

        for j, voltage in enumerate(voltages):
            q.v[channel] = float(voltage)
            currents[j] = q.i[channel]

        q.v[channel] = 0
        df[f"i_{channel}"] = currents

    df.set_index(df["v"], inplace=True)
    df.pop("v")
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
