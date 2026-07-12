import os

import pandas as pd

path = "../datasets/"


def _resolve(filename: str) -> str:
    """Resolve `filename` inside the datasets dir, rejecting path traversal."""
    base = os.path.abspath(path)
    # If the caller passes an absolute path, use it as-is; otherwise anchor it
    # to the datasets directory.
    candidate = filename if os.path.isabs(filename) else os.path.join(base, filename)
    resolved = os.path.abspath(candidate)
    # Reject anything that escapes the datasets directory (e.g. "../../etc/passwd").
    if not os.path.isabs(filename) and os.path.commonpath([base, resolved]) != base:
        raise ValueError(f"refusing to read outside datasets directory: {filename!r}")
    return resolved


def read(filename: str):
    filenamePath = _resolve(filename)
    try:
        unparsed_data = pd.read_csv(filenamePath)
    except FileNotFoundError:
        raise FileNotFoundError(f"no such file: {filenamePath}")
    except PermissionError:
        raise PermissionError(f"cannot read file: {filenamePath}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"file is empty: {filenamePath}")
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        raise ValueError(f"could not parse {filenamePath} as CSV: {e}")

    cleaned = unparsed_data.dropna(axis=1, how="all")
    cleaned = cleaned.drop(columns="Index", errors="ignore")
    if cleaned.empty:
        raise ValueError(f"no usable data in {filenamePath}")
    return cleaned


def getNumericalValues(df: pd.DataFrame):
    numerical_col_ds = df.select_dtypes(include="number")
    numerical_col_ds = numerical_col_ds.apply(pd.to_numeric, errors="coerce")
    return numerical_col_ds


# if __name__ == "__main__":
#     filename = "dataset_test.csv"
#     parsed_numerical_columns_ds = getNumericalValues(read(filename))
#     for title in parsed_numerical_columns_ds:
#         print(title)
#
