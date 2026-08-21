from app.database.connection import get_connection


def get_schema():

    connection = get_connection()

    try:

        cursor = connection.cursor()

        query = """
        SELECT
            table_name,
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position;
        """

        cursor.execute(query)

        rows = cursor.fetchall()

        schema = {}

        for table_name, column_name, data_type in rows:

            if table_name not in schema:
                schema[table_name] = []

            schema[table_name].append({
                "column": column_name,
                "type": data_type
            })

        cursor.close()

        return schema

    finally:
        connection.close()
def format_schema(schema):
    """
    Convert schema dictionary into text
    that can be provided to the LLM.
    """

    lines = []

    for table_name, columns in schema.items():

        lines.append(f"TABLE: {table_name}")

        for column in columns:

            lines.append(
                f"  {column['column']} "
                f"({column['type']})"
            )

        lines.append("")

    return "\n".join(lines)