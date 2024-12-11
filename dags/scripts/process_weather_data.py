from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Simple PySpark Example") \
    .getOrCreate()

data = [
    ("Alice", 34),
    ("Bob", 23),
    ("Cathy", 45),
    ("David", 34),
    ("Eve", 29)
]
columns = ["Name", "Age"]

df = spark.createDataFrame(data, schema=columns)

filtered_df = df.filter(df["Age"] > 30).sort("Age")

transformed_df = filtered_df.withColumn(
    "AgeGroup", 
    (filtered_df["Age"] / 10).cast("int") * 10
)

print("Filtered and Transformed DataFrame:")
transformed_df.show()

spark.stop()
