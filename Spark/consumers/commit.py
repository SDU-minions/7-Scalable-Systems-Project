from pyspark.sql import SparkSession, Row, functions as fn
from pyspark.sql.functions import col, explode
from pyspark.sql.avro.functions import from_avro
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

spark = SparkSession.builder.appName('Commit') \
    .master('local') \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-2:29092") \
    .option("subscribe", "commits") \
    .option("startingOffsets", "earliest") \
    .load() \

commit_schema = '''{"namespace": "git.avro","type": "record","name": "Commit","fields": [{"name": "repo_names", "type": {"type": "array", "items": "string"}},{"name": "commit",  "type": "string"},{"name": "author", "type": "string"},{"name": "date", "type": "int"}]}'''

exploded_df = (df
               .withColumn("value", fn.expr("substring(value, 6, length(value)-5)"))
               .select(
                   from_avro(col("value"), jsonFormatSchema=commit_schema).alias("commit")).select("commit.*")
               .select(explode("repo_names").alias("repo_name"), col("commit"), col("author"), col("date"))
               )

commit_spark_schema = avro.load("scripts/consumers/Avro/commit-spark.avsc")
producer_config = {
    "bootstrap.servers": "kafka-1:9092,kafka-2:9092,kafka-3:9092",
    "schema.registry.url": "http://schema-registry:8081"
}

def save_commit(row: Row):
    producer = AvroProducer(producer_config, default_value_schema=commit_spark_schema)
    producer.produce(topic = "commits-exploded", value = row.asDict())
    producer.flush()

exploded_df.writeStream\
    .foreach(save_commit).start()