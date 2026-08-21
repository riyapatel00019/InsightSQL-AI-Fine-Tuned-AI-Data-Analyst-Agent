from app.sql.validator import validate_sql


def test_valid_sql():

    sql = "SELECT * FROM customers;"

    valid, message = validate_sql(sql)

    print("\nValid SQL test:")
    print(valid)
    print(message)

    assert valid is True


def test_invalid_sql():

    sql = "DROP TABLE customers;"

    valid, message = validate_sql(sql)

    print("\nDangerous SQL test:")
    print(valid)
    print(message)

    assert valid is False


if __name__ == "__main__":

    test_valid_sql()

    test_invalid_sql()