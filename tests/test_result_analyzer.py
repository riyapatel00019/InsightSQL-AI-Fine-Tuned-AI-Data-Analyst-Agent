from app.analysis.result_analyzer import analyze_result


columns = ["average_price"]

rows = [
    (19200.0,)
]

result = analyze_result(columns, rows)

print("\n==============================")
print("RESULT ANALYZER TEST")
print("==============================")

print("\nCOLUMNS:")
print(result["columns"])

print("\nROW COUNT:")
print(result["row_count"])

print("\nDATA:")
print(result["data"])