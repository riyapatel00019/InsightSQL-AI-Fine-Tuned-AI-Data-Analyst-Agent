from app.visualization.chart_generator import generate_chart


def test_bar_chart():

    columns = [
        "state",
        "customer_count"
    ]

    rows = [
        ("Gujarat", 2),
        ("Delhi", 1),
        ("Maharashtra", 2)
    ]

    chart_decision = {
        "chart_required": True,
        "chart_type": "bar",
        "x_column": "state",
        "y_columns": ["customer_count"],
        "reason": "Categorical and numeric columns detected."
    }

    path = generate_chart(
        columns,
        rows,
        chart_decision
    )

    print()
    print("==============================")
    print("CHART GENERATOR TEST")
    print("==============================")
    print("CHART PATH:")
    print(path)

    assert path is not None


if __name__ == "__main__":
    test_bar_chart()