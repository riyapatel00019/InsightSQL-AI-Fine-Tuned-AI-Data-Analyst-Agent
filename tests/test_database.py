from app.database.connection import get_connection


def test_connection():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("SELECT 1;")

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    assert result[0] == 1

    print("Database connection successful!")


if __name__ == "__main__":
    test_connection()