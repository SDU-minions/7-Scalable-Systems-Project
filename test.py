import pandas as pd
# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")

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
    tblPrint(table)
