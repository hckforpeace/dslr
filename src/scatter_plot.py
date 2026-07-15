import sys

import matplotlib.pyplot as plt

from parser import read, getNumericalValues


def sanitize(name):
    """Make a course name safe to use in a filename."""
    return "".join(c if c.isalnum() else "_" for c in name)


if __name__ == "__main__":

    filename = "dataset_train.csv"

    try:
        df = read(filename)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(1)

    if df.empty or len(df.columns) == 0:
        print("error: no numerical columns to plot", file=sys.stderr)
        sys.exit(1)

    numericals = getNumericalValues(df)
    courses = numericals.columns

    if len(courses) < 2:
        print("error: need at least two numerical columns to plot", file=sys.stderr)
        sys.exit(1)

    # One image per base feature: it holds a subplot of that base against
    # every other feature (x vs y, x vs z, ...).
    for base in courses:
        others = [c for c in courses if c != base]

        cols = 4
        rows = -(-len(others) // cols)  # ceil division
        fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 3))
        axes = axes.flatten()

        for ax, other in zip(axes, others):
            ax.scatter(numericals[base], numericals[other], s=2, alpha=0.4)
            ax.set_xlabel(base, fontsize=8)
            ax.set_ylabel(other, fontsize=8)
            ax.set_title(f"{base} vs {other}", fontsize=9)
            ax.tick_params(labelsize=7)

        # Hide any unused subplots.
        for ax in axes[len(others):]:
            ax.set_visible(False)

        fig.suptitle(base, fontsize=12)
        fig.tight_layout()
        outfile = f"scatter_plot_{sanitize(base)}.png"
        fig.savefig(outfile, dpi=100)
        plt.close(fig)
        print(f"saved {outfile}")
