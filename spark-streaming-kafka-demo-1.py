"""
Important: 
    - start your local Kafka (e.g. Conduktor)
    - run syntax: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 spark-streaming-kafka-demo-1
"""
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession.builder\
             .master("local[1]")\
             .appName("spark-app-version-x")\
             .getOrCreate()

# Decreasing logs for better readibility.
spark.sparkContext.setLogLevel("ERROR")

# Kafka local options
kafka_options = {
    "kafka.bootstrap.servers": "localhost:9092",
    "startingOffsets": "earliest", 
    "subscribe": "pyspark-series3-kafka-topic-1"
}

# Subscribe to Kafka topic "hello"
df = spark.readStream.format("kafka").options(**kafka_options).load()

# Deserialize the value from Kafka as a String for now
deserialized_df = df.selectExpr("CAST(value AS STRING)")

# Query Kafka and wait 10sec before stopping pyspark
query = deserialized_df.writeStream.outputMode("append").format("console").start()

# Terminate stream
query.awaitTermination()
