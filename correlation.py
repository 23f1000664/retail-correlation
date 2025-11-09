import sqlite3
import json
import math

# 1. Load SQL file and create database
db = sqlite3.connect(":memory:")
cursor = db.cursor()

with open("retail_data.sql", "r") as f:
    sql_script = f.read()
cursor.executescript(sql_script)

# 2. Define a function to compute Pearson correlation
def correlation(x_col, y_col):
    cursor.execute(f"SELECT {x_col}, {y_col} FROM retail_data WHERE {x_col} IS NOT NULL AND {y_col} IS NOT NULL")
    rows = cursor.fetchall()
    xs = [r[0] for r in rows]
    ys = [r[1] for r in rows]
    n = len(xs)
    if n == 0:
        return None

    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    den = math.sqrt(sum((xs[i] - mean_x)**2 for i in range(n)) * sum((ys[i] - mean_y)**2 for i in range(n)))
    return num / den if den != 0 else 0

# 3. Compute correlations
pairs = [
    ("Net_Sales", "Promo_Spend"),
    ("Net_Sales", "Returns"),
    ("Promo_Spend", "Returns")
]

results = []
for a, b in pairs:
    corr = correlation(a, b)
    results.append((f"{a}-{b}", corr))

# 4. Find the strongest correlation (by absolute value)
strongest_pair = max(results, key=lambda x: abs(x[1]))

# 5. Print JSON output
output = { "pair": strongest_pair[0], "correlation": round(strongest_pair[1], 4) }
print(json.dumps(output, indent=2))
