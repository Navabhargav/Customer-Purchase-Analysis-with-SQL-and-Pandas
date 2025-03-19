import pandas as pd


def main():
    #loading the data sets
    customer_purchases = pd.read_csv("customer_purchases.csv")

    product_price = pd.read_csv("product_price.csv")

    # converting into suitable data time formats
    customer_purchases["purchase_date"] = pd.to_datetime(customer_purchases["purchase_date"])
    product_price["valid_from"] = pd.to_datetime(product_price["valid_from"])
    product_price["valid_to"] = pd.to_datetime(product_price["valid_to"])

    #MPerforming a left join on product id
    merged_data = customer_purchases.merge(product_price, on="product_id", how="left")

    #Filtering transactions based on valid price periods 
    valid_transactions = merged_data[
        (merged_data["purchase_date"] >= merged_data["valid_from"]) &
        ((merged_data["purchase_date"] <= merged_data["valid_to"]) | merged_data["valid_to"].isna())]

    #Compute total cost per transaction
    valid_transactions["total_cost"] = valid_transactions["quantity"] * valid_transactions["price"]

    #declaring the condition for total cost <50, then set to 0
    valid_transactions["total_cost"] = valid_transactions["total_cost"].apply(lambda x: 0 if x < 50 else x)

    #Now identifying customers with atleast 10 purchases
    customer_counts = valid_transactions["customer_id"].value_counts()
    eligible_customers = customer_counts[customer_counts >= 10].index

    #Filter transactions for the eligible transactions
    filtered_transactions = valid_transactions[valid_transactions["customer_id"].isin(eligible_customers)]

    #Grouping product_id and country and summing them and then assigning it to result
    result = (
        filtered_transactions
        .groupby(["product_id", "country"], as_index=False)
        .agg({"total_cost": "sum"})
        .rename(columns={"total_cost": "total"})
        .sort_values(by="total", ascending=False)
    )

    #Displaying the result with print statement
    print(result)




if __name__ == "__main__":

    main()
