"""
Syntax example to run on AWS:

    aws emr-serverless start-job-run \
        --application-id abcdedq3nl02mq15 \
        --execution-role-arn "arn:aws:iam::${aws_account}:role/EC2-Instance-Role-stream-lab" \
        --name spark-streaming-kafka-demo-3 \
        --job-driver '{
            "sparkSubmit": {
                "entryPoint": "s3://aws-glue-gluemsk-'${aws_account}'-eu-central-1/spark-jobs/spark-streaming-kafka-demo-3.py",
                "entryPointArguments": [
                    "--bootstrap_servers=b-2.streamlab.65t56j.c8.kafka.eu-central-1.amazonaws.com:9092,b-1.streamlab.65t56j.c8.kafka.eu-central-1.amazonaws.com:9092"
                ],
                "sparkSubmitParameters": "--conf spark.jars=s3://aws-glue-gluemsk-'${aws_account}'-eu-central-1/spark-libs/*.jar"
            }
        }'
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

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
            "b-2.streamlab.65t56j.c8.kafka.eu-central-1.amazonaws.com:9092,b-1.streamlab.65t56j.c8.kafka.eu-central-1.amazonaws.com:9092",
        "subscribe":
            "test",
        "startingOffsets":
            "earliest"
    }

# Subscribe to Kafka topic "hello"
df = spark.readStream.format("kafka").options(**kafka_options).load()

# Deserialize the value from Kafka as a String for now
deserialized_df = df.selectExpr("CAST(value AS STRING)")

# Dummy filtering or aggregation
deserialized_df = deserialized_df.where(col('value').like("%bank%"))

# Print Schema
deserialized_df.printSchema()
print('Writing data to data store...')

# Query Kafka and wait 10sec before stopping pyspark
query = deserialized_df.writeStream \
                            .outputMode("append") \
                            .format("csv") \
                            .option("checkpointLocation", "checkpoint/") \
                            .option("path", "s3a://aws-glue-gluemsk-eu-central-1/etl-output/streaming-demo-3/") \
                            .option("sep", ",") \
                            .start()

# Terminate stream
query.awaitTermination()
