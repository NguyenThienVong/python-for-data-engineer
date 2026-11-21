import polars as pl

products = pl.DataFrame({
    "product_id":["P01","P02","P03","P04"],
    "product": ["Keyboard", "Mouse", "Monitor", "Webcam"]
})

orders = pl.read_csv("D:\Data\pyde\data\orders.csv", try_parse_dates=True)
print(orders.schema)

clean = (
    orders
    .with_columns(pl.col("city").str.strip_chars())
    .unique(maintain_order=True)
    .filter(pl.col("quantity") > 0)
    .with_columns(
        revenue = pl.col("quantity") * pl.col("unit_price"),
        month = pl.col("order_date").dt.strftime("%Y-%m")
    )
    .join(products, on="product_id", how = "left", validate="m:1")
)

report = (clean.group_by("month","city")
          .agg(orders=pl.len(), revenue=pl.col("revenue").sum())
          .sort(["month", "revenue"], descending=[False,True])
        )

print(report.head(5))
report.write_parquet("data/report_polars.parquet")