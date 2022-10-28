from hdfs import InsecureClient
from kafka import KafkaProducer

# Create an insecure client that can read from HDFS
client = InsecureClient('http://namenode:9870', user='root')

producer = KafkaProducer(bootstrap_servers=['kafka:9092'])

# Read the alice in wonderland text file from HDFS
with client.read('/alice-in-wonderland.txt', encoding='utf-8', delimiter='\n') as reader:
  for line in reader:
    # Write each sentence in alice in wonderland to a kafka topic with a KafkaProducer
    producer.send('alice-in-kafkaland', bytes(line, 'utf-8'))
