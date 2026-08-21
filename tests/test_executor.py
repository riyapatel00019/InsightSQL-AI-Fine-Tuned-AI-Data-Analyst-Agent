from app.database.executor import execute_query


def test_executor():

    sql = "SELECT * FROM customers LIMIT 5;"

    result = execute_query(sql)

    print("\n========== COLUMNS ==========")

    print(result["columns"])

    print("\n========== ROWS ==========")

    for row in result["rows"]:
        print(row)


if __name__ == "__main__":
    test_executor()