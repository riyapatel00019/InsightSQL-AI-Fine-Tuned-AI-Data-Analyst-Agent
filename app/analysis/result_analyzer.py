from decimal import Decimal
from datetime import date, datetime


def _convert_value(value):
    """Convert PostgreSQL values into JSON-friendly Python values."""

    if isinstance(value, Decimal):
        return float(value)

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    return value


def analyze_result(columns, rows):
    """
    Convert database results into a structured format
    that can later be used for insights and charts.
    """

    data = []

    for row in rows:
        record = {}

        for column, value in zip(columns, row):
            record[column] = _convert_value(value)

        data.append(record)

    return {
        "columns": columns,
        "row_count": len(data),
        "data": data
    }