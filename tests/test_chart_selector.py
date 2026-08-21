from app.visualization.chart_selector import select_chart

from datetime import date
def run_test(name, columns, rows):

    print("\n" + "=" * 60)
    print(name)
    print("=" * 60)

    result = select_chart(
        columns,
        rows
    )

    print("COLUMNS:")
    print(columns)

    print("\nROWS:")
    print(rows)

    print("\nCHART DECISION:")
    print(result)


# ------------------------------------------
# TEST 1
# Single value
# ------------------------------------------

run_test(
    "TEST 1 - Average Price",

    ["average_price"],

    [
        (19200.0,)
    ]
)


# ------------------------------------------
# TEST 2
# Category + numeric
# ------------------------------------------

run_test(
    "TEST 2 - Customers By State",

    ["state", "customer_count"],

    [
        ("Gujarat", 2),
        ("Delhi", 1),
        ("Maharashtra", 2)
    ]
)


# ------------------------------------------
# TEST 3
# Date + numeric
# ------------------------------------------

run_test(
    "TEST 3 - Sales Over Time",

    ["order_date", "sales"],

    [
        (date(2025, 1, 1), 10000),
        (date(2025, 2, 1), 15000),
        (date(2025, 3, 1), 12000)
    ]
)