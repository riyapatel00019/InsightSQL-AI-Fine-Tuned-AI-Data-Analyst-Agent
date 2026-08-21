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


def generate_sql(
    question: str,
    schema: str,
    previous_sql: str = None,
    previous_error: str = None
) -> str:

    repair_context = ""

    if previous_sql and previous_error:
        repair_context = f"""
PREVIOUS SQL:
{previous_sql}

PREVIOUS ERROR:
{previous_error}

The previous SQL was incorrect.

Generate a corrected SQL query.

IMPORTANT:
- Carefully compare the previous SQL with the database schema.
- Use the exact table and column names from the schema.
- Do not invent column names.
- Do not repeat the previous mistake.
"""

    prompt = f"""You are a PostgreSQL Text-to-SQL assistant.

Convert the user's question into ONE correct PostgreSQL SELECT query.

DATABASE SCHEMA:

{schema}

RULES:

1. Return ONLY one SQL query.
2. Do not explain the query.
3. Use only tables from the schema.
4. Use only columns from the schema.
5. Never invent a column.
6. Never invent a table.
7. Use JOINs only when relationships exist in the schema.
8. Use valid PostgreSQL syntax.
9. For "show all" questions, use SELECT * when appropriate.
10. Carefully identify the correct column from the schema.

{repair_context}

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