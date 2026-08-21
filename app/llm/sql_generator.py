import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "distil-labs/distil-qwen3-0.6b-text2sql"


print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

print("Loading model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
)

model.eval()

print("Model loaded successfully!")


def generate_sql(question: str, schema: str) -> str:

    prompt = f"""You are a PostgreSQL Text-to-SQL assistant.

Your task is to convert the user's question into ONE correct SQL SELECT query.

DATABASE SCHEMA:

{schema}

RULES:

1. Return ONLY one SQL query.
2. Do not explain the query.
3. Do not add unnecessary subqueries.
4. If the user asks to show all rows from a table, use SELECT *.
5. Use only tables and columns that exist in the schema.
6. Use JOINs only when the schema supports the relationship.
7. The SQL must be valid PostgreSQL.
8. Do not invent columns.
9. Do not invent tables.

USER QUESTION:

{question}

SQL:
"""

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=128,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_tokens = outputs[0][
        inputs["input_ids"].shape[1]:
    ]

    generated_text = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    ).strip()

    generated_text = generated_text.replace(
        "```sql",
        ""
    )

    generated_text = generated_text.replace(
        "```",
        ""
    )

    if ";" in generated_text:

        generated_text = (
            generated_text.split(";")[0] + ";"
        )

    return generated_text.strip()