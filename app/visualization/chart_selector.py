from datetime import date, datetime
from decimal import Decimal


def is_numeric(value):
    """
    Check whether a value is numeric.
    """

    return isinstance(
        value,
        (int, float, Decimal)
    ) and not isinstance(value, bool)


def is_date_value(value):
    """
    Check whether a value is a date or datetime.
    """

    return isinstance(
        value,
        (date, datetime)
    )


def select_chart(columns, rows):
    """
    Dynamically select the most appropriate chart
    based on query result structure.

    Returns:
        {
            "chart_required": bool,
            "chart_type": str | None,
            "x_column": str | None,
            "y_columns": list,
            "reason": str
        }
    """

    # ------------------------------------------
    # No result
    # ------------------------------------------

    if not rows:

        return {
            "chart_required": False,
            "chart_type": None,
            "x_column": None,
            "y_columns": [],
            "reason": "No data available for visualization."
        }

    # ------------------------------------------
    # One-row / one-column result
    # ------------------------------------------

    if len(rows) == 1 and len(columns) == 1:

        return {
            "chart_required": False,
            "chart_type": None,
            "x_column": None,
            "y_columns": [],
            "reason": "Single value result does not require a chart."
        }

    # ------------------------------------------
    # Analyze columns
    # ------------------------------------------

    first_row = rows[0]

    numeric_columns = []
    date_columns = []
    categorical_columns = []

    for index, value in enumerate(first_row):

        column = columns[index]

        if is_numeric(value):

            numeric_columns.append(column)

        elif is_date_value(value):

            date_columns.append(column)

        else:

            categorical_columns.append(column)

    # ------------------------------------------
    # Date + numeric
    # → Line chart
    # ------------------------------------------

    if date_columns and numeric_columns:

        return {
            "chart_required": True,
            "chart_type": "line",
            "x_column": date_columns[0],
            "y_columns": numeric_columns,
            "reason": "Date and numeric columns detected."
        }

    # ------------------------------------------
    # Category + numeric
    # → Bar chart
    # ------------------------------------------

    if categorical_columns and numeric_columns:

        return {
            "chart_required": True,
            "chart_type": "bar",
            "x_column": categorical_columns[0],
            "y_columns": numeric_columns,
            "reason": "Categorical and numeric columns detected."
        }

    # ------------------------------------------
    # Multiple numeric columns
    # → Bar chart
    # ------------------------------------------

    if len(numeric_columns) >= 2:

        return {
            "chart_required": True,
            "chart_type": "bar",
            "x_column": None,
            "y_columns": numeric_columns,
            "reason": "Multiple numeric columns detected."
        }

    # ------------------------------------------
    # Nothing suitable
    # ------------------------------------------

    return {
        "chart_required": False,
        "chart_type": None,
        "x_column": None,
        "y_columns": [],
        "reason": "No suitable chart structure detected."
    }