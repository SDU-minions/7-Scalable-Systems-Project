spark/bin/spark-submit \
	--packages org.apache.spark:spark-avro_2.12:3.3.0,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 \
	./scripts/consumers/language.py