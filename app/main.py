from app.database.schema import get_schema
from app.database.executor import execute_query
from app.llm.sql_generator import generate_sql
from app.sql.validator import validate_sql


def format_schema(schema):

    text = ""

    for table, columns in schema.items():

        text += f"\nTABLE: {table}\n"

        for column in columns:

            text += (
                f"  {column['column']} "
                f"({column['type']})\n"
            )

    return text


def main():

    print("=" * 60)
    print("       InsightSQL AI - Text-to-SQL")
    print("=" * 60)

    question = input(
        "\nAsk your database question: "
    )

    # ----------------------------------
    # 1. Get database schema
    # ----------------------------------

    schema = get_schema()

    schema_text = format_schema(schema)

    print("\n[1] Schema retrieved")

    # ----------------------------------
    # 2. Generate SQL
    # ----------------------------------

    sql = generate_sql(
        question,
        schema_text
    )

    print("\n[2] Generated SQL:")
    print(sql)

    # ----------------------------------
    # 3. Validate SQL
    # ----------------------------------

    is_valid, message = validate_sql(sql)

    if not is_valid:

        print("\nSQL validation failed:")
        print(message)

        return

    print("\n[3] SQL validation successful")

    # ----------------------------------
    # 4. Execute SQL
    # ----------------------------------

    try:

        result = execute_query(sql)

        print("\n[4] Query Result:")

        for row in result:

            print(row)

    except Exception as e:

        print("\nDatabase execution error:")
        print(e)


if __name__ == "__main__":
    main()