from typing import Iterable, Union
from time import strftime, localtime
import pandas as pd
import numpy as np
import qontrol
from plab.config import PATH, logger, CONFIG
from plab.measurement import measurement, Measurement


def smu_qontrol(serial_port_name: str = "/dev/ttyUSB2"):
    """Returns qontrol SMU."""
    q = qontrol.QXOutput(serial_port_name=serial_port_name, response_timeout=0.1)
    logger.info(
        f"Qontroller {q.device_id} initialised with firmware {q.firmware} and {q.n_chs} channels"
    )

    device_info = dict(
        device_id=q.device_id, n_chs=q.n_chs, serial_port_name=serial_port_name
    )
    CONFIG.qontrol = device_info
    return q


@measurement
def sweep_voltage(
    vmin: float = 0.0,
    vmax: float = 1.0,
    vsteps: int = 20,
    channels: Union[Iterable[int], int] = 64,
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
    q = smu_qontrol()
    voltages = np.linspace(vmin, vmax, vsteps)
    df = pd.DataFrame(dict(v=voltages))

    if isinstance(channels, int):
        channels = range(channels)

    for channel in channels:
        currents = np.zeros_like(voltages)

        for j, voltage in enumerate(voltages):
            q.v[channel] = float(voltage)

            # Measure voltage (Q8iv)
            # measured_voltage = q.v[channel]

            # Measure current (Q8iv, Q8b, Q8)
            currents[j] = q.i[channel]

        q.v[channel] = 0
        df[f"i_{channel}"] = currents

    df.set_index(df["v"], inplace=True)
    df.pop("v")

    # set all channels to zero
    # q.v[:] = 0
    return df


def get_current(channel: int, voltage: float) -> float:
    """Sets voltage for a channel and measures the current.

    Args:
        channel:
        voltage:
    """
    q = smu_qontrol()
    q.v[channel] = float(voltage)
    return q.i[channel]


if __name__ == "__main__":
    # print(get_current(62, 0.1))
    m = sweep_voltage(vmax=3, channels=(1,))
    m.write()
