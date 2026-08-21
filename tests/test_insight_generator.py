from app.insights.insight_generator import generate_insight


def test_average():

    columns = ["average_price"]

    rows = [
        (19200.0,)
    ]

    insight = generate_insight(
        question="What is the average product price?",
        columns=columns,
        rows=rows
    )

    print()
    print("==============================")
    print("INSIGHT TEST - AVERAGE")
    print("==============================")
    print(insight)

    assert insight


def test_grouped_result():

    columns = [
        "state",
        "customer_count"
    ]

    rows = [
        ("Gujarat", 2),
        ("Delhi", 1),
        ("Maharashtra", 2)
    ]

    insight = generate_insight(
        question="How many customers are there in each state?",
        columns=columns,
        rows=rows
    )

    print()
    print("==============================")
    print("INSIGHT TEST - GROUPED")
    print("==============================")
    print(insight)

    assert insight


if __name__ == "__main__":

    test_average()
    test_grouped_result()