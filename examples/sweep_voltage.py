import pandas as pd
import numpy as np
import qontrol
from plab.config import PATH


serial_port_name = "/dev/ttyUSB0"
q = qontrol.QXOutput(serial_port_name=serial_port_name, response_timeout=0.1)

print(
    "Qontroller '{:}' initialised with firmware {:} and {:} channels".format(
        q.device_id, q.firmware, q.n_chs
    )
)


def sweep_voltage(
    vmin: float = 0, vmax: float = 1, vsteps: int = 20, n: int = 1
) -> pd.DataFrame:
    """Sweep voltage and measure current.

    Args:
        vmin: min voltage
        vmax: max voltage
        vsteps: number of steps
        n: number of channels to sweep
    """
    voltages = np.linspace(vmin, vmax, vsteps)
    df = pd.DataFrame(dict(v=voltages))

    for channel in range(n):
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

    df.to_csv(PATH.labdata / f"sweep_voltage_{vmin}_{vmax}_{vsteps}_{n}.csv")

    # set all channels to zero
    q.v[:] = 0
    return df


def get_current(channel: int, voltage: float) -> float:
    q.v[channel] = float(voltage)

    return q.v[channel]


def demo():
    voltages = np.linspace(0, 1, 3)
    n = 32
    df = pd.DataFrame(dict(v=voltages))

    for channel in range(n):
        currents = np.zeros_like(voltages)
        for j, voltage in enumerate(voltages):
            # Set voltage
            q.v[channel] = float(voltage)

            # Measure voltage (Q8iv)
            measured_voltage = q.v[channel]

            # Measure current (Q8iv, Q8b, Q8)
            measured_current = q.i[channel]
            currents[j] = measured_current

        df[f"i_{channel}"] = currents

    print(df)
    df.to_csv()


if __name__ == "__main__":
    # print(get_current(62, 0.1))
    df = sweep_voltage(vmax=3, n=1)
