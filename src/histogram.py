import sys

import matplotlib.pyplot as plt
import pandas as pd

from parser import read, getNumericalValues
from stats import count, mean, std, q1, q2, q3, min, max

if __name__ == "__main__":

    filename = "dataset_train.csv"

    try:
        df = read(filename)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    if df.empty or len(df.columns) == 0:
        print("error: no numerical columns to describe", file=sys.stderr)
        sys.exit(1)

    scoreByHousesByCourse = {}

    courses = getNumericalValues(df).columns

    for _, row in df.iterrows():
        house = row["Hogwarts House"]
        for course in courses:
            grade = row[course]
            if pd.isna(grade):
                continue
            scoreByHousesByCourse.setdefault(house, {}).setdefault(course, []).append(grade)

    houses = list(scoreByHousesByCourse.keys())
    colors = {
        "Gryffindor": "#AE0001",
        "Slytherin": "#2A623D",
        "Ravenclaw": "#222F5B",
        "Hufflepuff": "#FFDB00",
    }

    cols = 4
    rows = -(-len(courses) // cols)  # ceil division
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
    axes = axes.flatten()

    for ax, course in zip(axes, courses):
        for house in houses:
            grades = scoreByHousesByCourse[house].get(course, [])
            ax.hist(grades, bins=20, alpha=0.5, label=house,
                    color=colors.get(house))
        ax.set_title(course, fontsize=9)
        ax.tick_params(labelsize=7)

    # Hide any unused subplots.
    for ax in axes[len(courses):]:
        ax.set_visible(False)

    # One shared legend for the whole figure.
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right")

    fig.tight_layout()
    fig.savefig("histogram.png", dpi=100)
    print("saved histogram.png")
