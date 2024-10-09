"""
Example:
    1. run this Spark app: 
        spark-submit spark-streaming-demo-1.py localhost 9999 
    2. For Mac - In a diff SSH session, open Netcat:
        nc -lk 9999
    3. For Windows - To establish a chat communication between two windows on a Windows machine using Netcat, adhere to the subsequent steps:
        a. Open two command prompt using run as administrator windows
        b. On the first window run: ncat -l 9999
        c. On the second window run: ncat -C localhost 9999
    
    4. Enter random sentences on NC, to see these being aggregated by Spark

    Source: spark.apache.org/docs/latest/structured-streaming-programming-guide.html
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

# Keep running word count of text data received, from a data server listening on a TCP socket
spark = SparkSession \
    .builder \
    .appName("StructuredNetworkWordCount") \
    .getOrCreate()

# Decreasing logs for better readibility.
spark.sparkContext.setLogLevel("ERROR")

# Create DataFrame representing the stream of input lines from connection to localhost:9999
lines = spark \
    .readStream \
    .format("socket") \
    .option("host", "localhost") \
    .option("port", 9999) \
    .load()

# Split the lines into words
words = lines.select(
   explode(
       split(lines.value, " ")
   ).alias("word")
)

# Generate running word count
wordCounts = words.groupBy("word").count()

# Start running the query that prints the running counts to the console
query = wordCounts \
    .writeStream \
    .outputMode("complete") \
    .format("console") \
    .start()

query.awaitTermination()
