from typing import Iterable
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
    channels: Iterable[int] = (0,),
    **kwargs,
) -> Measurement:
    """Sweep voltage and measure current.

    Args:
        vmin: min voltage
        vmax: max voltage
        vsteps: number of steps
        channels: specific channels to sweep
        **kwargs: captures labstate metadata in @measurement
    """
    q = smu_qontrol()

    # timestamp = strftime("%y%m%d%H%M", localtime())
    # filename = f"sweep_voltage_{timestamp}_{sample}_{vmin}_{vmax}_{vsteps}_{channels}"
    # logger.info(filename, "start")

    voltages = np.linspace(vmin, vmax, vsteps)
    df = pd.DataFrame(dict(v=voltages))

    for channel in channels:
        currents = np.zeros_like(voltages)

        # set all channels to zero
        # q.v[:] = 0
        for j, voltage in enumerate(voltages):
            # Set voltage
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
    # filepath = PATH.labdata / f"{filename}.csv"
    # logger.info(filename, "finished")
    # df.to_csv(filepath)
    # df.path = filepath
    return df


@measurement
def get_current(channel: int, voltage: float) -> float:
    q = smu_qontrol()
    q.v[channel] = float(voltage)
    return q.v[channel]


if __name__ == "__main__":
    # print(get_current(62, 0.1))
    m = sweep_voltage(vmax=3, channels=(1,))
    m.write()
