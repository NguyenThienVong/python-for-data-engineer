import csv
from collections import Counter

cities = Counter()
revenue = 0.0
bad = 0
with open("data/orders.csv", newline="") as f:
    for row in csv.DictReader(f):
        cities[row["city"]] += 1
        try:
            revenue += int(row["quantity"]) * float(row["unit_price"])
        except ValueError:
            bad += 1

print("rows per city:", cities.most_common(7))
print(f"Revenue: {revenue:.2f}")
print("Rows with bad data:", bad)