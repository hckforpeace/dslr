import sys

from parser import read, getNumericalValues
from stats import count, mean, std, q1, q2, q3, min, max
from prettytable import PrettyTable

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <dataset.csv>", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]

    df = read(filename)
    df = getNumericalValues(df)

    print(df.describe())

    table = PrettyTable()
    table.border = False
    table.align = "r"
    table.left_padding_width = 0
    table.right_padding_width = 2
    fields = [""]
    countRow = ["Count"]
    meanRow = ["Mean"]
    stdRow = ["Std"]
    q1Row = ["25%"]
    q2Row = ["50%"]
    q3Row = ["75%"]
    minRow = ["min"]
    maxRow = ["max"]

    for title in df:
        fields.append(title)

    table.field_names = fields
    
    for title in df:
        countRow.append(f"{count(df[title]):.6f}")
        meanRow.append(f"{mean(df[title]):.6f}")
        stdRow.append(f"{std(df[title]):.6f}")
        q1Row.append(f"{q1(df[title]):.6f}")
        q2Row.append(f"{q2(df[title]):.6f}")
        q3Row.append(f"{q3(df[title]):.6f}")
        minRow.append(f"{min(df[title]):.6f}")
        maxRow.append(f"{max(df[title]):.6f}")
        # print(title + 'count : ', count(df[title]))
        # print(title + ' mean : ', mean(df[title]))
    table.add_row(countRow)
    table.add_row(meanRow)
    table.add_row(stdRow)
    table.add_row(minRow)
    table.add_row(q1Row)
    table.add_row(q2Row)
    table.add_row(q3Row)
    table.add_row(maxRow)
    print(table)

