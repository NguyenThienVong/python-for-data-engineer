import sqlite3
import pandas as pd

orders = pd.read_parquet("data/orders_clean.parquet")
orders["order_date"] = orders["order_date"].dt.strftime("%Y-%m-%d")
rows = list(orders.itertuples(index=False, name=None))

con = sqlite3.connect("data/shop.db")
con.execute("""
CREATE TABLE IF NOT EXISTS orders(
    order_id INTEGER PRIMARY KEY,
    order_date TEXT NOT NULL,
    city TEXT NOT NULL,
    product_id TEXT NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL
)""")

with con:
    con.executemany("""
        INSERT INTO orders VALUES (?,?,?,?,?,?)
        ON CONFLICT (order_id) DO UPDATE SET
           quantity = excluded.quantity, unit_price = excluded.unit_price
""", rows)

count = con.execute("select COUNT(*) FROM orders").fetchone()[0]
print("orders in database", count)


city = "Lahore"
top = con.execute(
    "SELECT order_date, ROUND(SUM(quantity * unit_price), 2) AS revenue "
    "FROM orders WHERE city = ? "
    "GROUP BY order_date ORDER BY revenue DESC LIMIT 3",
    (city,),
).fetchall()
print("Best days in", city, top)

df = pd.read_sql("SELECT city, COUNT(*) AS n FROM orders GROUP BY city", con)
print(df)
con.close()