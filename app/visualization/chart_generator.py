import os
import matplotlib.pyplot as plt


def generate_chart(
    columns,
    rows,
    chart_decision,
    output_dir="outputs/charts"
):
    """
    Generate a chart from SQL query results.

    Parameters
    ----------
    columns : list
        Column names returned by SQL.

    rows : list
        SQL result rows.

    chart_decision : dict
        Output from chart_selector.

    output_dir : str
        Directory where the chart will be saved.

    Returns
    -------
    str or None
        Path of generated chart.
    """

    # -----------------------------------------
    # Check whether chart is required
    # -----------------------------------------

    if not chart_decision.get("chart_required"):
        return None

    chart_type = chart_decision.get("chart_type")
    x_column = chart_decision.get("x_column")
    y_columns = chart_decision.get("y_columns", [])

    if not rows:
        return None

    if not x_column or not y_columns:
        return None

    # -----------------------------------------
    # Find column indexes dynamically
    # -----------------------------------------

    if x_column not in columns:
        raise ValueError(
            f"X column '{x_column}' not found in result."
        )

    x_index = columns.index(x_column)

    y_indexes = []

    for column in y_columns:

        if column not in columns:
            raise ValueError(
                f"Y column '{column}' not found in result."
            )

        y_indexes.append(columns.index(column))

    # -----------------------------------------
    # Create output directory
    # -----------------------------------------

    os.makedirs(output_dir, exist_ok=True)

    # -----------------------------------------
    # Create figure
    # -----------------------------------------

    plt.figure(figsize=(10, 6))

    # -----------------------------------------
    # BAR CHART
    # -----------------------------------------

    if chart_type == "bar":

        x_values = [
            str(row[x_index])
            for row in rows
        ]

        for y_index in y_indexes:

            y_values = [
                float(row[y_index])
                for row in rows
            ]

            plt.bar(
                x_values,
                y_values
            )

        plt.xlabel(x_column)
        plt.ylabel(", ".join(y_columns))
        plt.title(
            f"{', '.join(y_columns)} by {x_column}"
        )

    # -----------------------------------------
    # LINE CHART
    # -----------------------------------------

    elif chart_type == "line":

        x_values = [
            str(row[x_index])
            for row in rows
        ]

        for y_index in y_indexes:

            y_values = [
                float(row[y_index])
                for row in rows
            ]

            plt.plot(
                x_values,
                y_values,
                marker="o",
                label=columns[y_index]
            )

        plt.xlabel(x_column)
        plt.ylabel(", ".join(y_columns))
        plt.title(
            f"{', '.join(y_columns)} over {x_column}"
        )

        if len(y_indexes) > 1:
            plt.legend()

    # -----------------------------------------
    # PIE CHART
    # -----------------------------------------

    elif chart_type == "pie":

        if len(y_indexes) != 1:
            raise ValueError(
                "Pie chart requires exactly one Y column."
            )

        y_index = y_indexes[0]

        labels = [
            str(row[x_index])
            for row in rows
        ]

        values = [
            float(row[y_index])
            for row in rows
        ]

        plt.pie(
            values,
            labels=labels,
            autopct="%1.1f%%"
        )

        plt.title(
            f"{y_columns[0]} distribution"
        )

    # -----------------------------------------
    # SCATTER CHART
    # -----------------------------------------

    elif chart_type == "scatter":

        if len(y_indexes) != 1:
            raise ValueError(
                "Scatter chart requires exactly one Y column."
            )

        y_index = y_indexes[0]

        x_values = [
            float(row[x_index])
            for row in rows
        ]

        y_values = [
            float(row[y_index])
            for row in rows
        ]

        plt.scatter(
            x_values,
            y_values
        )

        plt.xlabel(x_column)
        plt.ylabel(y_columns[0])

        plt.title(
            f"{y_columns[0]} vs {x_column}"
        )

    else:

        raise ValueError(
            f"Unsupported chart type: {chart_type}"
        )

    # -----------------------------------------
    # Improve layout
    # -----------------------------------------

    plt.xticks(rotation=45)
    plt.tight_layout()

    # -----------------------------------------
    # Create filename
    # -----------------------------------------

    filename = (
        f"{chart_type}_chart.png"
    )

    chart_path = os.path.join(
        output_dir,
        filename
    )

    # -----------------------------------------
    # Save chart
    # -----------------------------------------

    plt.savefig(
        chart_path,
        dpi=150,
        bbox_inches="tight"
    )

    plt.close()

    return chart_path