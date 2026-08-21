import re


def understand_query(question: str):

    question_lower = question.lower()

    result = {
        "original_question": question,
        "intent": "unknown",
        "table": None,
        "limit": None,
        "aggregation": None,
        "sort": None,
        "filters": []
    }

    # -------------------------
    # Detect table
    # -------------------------

    if "customer" in question_lower:
        result["table"] = "customers"

    elif "product" in question_lower:
        result["table"] = "products"

    elif "order item" in question_lower:
        result["table"] = "order_items"

    elif "order" in question_lower:
        result["table"] = "orders"

    # -------------------------
    # Detect intent
    # -------------------------

    if "how many" in question_lower or "count" in question_lower:

        result["intent"] = "count"
        result["aggregation"] = "COUNT"

    elif "average" in question_lower or "avg" in question_lower:

        result["intent"] = "average"
        result["aggregation"] = "AVG"

    elif "total" in question_lower or "sum" in question_lower:

        result["intent"] = "sum"
        result["aggregation"] = "SUM"

    elif (
        "most expensive" in question_lower
        or "highest price" in question_lower
        or "most costly" in question_lower
    ):

        result["intent"] = "ranking"

        result["sort"] = {
            "direction": "DESC",
            "column": "price"
        }

    elif (
        "cheapest" in question_lower
        or "lowest price" in question_lower
    ):

        result["intent"] = "ranking"

        result["sort"] = {
            "direction": "ASC",
            "column": "price"
        }

    elif (
        "show" in question_lower
        or "list" in question_lower
        or "display" in question_lower
    ):

        result["intent"] = "select"

    # -------------------------
    # Detect LIMIT
    # -------------------------

    match = re.search(r"\b(\d+)\b", question_lower)

    if match:
        result["limit"] = int(match.group(1))

    # -------------------------
    # Detect Gujarat filter
    # -------------------------

    if "gujarat" in question_lower:

        result["filters"].append({
            "column": "state",
            "operator": "=",
            "value": "Gujarat"
        })

    return result