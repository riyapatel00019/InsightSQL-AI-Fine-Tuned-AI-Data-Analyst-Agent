from app.pipeline.pipeline import answer_question


def test_pipeline():

    question = "How many customers are there in each state?"

    result = answer_question(question)

    print()
    print("=" * 60)
    print("QUESTION")
    print("=" * 60)
    print(result["question"])

    print()
    print("=" * 60)
    print("QUERY UNDERSTANDING")
    print("=" * 60)
    print(result["understanding"])

    print()
    print("=" * 60)
    print("GENERATED SQL")
    print("=" * 60)
    print(result["sql"])

    print()
    print("=" * 60)
    print("STATUS")
    print("=" * 60)
    print(result["success"])

    if result["success"]:

        print()
        print("=" * 60)
        print("COLUMNS")
        print("=" * 60)
        print(result["columns"])

        print()
        print("=" * 60)
        print("RESULTS")
        print("=" * 60)

        for row in result["rows"]:
            print(row)

        print()
        print("=" * 60)
        print("ANALYSIS")
        print("=" * 60)
        print(result["analysis"])

        print()
        print("=" * 60)
        print("CHART")
        print("=" * 60)
        print(result["chart"])

        print()
        print("=" * 60)
        print("INSIGHT")
        print("=" * 60)
        print(result["insight"])

    else:

        print()
        print("=" * 60)
        print("ERROR")
        print("=" * 60)
        print(result["error"])


if __name__ == "__main__":
    test_pipeline()