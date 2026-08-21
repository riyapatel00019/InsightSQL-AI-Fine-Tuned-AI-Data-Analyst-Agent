from app.llm.sql_generator import generate_sql


schema = """
TABLE customers
    customer_id INTEGER
    customer_name VARCHAR
    city VARCHAR
    state VARCHAR

TABLE products
    product_id INTEGER
    product_name VARCHAR
    category VARCHAR
    price NUMERIC

TABLE orders
    order_id INTEGER
    customer_id INTEGER
    order_date DATE
    status VARCHAR

TABLE order_items
    order_item_id INTEGER
    order_id INTEGER
    product_id INTEGER
    quantity INTEGER
    unit_price NUMERIC
"""


question = "Show all customers."


print("\nGenerating SQL...\n")

sql = generate_sql(
    question,
    schema
)

print("Generated SQL:")
print(sql)