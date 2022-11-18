from pyspark.sql import SparkSession
from pyspark.sql.streaming import *
from pyspark.sql.functions import explode, split, to_json, array, col, struct, udf

# Lecture 04 - SentimentExcersiseExtended
# Create SparkSession and configure it
spark = SparkSession.builder.appName('streamTest') \
    .master('local') \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
    
# Create a read stream from Kafka and a topic
kafka_df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", "10.123.252.231:9092") \
  .option("subscribe", "test-topic") \
  .option("startingOffsets", "earliest") \
  .load()

# Cast to string
query = kafka_df.selectExpr("CAST(value AS STRING)")

# Process data here, like adding collumns etc.
result = query # Do something here

# Add the processed data to a new topic
result.writeStream \
    .format("kafka") \
    .option("checkpointLocation", "path/to/HDFS/dir") \
    .option("kafka.bootstrap.servers", "10.123.252.231:9092") \
    .option("topic", "test-topic-2") \
    .outputMode("append") \
    .start() \
    .awaitTermination()