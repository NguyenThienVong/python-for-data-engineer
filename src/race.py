import time
import pandas as pd
import polars as pl

SRC = "data/raw/orders_big.csv"

t = time.perf_counter()
df = pd.read_csv(SRC)
df = df[df["quantity"] > 0 ]
df["revenue"] = df["quantity"] * df["unit_price"]
pd_out = df.groupby("city")["revenue"].sum()
print(f'pandas: {time.perf_counter() - t:.2f}')


t = time.perf_counter()
pl_out = (pl.scan_csv(SRC)
          .filter(pl.col("quantity") > 0)
          .group_by("city")
          .agg((pl.col("quantity") * pl.col("unit_price")).sum().cast(pl.Int64).alias("revenue"))
          .collect())

print(f"polars lazy:{time.perf_counter() - t:.2f} s")
print(pl_out.sort("city"))