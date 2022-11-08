# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper
from kafka import KafkaProducer

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")
k_producer = KafkaProducer(bootstrap_servers=['kafka-1:9092'])

tables = bq_assistant.list_tables()

print("Tables found:")
print(tables)

def tblPrint(table):
    print("----------------------------------")
    print(table + " table scheme") 
    scheme = bq_assistant.table_schema(table)
    print(scheme)
    print("----------------------------------")

k_producer.send('test', bytes("It just works!", 'utf-8'))

for table in tables:
    # Write to a kafka topic with a KafkaProducer
    k_producer.send('tables', bytes(table, 'utf-8'))
    tblPrint(table)