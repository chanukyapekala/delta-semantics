from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("CreateSampleDeltaTable") \
    .getOrCreate()

# Sample DataFrame
df = spark.createDataFrame([
    (1, "Chanukya"),
    (2, "Shourya")
], ["id", "name"])

# Save as Delta table
df.write.format("delta").mode("overwrite").save("/tmp/delta/customers")

print("Delta table created at /tmp/delta/customers")
