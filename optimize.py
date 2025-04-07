import pandas as pd

def load_and_prepare_data():
    cp = pd.read_csv("customer_purchases.csv", parse_dates=["purchase_date"])
    pp = pd.read_csv("product_price.csv", parse_dates=["valid_from", "valid_to"])
    return cp, pp

def filter_valid_prices(cp, pp):
    merged = cp.merge(pp, on="product_id", how="left")
    return merged[
        (merged["purchase_date"] >= merged["valid_from"]) &
        ((merged["purchase_date"] <= merged["valid_to"]) | merged["valid_to"].isna())
    ]

def calculate_total_cost(df):
    df["total_cost"] = df["quantity"] * df["price"]
    df.loc[df["total_cost"] < 50, "total_cost"] = 0
    return df

def filter_frequent_customers(df):
    eligible_ids = df["customer_id"].value_counts()[lambda x: x >= 10].index
    return df[df["customer_id"].isin(eligible_ids)]

def aggregate_results(df):
    return (
        df.groupby(["product_id", "country"], as_index=False)
        .agg(total=("total_cost", "sum"))
        .sort_values(by="total", ascending=False)
    )
    

def main():
    cp, pp = load_and_prepare_data()
    valid = filter_valid_prices(cp, pp)
    costed = calculate_total_cost(valid)
    filtered = filter_frequent_customers(costed)
    result = aggregate_results(filtered)
    print(result)

if __name__ == "__main__":
    main()
