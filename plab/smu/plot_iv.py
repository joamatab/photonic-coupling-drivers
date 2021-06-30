from typing import Iterable, Optional
import pandas as pd
import matplotlib.pyplot as plt
import plab


def plot_iv_max(df: pd.DataFrame, title: Optional[str] = None) -> None:
    """Plots max value for IV."""
    x = range(len(df.keys()))
    imax = [df[f"i_{i}"].max() for i in x]
    plt.plot(x, imax, "o")
    if title:
        plt.title(title)
    plt.xlabel("channel #")
    plt.ylabel("Max current (mA)")


def plot_iv(df: pd.DataFrame, keys: Optional[Iterable[str]]) -> None:
    """Plots all IV curves in separate plots."""
    keys = keys or df.keys()
    for key in keys:
        plt.figure()
        plt.title(f"{key}")
        plt.plot(df.index, df[key] * 1e3)
        plt.xlabel("V")
        plt.ylabel("I (mA)")


if __name__ == "__main__":
    for csv in plab.config.PATH.labdata.glob("*.csv"):
        print(csv.stem)

    print("\a")
    # df = pd.read_csv("")
    # x = range(64)
