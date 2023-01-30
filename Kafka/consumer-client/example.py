from kafka import KafkaConsumer
consumer = KafkaConsumer(bootstrap_servers=['kafka-1:9092','kafka-2:9092','kafka-3:9092'])

consumer.subscribe(['repos','languages','commits'])

for msg in consumer:
    print (msg)
