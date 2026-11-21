import pandas as pd
from pathlib import Path


orders = pd.read_csv(
    "data/orders.csv",
    parse_dates=["order_date"]
)
print(orders.dtypes)
print(orders.head())


products = pd.DataFrame({
    "product_id":["P01","P02","P03","P04"],
    "product": ["Keyboard", "Mouse", "Monitor", "Webcam"]
})

orders["city"] = orders["city"].str.strip().str.title()
orders = orders.drop_duplicates()
orders = orders[orders["quantity"] > 0]
orders["revenue"] = orders["quantity"] * orders["unit_price"]
orders["month"] = orders["order_date"].dt.strftime("%Y-%m")

orders = orders.merge(products, on="product_id", how="left", validate = "many_to_one")

report = (orders.groupby(["month","city"], as_index=False)
          .agg(orders = ("order_id", "count"), revenue=("revenue","sum"))
          .sort_values(["month","revenue"], ascending=[True,False]))

print(report.head(10))
print(orders.groupby("product")["revenue"].sum().round(2))

# LOAD
report.to_parquet(
    "data/report_pandas.parquet",
    index=False
)
print("Saved", len(report),"rows")