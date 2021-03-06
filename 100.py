#!/bin/env python3
from os import path
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime as dt

DATE_FMT = "%d/%m/%Y"


def to_seconds(time_str):
    """
    Return the number of seconds corresponding to
    a duration string formatted as %M'%S
    """
    m, s = time_str.split("'")
    return int(m) * 60 + int(s)


def seconds_formatter(x, pos):
    """
    Formatter used for the plot's xaxis, takes x as
    a number of seconds (float), and returns a string.
    For example, x:90.0 returns "01m30s"
    """
    m = x // 60
    s = x % 60
    return "{:02.0f}m{:02.0f}s".format(m, s)


def load_data(file_path):
    dates = []
    pushups_times = []
    squats_times = []

    with open(file_path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            dates.append(dt.strptime(row["date"], DATE_FMT).date())
            pushups_times.append(to_seconds(row["pushups_time"]))
            squats_times.append(to_seconds(row["squats_time"]))
    return dates, pushups_times, squats_times


if __name__ == "__main__":
    dirname = path.dirname(__file__)
    data_path = path.join(dirname, "data.csv")
    d, pt, st = load_data(data_path)
    fig, ax1 = plt.subplots()

    ax1.set_ylabel("Time to 100 reps")
    ax1.xaxis.set_major_formatter(mdates.DateFormatter(fmt=DATE_FMT))

    locator = mdates.DayLocator(interval=2)
    fig.autofmt_xdate()  # rotate and align the tick labels so they look better
    ax1.xaxis.set_major_locator(locator)
    ax1.yaxis.set_major_formatter(FuncFormatter(seconds_formatter))

    ax1.plot(d, pt, "o:", label="push-ups")
    ax1.plot(d, st, "o:", label="squats")
    ax1.legend()
    ax1.set_title("100 push-ups and squats every 2 days: timing progression")

    fig.tight_layout()
    fig.savefig("figure.png")
