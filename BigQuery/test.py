# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")

QUERY = """
        select lang.name
        from bigquery-public-data.github_repos.languages l
        CROSS JOIN UNNEST(l.language) as lang
        GROUP BY lang.name
        ORDER BY lang.name
        """
res = bq_assistant.query_to_pandas_safe(QUERY)
print(res.values.size, " languages found.")
for value in res.values:
    language = value[0]
    print(language)

exit()

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
    top = bq_assistant.head(table, num_rows=10)
    print("----------------------------------")
    print(top)
    print("----------------------------------")
    #tblPrint(table)
