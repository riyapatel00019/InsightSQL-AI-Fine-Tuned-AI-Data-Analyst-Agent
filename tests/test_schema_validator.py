from app.sql.schema_validator import validate_schema


def test_schema_validator():

    tests = [

        (
            "VALID SIMPLE",
            """
            SELECT *
            FROM customers;
            """
        ),

        (
            "VALID WHERE",
            """
            SELECT *
            FROM customers
            WHERE state = 'Gujarat';
            """
        ),

        (
            "VALID ALIAS",
            """
            SELECT c.state, COUNT(*)
            FROM customers c
            GROUP BY c.state;
            """
        ),

        (
            "VALID JOIN",
            """
            SELECT
                c.customer_name,
                o.order_date,
                o.status
            FROM customers c
            LEFT JOIN orders o
                ON c.customer_id = o.customer_id;
            """
        ),

        (
            "VALID AVG",
            """
            SELECT AVG(price)
            FROM products;
            """
        ),

        (
            "INVALID COLUMN",
            """
            SELECT AVG(product_price)
            FROM products;
            """
        ),

        (
            "INVALID TABLE",
            """
            SELECT *
            FROM customer_data;
            """
        ),

    ]

    for name, sql in tests:

        print()
        print("=" * 60)
        print(name)
        print("=" * 60)

        valid, message = validate_schema(sql)

        print("SQL:")
        print(sql)

        print("RESULT:")
        print(valid, message)


if __name__ == "__main__":
    test_schema_validator()