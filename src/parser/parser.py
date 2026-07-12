import pandas as pd

path = "../datasets/"


def read(filename: str):
    filenamePath = path + filename
    unparsed_data = pd.read_csv(filenamePath)
    cleaned = unparsed_data.dropna(axis=1, how="all")
    cleaned = cleaned.drop(columns="Index", errors="ignore")
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
