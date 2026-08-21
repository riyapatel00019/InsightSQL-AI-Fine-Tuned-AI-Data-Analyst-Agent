import sqlglot
from sqlglot import exp

from app.database.schema import get_schema


def validate_schema(sql: str) -> tuple[bool, str]:

    if not sql or not sql.strip():
        return False, "SQL query is empty."

    # =====================================================
    # GET ACTUAL DATABASE SCHEMA
    # =====================================================

    schema = get_schema()

    database_schema = {}

    for table_name, columns in schema.items():

        database_schema[table_name.lower()] = {
            column["column"].lower()
            for column in columns
        }

    # =====================================================
    # PARSE SQL
    # =====================================================

    try:

        parsed = sqlglot.parse_one(
            sql,
            dialect="postgres"
        )

    except Exception as error:

        return False, f"Unable to parse SQL: {error}"

    # =====================================================
    # FIND TABLES
    # =====================================================

    tables = list(parsed.find_all(exp.Table))

    if not tables:

        return False, "No table found in SQL query."

    # =====================================================
    # VALIDATE TABLES + BUILD ALIAS MAP
    # =====================================================

    alias_to_table = {}

    for table in tables:

        table_name = table.name.lower()

        # ---------------------------------------------
        # Check whether table exists
        # ---------------------------------------------

        if table_name not in database_schema:

            return False, (
                f"Table '{table.name}' does not exist "
                f"in the database."
            )

        # ---------------------------------------------
        # Map table name to itself
        # ---------------------------------------------

        alias_to_table[table_name] = table_name

        # ---------------------------------------------
        # Get alias correctly
        # ---------------------------------------------

        alias = table.alias

        if alias:

            alias = str(alias).lower()

            alias_to_table[alias] = table_name

    # =====================================================
    # VALIDATE COLUMNS
    # =====================================================

    columns = list(parsed.find_all(exp.Column))

    for column in columns:

        column_name = column.name.lower()

        # Ignore *
        if column_name == "*":
            continue

        # =================================================
        # QUALIFIED COLUMN
        #
        # Example:
        # c.customer_id
        # =================================================

        if column.table:

            table_reference = str(
                column.table
            ).lower()

            # ---------------------------------------------
            # Check alias/table reference
            # ---------------------------------------------

            if table_reference not in alias_to_table:

                return False, (
                    f"Unknown table alias "
                    f"'{column.table}'."
                )

            real_table = alias_to_table[
                table_reference
            ]

            # ---------------------------------------------
            # Check column
            # ---------------------------------------------

            if column_name not in database_schema[
                real_table
            ]:

                return False, (
                    f"Column '{column.name}' does not "
                    f"exist in table '{real_table}'."
                )

        # =================================================
        # UNQUALIFIED COLUMN
        #
        # Example:
        # price
        # =================================================

        else:

            matching_tables = []

            for table_name, table_columns in (
                database_schema.items()
            ):

                if column_name in table_columns:

                    matching_tables.append(
                        table_name
                    )

            # ---------------------------------------------
            # Column doesn't exist anywhere
            # ---------------------------------------------

            if not matching_tables:

                return False, (
                    f"Column '{column.name}' does not "
                    f"exist in the database."
                )

            # ---------------------------------------------
            # Ambiguous column
            # ---------------------------------------------

            if len(matching_tables) > 1:

                return False, (
                    f"Column '{column.name}' is ambiguous. "
                    f"Use a table name or alias."
                )

    # =====================================================
    # SUCCESS
    # =====================================================

    return True, "Schema is valid."