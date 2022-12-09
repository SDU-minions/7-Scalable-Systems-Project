from pyspark.sql import SparkSession, Row, functions as fn
from pyspark.sql.functions import col, explode
from pyspark.sql.avro.functions import from_avro
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

spark = SparkSession.builder.appName('Language') \
    .master('local') \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "10.123.252.194:9092") \
    .option("subscribe", "languages") \
    .option("startingOffsets", "earliest") \
    .load() \

language_schema = '''{"type": "record","name": "Language","fields": [{"name": "repo_name",  "type": "string"},{"name": "languages", "type": {"type": "map", "values": "int"}}]}'''

exploded_df = (df
            .withColumn("value", fn.expr("substring(value, 6, length(value)-5)"))
            .select(
                from_avro(col("value"), jsonFormatSchema=language_schema).alias("repo")).select("repo.*")
            .select(col("repo_name"), explode("languages").alias("language", "language_size"))
            )

language_spark_schema = avro.load("scripts/consumers/Avro/language-spark.avsc")
producer_config = {
    "bootstrap.servers": "10.123.252.231:9092,10.123.252.194:9092,10.123.252.207:9092",
    "schema.registry.url": "http://10.123.252.231:8082"
}

def save_language(row: Row):
    producer = AvroProducer(producer_config, default_value_schema=language_spark_schema)
    producer.produce(topic = "languages-exploded", value = row.asDict())
    producer.flush()

queue = exploded_df.writeStream\
    .foreach(save_language).start()

queue.awaitTermination()