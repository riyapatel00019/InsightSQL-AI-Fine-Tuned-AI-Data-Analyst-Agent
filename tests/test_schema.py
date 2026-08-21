from app.database.schema import get_schema


def test_schema():

    schema = get_schema()

    print("\n========== DATABASE SCHEMA ==========\n")

    for table_name, columns in schema.items():

        print(f"TABLE: {table_name}")

        for column in columns:

            print(
                f"    {column['column']} "
                f"({column['type']})"
            )

        print()


if __name__ == "__main__":
    test_schema()