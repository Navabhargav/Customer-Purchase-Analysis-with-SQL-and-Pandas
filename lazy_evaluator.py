#for dash
import dask.dataframe as dd

# Load CSV lazily (doesn't read it into memory yet)
df = dd.read_csv("large_customer_purchases.csv")

# Filter rows (lazy)
df_filtered = df[df['quantity'] > 10]

# Compute the result (triggers actual execution)
result = df_filtered.compute()


# for pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("lazy-demo").getOrCreate()

# Load data (lazy)
df = spark.read.csv("customer_purchases.csv", header=True, inferSchema=True)

# Filter and select (lazy)
filtered = df.filter(df.quantity > 10).select("customer_id", "product_id")

# Now trigger the execution
filtered.show()

