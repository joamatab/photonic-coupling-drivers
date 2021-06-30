from typing import Iterable
from time import strftime, localtime
import pandas as pd
import numpy as np
import qontrol
from plab.config import PATH, logger


serial_port_name = "/dev/ttyUSB2"
q = qontrol.QXOutput(serial_port_name=serial_port_name, response_timeout=0.1)

print(
    f"Qontroller {q.device_id} initialised with firmware {q.firmware} and {q.n_chs} channels"
)


def sweep_voltage(
    sample: str = "sample_name",
    vmin: float = 0.0,
    vmax: float = 1.0,
    vsteps: int = 20,
    channels: Iterable[int] = (0,),
) -> pd.DataFrame:
    """Sweep voltage and measure current.

    Args:
        sample: name of the sample
        vmin: min voltage
        vmax: max voltage
        vsteps: number of steps
        channels: specific channels to sweep
    """
    timestamp = strftime("%y%m%d%H%M", localtime())
    filename = f"sweep_voltage_{timestamp}_{sample}_{vmin}_{vmax}_{vsteps}_{channels}"
    logger.info(filename, 'start')
    voltages = np.linspace(vmin, vmax, vsteps)
    df = pd.DataFrame(dict(v=voltages))

    for channel in channels:
        currents = np.zeros_like(voltages)

        # set all channels to zero
        q.v[:] = 0
        for j, voltage in enumerate(voltages):
            # Set voltage
            q.v[channel] = float(voltage)

            # Measure voltage (Q8iv)
            measured_voltage = q.v[channel]

            # Measure current (Q8iv, Q8b, Q8)
            measured_current = q.i[channel]
            currents[j] = measured_current

        df[f"i_{channel}"] = currents

    df.set_index(df["v"], inplace=True)
    df.pop("v")
    df.to_csv(PATH.labdata / f"{filename}.csv")

    # set all channels to zero
    q.v[:] = 0
    logger.info(filename, 'finished')
    return df


def get_current(channel: int, voltage: float) -> float:
    q.v[channel] = float(voltage)

    return q.v[channel]


if __name__ == "__main__":
    # print(get_current(62, 0.1))
    df = sweep_voltage(vmax=3, channels=1)
