def generate_response(
    question,
    insight,
    chart
):
    """
    Create the final user-facing response.
    """

    return {
        "question": question,
        "answer": insight,
        "chart": chart
    }