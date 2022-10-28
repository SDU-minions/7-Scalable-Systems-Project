# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper
from kafka import KafkaProducer

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")
k_producer = KafkaProducer(bootstrap_servers=['kafka:9092'])

tables = bq_assistant.list_tables()

print("Tables found:")
print(tables)

def tblPrint(table):
    print("----------------------------------")
    print(table + " table scheme") 
    scheme = bq_assistant.table_schema(table)
    print(scheme)
    print("----------------------------------")

for table in tables:
    #tblPrint(table)
    # Write to a kafka topic with a KafkaProducer
    k_producer.send('tables', bytes(table, 'utf-8'))
