from app.query.query_understanding import understand_query

from app.llm.schema_grounding import ground_schema

from app.database.schema import get_schema

from app.analysis.response_generator import generate_response

from app.llm.sql_generator import generate_sql

from app.sql.validator import validate_sql
from app.sql.schema_validator import validate_schema

from app.database.executor import execute_query

from app.analysis.result_analyzer import analyze_result

from app.visualization.chart_selector import select_chart
from app.visualization.chart_generator import generate_chart

from app.insights.insight_generator import generate_insight


MAX_RETRIES = 3


def answer_question(question: str):

    # ==========================================================
    # STEP 1: QUERY UNDERSTANDING
    # ==========================================================

    understanding = understand_query(question)

    # ==========================================================
    # STEP 2: GET DATABASE SCHEMA
    # ==========================================================

    schema = get_schema()

    # ==========================================================
    # STEP 3: SCHEMA GROUNDING
    # ==========================================================

    schema_text = ground_schema(
        question,
        schema
    )

    # ==========================================================
    # STEP 4: SQL GENERATION + VALIDATION + REPAIR
    # ==========================================================

    previous_sql = None
    previous_error = None

    result = None
    sql = None

    for attempt in range(1, MAX_RETRIES + 1):

        print()
        print("=" * 60)
        print(f"SQL GENERATION ATTEMPT {attempt}/{MAX_RETRIES}")
        print("=" * 60)

        # ------------------------------------------------------
        # Generate SQL
        # ------------------------------------------------------

        sql = generate_sql(
            question=question,
            schema=schema_text,
            previous_sql=previous_sql,
            previous_error=previous_error
        )

        print()
        print("GENERATED SQL:")
        print(sql)

        # ------------------------------------------------------
        # SQL VALIDATION
        # ------------------------------------------------------

        valid, message = validate_sql(sql)

        if not valid:

            print()
            print("SQL VALIDATION FAILED:")
            print(message)

            previous_sql = sql
            previous_error = message

            continue

        print()
        print("SQL VALIDATION:")
        print("PASSED")

        # ------------------------------------------------------
        # SCHEMA VALIDATION
        # ------------------------------------------------------

        schema_valid, schema_message = validate_schema(sql)

        if not schema_valid:

            print()
            print("SCHEMA VALIDATION FAILED:")
            print(schema_message)

            previous_sql = sql
            previous_error = schema_message

            continue

        print()
        print("SCHEMA VALIDATION:")
        print("PASSED")

        # ------------------------------------------------------
        # SQL EXECUTION
        # ------------------------------------------------------

        try:

            print()
            print("=" * 60)
            print("EXECUTING SQL")
            print("=" * 60)

            result = execute_query(sql)

            print("SQL execution successful.")

            break

        except Exception as error:

            print()
            print("SQL EXECUTION FAILED:")
            print(error)

            previous_sql = sql
            previous_error = str(error)

    # ==========================================================
    # STEP 5: IF SQL FAILED
    # ==========================================================

    if result is None:

        return {
            "question": question,
            "understanding": understanding,
            "sql": previous_sql,
            "success": False,
            "error": (
                f"SQL generation failed after "
                f"{MAX_RETRIES} attempts. "
                f"Last error: {previous_error}"
            ),
            "columns": [],
            "rows": [],
            "analysis": None,
            "chart": None,
            "insight": None,
            "response": None
        }

    # ==========================================================
    # STEP 6: RESULT ANALYSIS
    # ==========================================================

    analysis = analyze_result(
        result["columns"],
        result["rows"]
    )

    # ==========================================================
    # STEP 7: CHART SELECTION
    # ==========================================================

    chart_decision = select_chart(
        result["columns"],
        result["rows"]
    )

    # ==========================================================
    # STEP 8: CHART GENERATION
    # ==========================================================

    chart_path = None

    if chart_decision["chart_required"]:

        chart_path = generate_chart(
            columns=result["columns"],
            rows=result["rows"],
            chart_decision=chart_decision
        )

    # ==========================================================
    # STEP 9: BUILD CHART OBJECT
    # ==========================================================

    chart = {
        "required": chart_decision["chart_required"],
        "type": chart_decision["chart_type"],
        "x_column": chart_decision["x_column"],
        "y_columns": chart_decision["y_columns"],
        "path": chart_path
    }

    # ==========================================================
    # STEP 10: INSIGHT GENERATION
    # ==========================================================

    insight = generate_insight(
        question,
        result["columns"],
        result["rows"]
    )

    # ==========================================================
    # STEP 11: NATURAL LANGUAGE RESPONSE
    # ==========================================================

    response = generate_response(
        question=question,
        insight=insight,
        chart=chart
    )

    # ==========================================================
    # STEP 12: FINAL RESPONSE
    # ==========================================================

    return {
        "question": question,

        "understanding": understanding,

        "sql": sql,

        "success": True,

        "error": None,

        "columns": result["columns"],

        "rows": result["rows"],

        "analysis": analysis,

        "chart": chart,

        "insight": insight,

        "response": response
    }