import sys

import matplotlib.pyplot as plt

from parser import Parser

COLORS = {
    "Gryffindor": "#AE0001",
    "Slytherin": "#2A623D",
    "Ravenclaw": "#222F5B",
    "Hufflepuff": "#FFDB00",
}

if __name__ == "__main__":

    datasetPath = "datasets/dataset_train.csv"

    try:
        data = Parser(datasetPath)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    if not data.courses:
        print("error: no numerical columns to plot", file=sys.stderr)
        sys.exit(1)

    if data.houses is None:
        print(f"error: {datasetPath} has no Hogwarts House column", file=sys.stderr)
        sys.exit(1)

    houses = data.uniqueHouses()

    cols = 4
    rows = -(-len(data.courses) // cols)  # ceil division
    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
    axes = axes.flatten()

    # The matrix is stored courses x students, so one subplot is one row of
    # it: gradesFor only has to mask that row by house.
    for ax, course in zip(axes, data.courses):
        for house in houses:
            ax.hist(data.gradesFor(course, house), bins=20, alpha=0.5,
                    label=house, color=COLORS.get(house))
        ax.set_title(course, fontsize=9)
        ax.tick_params(labelsize=7)

    # Hide any unused subplots.
    for ax in axes[len(data.courses):]:
        ax.set_visible(False)

    # One shared legend for the whole figure.
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right")

    fig.tight_layout()
    fig.savefig("./images/histogram/histogram.png", dpi=100)
    print("saved histogram.png")
