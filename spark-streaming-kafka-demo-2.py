"""
Syntax:
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 spark-streaming-kafka-demo-1.py
"""
from pyspark.sql import SparkSession

# Create SparkSession
spark = SparkSession \
        .builder \
        .appName("02-example-console") \
        .getOrCreate()

# Decreasing logs for better readibility.
spark.sparkContext.setLogLevel("ERROR")

# Kafka local options
kafka_options = {
        "kafka.bootstrap.servers":
            "b-2.streamlab.651ki.c8.kafka.eu-central-1.amazonaws.com:9092,b-1.streamlab.651ki.c8.kafka.eu-central-1.amazonaws.com:9092",
        "subscribe":
            "test",
        "startingOffsets":
            "earliest"
    }

# Subscribe to Kafka topic "hello"
df = spark.readStream.format("kafka").options(**kafka_options).load()

# Deserialize the value from Kafka as a String for now
deserialized_df = df.selectExpr("CAST(value AS STRING)")

# Query Kafka and wait 10sec before stopping pyspark
query = deserialized_df.writeStream \
                            .outputMode("append") \
                            .option("truncate", "false") \
                            .option("checkpointLocation", "checkpoint/") \
                            .format("console").start()

# Terminate stream
query.awaitTermination()
