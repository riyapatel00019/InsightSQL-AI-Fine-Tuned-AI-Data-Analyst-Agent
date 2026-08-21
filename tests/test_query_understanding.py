from app.query.query_understanding import understand_query


def test_query_understanding():

    questions = [
        "Show all customers.",
        "How many customers are there?",
        "Show the 5 most expensive products.",
        "Show customers from Gujarat.",
        "What is the average product price?"
    ]

    for question in questions:

        result = understand_query(question)

        print("\nQUESTION:")
        print(question)

        print("\nUNDERSTANDING:")
        print(result)


if __name__ == "__main__":
    test_query_understanding()