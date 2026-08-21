import sqlglot


def validate_sql(sql: str) -> tuple[bool, str]:

    if not sql or not sql.strip():
        return False, "SQL query is empty."

    sql = sql.strip()

    # Only allow SELECT statements
    if not sql.upper().startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    # Block dangerous SQL keywords
    forbidden_keywords = [
        "DROP",
        "DELETE",
        "UPDATE",
        "INSERT",
        "ALTER",
        "TRUNCATE",
        "CREATE",
        "GRANT",
        "REVOKE",
    ]

    sql_upper = sql.upper()

    for keyword in forbidden_keywords:

        if keyword in sql_upper:
            return False, f"Forbidden SQL operation: {keyword}"

    # Parse SQL
    try:

        parsed = sqlglot.parse_one(
            sql,
            dialect="postgres"
        )

    except Exception as error:

        return False, f"Invalid SQL syntax: {error}"

    # Make sure it is actually a SELECT
    if parsed is None:

        return False, "Unable to parse SQL."

    return True, "SQL is valid."