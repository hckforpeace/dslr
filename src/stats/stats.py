import math

from pandas import Series
from pandas.core.interchange.dataframe_protocol import Column


def count(column: Series):
    cnt = 0
    for v in column:
        if v is not None and not math.isnan(v):
            cnt = cnt + 1
    return float(cnt)

def mean(column: Series):
    total = 0
    n = 0
    for v in column:
        if v is not None and not math.isnan(v):
            total = total + v
            n = n + 1
    return total / n if n else float("nan")
    
def std(column: Series):
    n = count(column)
    avg = mean(column)
    distanceValue = 0

    for v in column:
        if v is not None and not math.isnan(v):
            distanceValue = distanceValue + math.pow(v - avg, 2)
    return math.sqrt(distanceValue / (n - 1))

def q1(column: Series):
    values = sorted(v for v in column if v is not None and not math.isnan(v))
    n = len(values)
    if n == 0:
        return float("nan")
    pos = 0.25 * (n - 1)
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return values[int(pos)]
    return values[lower] + (values[upper] - values[lower]) * (pos - lower)

def q2(column: Series):
    values = sorted(v for v in column if v is not None and not math.isnan(v))
    n = len(values)
    if n == 0:
        return float("nan")
    pos = 0.5 * (n - 1)
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return values[int(pos)]
    return values[lower] + (values[upper] - values[lower]) * (pos - lower)

def q3(column: Series):
    values = sorted(v for v in column if v is not None and not math.isnan(v))
    n = len(values)
    if n == 0:
        return float("nan")
    pos = 0.75 * (n - 1)
    lower = math.floor(pos)
    upper = math.ceil(pos)
    if lower == upper:
        return values[int(pos)]
    return values[lower] + (values[upper] - values[lower]) * (pos - lower)

def min(column: Series):
    values = sorted(v for v in column if v is not None and not math.isnan(v))
    n = len(values)
    if n == 0:
        return float("nan")
    return values[0]

def max(column: Series):
    values = sorted(v for v in column if v is not None and not math.isnan(v))
    n = len(values)
    if n == 0:
        return float("nan")
    return values[n - 1]
