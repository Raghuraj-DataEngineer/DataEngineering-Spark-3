import logging
import traceback
import boto3
import json
import base64
from datetime import datetime, timedelta
from pyspark.sql import SparkSession
from pyspark.sql.functions import col


def get_secret(secret_name='dev/mysql/stream-demo-db-1', region_name='eu-central-1'):
    """
    Fetch Database credentials, from AWS Secrets Manager
    :secret_name, String: 
    :aws_region, String: AWS region id; e.g. eu-west-2

    :return: Json with AWS Secret 
    """
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # Fetching password:
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            secret_payload = json.loads(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            secret_payload = json.loads('{"message": "no data found"}')

        return secret_payload

    except Exception as e:
        logging.error('Error while retrieving credentials from Secrets Manager: {}'.format(e))
        traceback.print_exc()


def write_to_mysql(df, epoch_id):
    try:
        # Obtain credentials and connection details
        credentials_details = get_secret()

        # Hard-coded values. These can come from OS ENV variables
        db_jdbc_string = "jbdc:mysql://" + credentials_details['host_rw'] + ":3306/" + credentials_details['database_name']

        # Table name
        db_properties = {"user":credentials_details['user'], "password":credentials_details['password']}

        # write data to Database
        df.write.jdbc(url=db_jdbc_string, table=credentials_details['table_name'], properties=db_properties, mode="append")
    
    except Exception as e:
        logging.error('Error while trying to write to data store: {}'.format(e))
        traceback.print_exc()


# Create SparkSession
spark = SparkSession \
        .builder \
        .appName("02-example-mysql") \
        .config('spark.driver.extraClassPath', 's3://aws-glue-gluemsk-411292098857-eu-central-1/spark-libs/mysql-connector-j-8.1.0.jar') \
        .config('spark.executor.extraClassPath', 's3://aws-glue-gluemsk-411292098857-eu-central-1/spark-libs/mysql-connector-j-8.1.0.jar') \
        .getOrCreate()

# Decreasing logs for better readibility.
spark.sparkContext.setLogLevel("ERROR")

# Kafka local options. Hard-coded servers, as this is demo / testing code. 
kafka_options = {
        "kafka.bootstrap.servers":
            "b-2.streamlab.9xe5xv.c8.kafka.eu-central-1.amazonaws.com:9092,b-1.streamlab.9xe5xv.c8.kafka.eu-central-1.amazonaws.com:9092",
        "subscribe":
            "stream-events-t1",
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

# Call fn to write to data store
query = deserialized_df \
                .writeStream \
                .option("driver", "com.mysql.jdbc.Driver") \
                .outputMode("append") \
                .trigger(processingTime='5 seconds') \
                .foreachBatch(write_to_mysql) \
                .start()

# Terminate stream
query.awaitTermination()
