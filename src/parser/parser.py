import os

import pandas as pd


def read(filePath: str):
    try:
        unparsed_data = pd.read_csv(filePath)
    except FileNotFoundError:
        raise FileNotFoundError(f"no such file: {filePath}")
    except PermissionError:
        raise PermissionError(f"cannot read file: {filePath}")
    except pd.errors.EmptyDataError:
        raise ValueError(f"file is empty: {filePath}")
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        raise ValueError(f"could not parse {filePath} as CSV: {e}")

    cleaned = unparsed_data.dropna(axis=1, how="all")
    cleaned = cleaned.drop(columns="Index", errors="ignore")
    if cleaned.empty:
        raise ValueError(f"no usable data in {filePath}")
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
