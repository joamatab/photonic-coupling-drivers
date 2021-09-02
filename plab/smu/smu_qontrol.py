from typing import Iterable, Union, Optional
from time import strftime, localtime
import pandas as pd
import numpy as np
from tqdm import tqdm
import qontrol
from plab.config import logger, CONFIG
from plab.measurement import measurement, Measurement


def smu_qontrol(serial_port_name: str = "/dev/ttyUSB0", imax: Optional[float] = 50e-3):
    """Returns qontrol SMU.

    https://github.com/takeqontrol/api
    """
    q = qontrol.QXOutput(
        serial_port_name=serial_port_name, response_timeout=0.1, imax=imax
    )
    logger.info(
        f"Qontroller {q.device_id} initialised with firmware {q.firmware} and {q.n_chs} channels"
    )

    device_info = dict(
        device_id=q.device_id, n_chs=q.n_chs, serial_port_name=serial_port_name
    )
    CONFIG.qontrol = device_info
    return q


if __name__ == "__main__":
    q = smu_qontrol()
