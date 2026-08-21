import re


def ground_schema(question: str, schema: dict) -> str:
    """
    Select the most relevant tables/columns from the database schema.

    This is generic and does not contain question-specific SQL rules.
    """

    question_lower = question.lower()

    scored_tables = []

    for table_name, columns in schema.items():

        score = 0

        # Table-name relevance
        if table_name.lower() in question_lower:
            score += 5

        # Column-name relevance
        for column in columns:

            column_name = column["column"].lower()

            if column_name in question_lower:
                score += 3

            # Match individual words
            words = re.findall(
                r"[a-zA-Z_]+",
                column_name
            )

            for word in words:
                if len(word) > 2 and word in question_lower:
                    score += 1

        scored_tables.append(
            (score, table_name)
        )

    # Highest relevance first
    scored_tables.sort(
        reverse=True
    )

    # Keep relevant tables
    selected_tables = [
        table_name
        for score, table_name in scored_tables
        if score > 0
    ]

    # If nothing matched, provide complete schema
    if not selected_tables:
        selected_tables = list(schema.keys())

    lines = []

    for table_name in selected_tables:

        lines.append(
            f"TABLE: {table_name}"
        )

        for column in schema[table_name]:

            lines.append(
                f"  {column['column']} "
                f"({column['type']})"
            )

        lines.append("")

    return "\n".join(lines)