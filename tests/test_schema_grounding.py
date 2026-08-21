from app.database.schema import get_schema
from app.llm.schema_grounding import ground_schema


questions = [
    "What is the average product price?",
    "How many customers are there?",
    "Show customers and their orders."
]


schema = get_schema()


for question in questions:

    print()
    print("=" * 60)
    print("QUESTION")
    print("=" * 60)

    print(question)

    print()
    print("GROUNDED SCHEMA")
    print("=" * 60)

    result = ground_schema(
        question,
        schema
    )

    print(result)