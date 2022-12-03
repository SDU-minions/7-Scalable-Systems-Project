# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper
import datetime
import io
import avro.schema
import avro.io

SCHEMA_PATH = "Avro/repo.avsc"
SCHEMA = avro.schema.parse(open(SCHEMA_PATH).read())

# Write Avro
writer = avro.io.DatumWriter(SCHEMA)
bytes_writer = io.BytesIO()
encoder = avro.io.BinaryEncoder(bytes_writer)
writer.write(
    {
        "repo_name": "ironbee/ironbee"
    }, encoder)
raw_bytes = bytes_writer.getvalue()

# Read Avro
bytes_reader = io.BytesIO(raw_bytes)
decoder = avro.io.BinaryDecoder(bytes_reader)
reader = avro.io.DatumReader(SCHEMA)
repo = reader.read(decoder)

#/////////////////////////////////////////////////

SCHEMA_PATH = "Avro/language.avsc"
SCHEMA = avro.schema.parse(open(SCHEMA_PATH).read())

writer = avro.io.DatumWriter(SCHEMA)
bytes_writer = io.BytesIO()
encoder = avro.io.BinaryEncoder(bytes_writer)
writer.write(
    {
        "repo_name": "zzzzzzzzzzz0/zhscript-go",
        "languages": {"Go": 60704, "Shell": 528}
    }, encoder)
raw_bytes = bytes_writer.getvalue()

bytes_reader = io.BytesIO(raw_bytes)
decoder = avro.io.BinaryDecoder(bytes_reader)
reader = avro.io.DatumReader(SCHEMA)
language = reader.read(decoder)

#/////////////////////////////////////////////////

SCHEMA_PATH = "Avro/commit.avsc"
SCHEMA = avro.schema.parse(open(SCHEMA_PATH).read())

writer = avro.io.DatumWriter(SCHEMA)
bytes_writer = io.BytesIO()
encoder = avro.io.BinaryEncoder(bytes_writer)
writer.write(
    {
        "repo_names": ["ironbee/ironbee","b1v1r/ironbee"], 
        "commit": "628796557d37ecd41741f77eeb888109a518714d", 
        "author": "Sam Baskinger",
        "date": 1368114069
    }, encoder)
raw_bytes = bytes_writer.getvalue()

bytes_reader = io.BytesIO(raw_bytes)
decoder = avro.io.BinaryDecoder(bytes_reader)
reader = avro.io.DatumReader(SCHEMA)
commit = reader.read(decoder)

exit()

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")

def saveCommits(res):
    for val in res.values:
        repo_name = val[0]
        repo_names = []
        for name in repo_name:
            repo_names.append(name)
        commit = val[1]
        author = val[2]
        date = val[3]["seconds"]
        data = {
            'repo_names': repo_names,
            'commit' : commit,
            'author' : author,
            'date': date
            }
        test = 1

limit = 1000
offset = 0
while (True):
    fromDate = datetime.datetime(2005, 1, 1).timestamp()
    toDate = datetime.datetime(2016, 12, 31).timestamp()
    QUERY = f"""
            select repo_name, commit, author.name, author.date
            from bigquery-public-data.github_repos.commits
            where author.date.seconds >= {fromDate}
            and author.date.seconds <= {toDate}
            order by author.date.seconds asc, commit
            LIMIT {limit} OFFSET {offset}
            """
    res = bq_assistant.query_to_pandas_safe(QUERY, max_gb_scanned=107)
    saveCommits(res)
    count = len(res.values)
    if (count == 0):
        break
    offset += limit

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
