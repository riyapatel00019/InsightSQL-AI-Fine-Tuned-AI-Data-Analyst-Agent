import json

from app.pipeline.pipeline import answer_question


DATASET_PATH = "data/evaluation/sql_capability_tests.json"


def load_questions():

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def run_tests():

    questions = load_questions()

    total = len(questions)
    successful = 0
    failed = 0

    print("=" * 70)
    print("SQL CAPABILITY TEST")
    print("=" * 70)

    for test in questions:

        question_id = test["id"]
        category = test["category"]
        question = test["question"]

        print("\n" + "=" * 70)
        print(f"TEST ID   : {question_id}")
        print(f"CATEGORY   : {category}")
        print(f"QUESTION   : {question}")
        print("=" * 70)

        try:

            result = answer_question(question)

            print("\nGENERATED SQL:")
            print(result["sql"])

            print("\nSUCCESS:")
            print(result["success"])

            if result["success"]:
                successful += 1

                print("\nRESULT:")
                for row in result["rows"][:5]:
                    print(row)

            else:
                failed += 1

                print("\nERROR:")
                print(result.get("error"))

        except Exception as error:

            failed += 1

            print("\nPIPELINE ERROR:")
            print(error)

    print("\n")
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"Total tests : {total}")
    print(f"Successful  : {successful}")
    print(f"Failed      : {failed}")

    if total > 0:

        accuracy = (successful / total) * 100

        print(f"Success rate: {accuracy:.2f}%")


if __name__ == "__main__":
    run_tests()