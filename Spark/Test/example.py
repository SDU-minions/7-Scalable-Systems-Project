from pyspark.sql import SparkSession
from pyspark.sql.streaming import *

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
  .option("kafka.bootstrap.servers", "kafka-1:19092") \
  .option("subscribe", "test-topic") \
  .option("startingOffsets", "earliest") \
  .load()
kafka_df.printSchema()

# Create a write stream and output to console
query = kafka_df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
    .writeStream \
    .format("console") \
    .option("checkpointLocation", "path/to/HDFS/dir") \
    .start()

query.awaitTermination()