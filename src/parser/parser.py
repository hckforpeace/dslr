import numpy as np
import pandas as pd

HOUSE_COLUMN = "Hogwarts House"


class Parser:
    """Read a dataset once and expose it as a dataframe and a numpy matrix.

    Everything is computed by the constructor and kept as attributes:

        df          the full cleaned frame, string columns included
        numericals  the numerical columns only (the courses)
        courses     the course names, in matrix row order
        matrix      the grades as floats, shaped (n_courses, n_students)
        houses      the Hogwarts House of every student, or None when the
                    dataset has no such column (the test set does not)
    """

    def __init__(self, filePath: str):
        self.filePath = filePath
        self.df = self.read()
        self.numericals = self.getNumericalValues()
        self.courses = list(self.numericals.columns)
        self.matrix = self.toNumpy()
        self.houses = self.getHouses()

    def read(self):
        """Load the CSV, drop empty columns and the Index column."""
        try:
            unparsed_data = pd.read_csv(self.filePath)
        except FileNotFoundError:
            raise FileNotFoundError(f"no such file: {self.filePath}")
        except PermissionError:
            raise PermissionError(f"cannot read file: {self.filePath}")
        except pd.errors.EmptyDataError:
            raise ValueError(f"file is empty: {self.filePath}")
        except (pd.errors.ParserError, UnicodeDecodeError) as e:
            raise ValueError(f"could not parse {self.filePath} as CSV: {e}")

        cleaned = unparsed_data.dropna(axis=1, how="all")
        cleaned = cleaned.drop(columns="Index", errors="ignore")
        if cleaned.empty:
            raise ValueError(f"no usable data in {self.filePath}")
        return cleaned

    def getNumericalValues(self):
        """Return the numerical columns of the frame."""
        return self.df.select_dtypes(include="number")

    def toNumpy(self):
        """Return the grades as a matrix, transposed to (courses, students).

        Rows are courses, not students: matrix[i] holds every grade of
        courses[i], which is exactly what one plot per course needs.
        """
        return self.numericals.to_numpy(dtype=float).T

    def getHouses(self):
        """Return the house of every student, or None if the column is absent."""
        if HOUSE_COLUMN not in self.df.columns:
            return None
        return self.df[HOUSE_COLUMN].to_numpy()

    def uniqueHouses(self):
        """Return the houses present in the dataset, sorted alphabetically."""
        if self.houses is None:
            return []
        return sorted({house for house in self.houses if pd.notna(house)})

    def gradesFor(self, course: str, house: str | None = None):
        """Return the grades of a course, without the missing ones.

        With a house, only the students of that house are kept.
        """
        if course not in self.courses:
            raise ValueError(f"no such course: {course}")

        grades = self.matrix[self.courses.index(course)]
        if house is not None:
            if self.houses is None:
                raise ValueError(f"no {HOUSE_COLUMN} column in {self.filePath}")
            grades = grades[self.houses == house]
        return grades[~np.isnan(grades)]
