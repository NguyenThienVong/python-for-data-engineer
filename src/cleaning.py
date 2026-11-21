import pandas as pd

REQUIRED = ["order_id", "order_date", "city", "product_id", "quantity", "unit_price"]
CITIES = {"Lahore", "Austin", "Berlin","Nairobi", "Lima"}


def check_columns(df):
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(f"missing columns:{missing}")

def clean_orders(df):
    check_columns(df)
    df = df.copy()
    df["city"] = df["city"].str.strip().str.title()
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df["reason"] = ""
    df.loc[df["quantity"].isna(),"reason"] = "missing quantity"
    df.loc[df["quantity"] <= 0, "reason"] = "quantity not positive"
    df.loc[~df["city"].isin(CITIES), "reason"] = "unknown city"
    df.loc[df.duplicated("order_id"), "reason"] = "duplicated order_id"
    df.loc[df["unit_price"].isna(), "reason"] = "missing unit_price"
    df.loc[df["unit_price"] <= 0, "reason"] = "unit_price not positive"
    bad = df[df["reason"] != ""]
    good = df[df["reason"] == ""].drop(columns = "reason")
    good = good.astype({"quantity": "int64"})
    return good, bad


if __name__ == "__main__":
    raw = pd.read_csv("data\orders.csv")
    good, bad = clean_orders(raw)
    print(f"raw{len(raw)}, good {len(good)}, rejected {len(bad)}")
    print(bad["reason"].value_counts())
    good.to_parquet("data/orders_clean.parquet", index = False)
    bad.to_csv("data/orders_rejected.csv", index=False)
    assert good["order_id"].is_unique, "order_id must be unique"
    assert (good["quantity"] > 0).all(), "quantity must be positive"
    print("ALl check passed")
