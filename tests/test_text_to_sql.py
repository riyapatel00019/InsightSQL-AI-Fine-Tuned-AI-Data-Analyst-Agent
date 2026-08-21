from app.database.schema import (
    get_schema,
    format_schema
)

from app.llm.sql_generator import (
    generate_sql
)


def test_text_to_sql():

    # 1. Get real schema
    schema = get_schema()

    # 2. Convert schema to text
    schema_text = format_schema(schema)

    print("\n========== DATABASE SCHEMA ==========\n")
    print(schema_text)

    # 3. User question
    question = "Show all customers."

    print("\n========== QUESTION ==========\n")
    print(question)

    # 4. Generate SQL
    sql = generate_sql(
        question,
        schema_text
    )

    print("\n========== GENERATED SQL ==========\n")
    print(sql)


if __name__ == "__main__":
    test_text_to_sql()