import pydantic
import pytest
import pandas as pd
import numpy as np
import plab
from plab.config import write_config, PATH


@plab.measurement
def demo(
    vmin: float = 0.0,
    vmax: float = 1.0,
    vsteps: int = 20,
) -> pd.DataFrame:
    voltages = np.linspace(vmin, vmax, vsteps)
    df = pd.DataFrame(dict(v=voltages))

    csvpath = PATH.labdata / "a.csv"
    df.to_csv(csvpath)
    df.path = csvpath
    return df


def test_validator_error():
    with pytest.raises(pydantic.ValidationError):
        demo(vmin="wrong")


if __name__ == "__main__":
    df = demo()
    write_config(df.path.with_suffix(".yml"))
    # test_validator_error()
