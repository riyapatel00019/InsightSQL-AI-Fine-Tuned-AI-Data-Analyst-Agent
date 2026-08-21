from typing import Any


def _to_number(value: Any):
    """
    Convert numeric database values to float.
    Return None if the value is not numeric.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def generate_insight(question, columns, rows):
    """
    Generate a simple business insight from SQL results.

    Parameters:
        question: Original user question
        columns: Result column names
        rows: SQL result rows

    Returns:
        Human-readable insight
    """

    if not rows:
        return "No data was found for this question."

    # Convert rows into dictionaries
    data = []

    for row in rows:
        record = {}

        for column, value in zip(columns, row):
            record[column] = value

        data.append(record)

    # Single-value result
    if len(data) == 1 and len(columns) == 1:

        value = data[0][columns[0]]

        return (
            f"The result for your question is {value}."
        )

    # Grouped result
    if len(data) > 1 and len(columns) >= 2:

        first_column = columns[0]
        second_column = columns[1]

        values = []

        for record in data:

            value = record[second_column]

            if isinstance(value, (int, float)):

                values.append(
                    (
                        record[first_column],
                        value
                    )
                )

        if values:

            highest = max(
                values,
                key=lambda x: x[1]
            )

            lowest = min(
                values,
                key=lambda x: x[1]
            )

            return (
                f"The highest value is {highest[1]} "
                f"for {first_column} '{highest[0]}'. "
                f"The lowest value is {lowest[1]} "
                f"for {first_column} '{lowest[0]}'."
            )

    return (
        f"The query returned {len(data)} rows."
    )