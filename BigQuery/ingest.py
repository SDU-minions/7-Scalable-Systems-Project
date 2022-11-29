# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper
from kafka import KafkaProducer
import datetime
import json

# --- https://pypi.org/project/kafka-schema-registry/ ---
#from kafka_schema_registry import prepare_producer
#topic_name = "topic_name"
#SAMPLE_SCHEMA = {"type":"record", "name":"TestType", "fields":[{"name": "age", "type": "int"}, {"name": "name", "type": ["null", "string"]}]}
#producer = prepare_producer(['kafka-1:9092'],
#        f'http://schema-registry:8081',
#        topic_name, 1, 1, value_schema=SAMPLE_SCHEMA)
#producer.send(topic_name, {'age': 34})
#producer.send(topic_name, {'age': 9000, 'name': 'john'})
#producer.flush()

from confluent_kafka import Producer, KafkaException
from confluent_kafka.avro import AvroProducer
from confluent_kafka import avro

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")

# --- https://www.stackstalk.com/2022/08/avro-producer-consumer-python.html ---
repo_schema = avro.load("Avro/repo.avsc")
language_schema = avro.load("Avro/language.avsc")
commit_schema = avro.load("Avro/commit.avsc")

producer_config = {
    "bootstrap.servers": "kafka-1:9092,kafka-2:9092,kafka-3:9092",
    "schema.registry.url": "http://schema-registry:8081"
}

global_limit = 100000

def saveRepos(res):
    producer = AvroProducer(producer_config, default_value_schema=repo_schema)
    for value in res.values:
        repo_name = value[0]
        data = {"repo_name": repo_name}
        producer.produce(topic = "repos", value = data)
        producer.flush()
    producer.close()

def saveLanguages(res):
    for val in res.values:
        repo_name = val[0]
        language = val[1]
        langauges = {}
        for lang in language:
            name = lang["name"]
            bytes = lang["bytes"]
            langauges[name] = bytes
        data = {
                'repo_name': repo_name,
                'langauges' : langauges
                }
        k_producer.send('languages', json.dumps(data).encode('utf-8'))
        k_producer.flush()

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
        k_producer.send('commits', json.dumps(data).encode('utf-8'))
        k_producer.flush()

def saveFiles(res):
    for val in res.values:
        repo_name = val[0]
        path = val[1]
        data = {
            'repo_name ': repo_name,
            'path' : path
            }
        k_producer.send('files', json.dumps(data).encode('utf-8'))
        k_producer.flush()

def importRepos():
    QUERY = f"""
            select repo_name
            from bigquery-public-data.github_repos.sample_repos
            limit 10
            """
    res = bq_assistant.query_to_pandas_safe(QUERY)
    saveRepos(res)

def importLanguages():
    limit = global_limit
    offset = 0
    while (True):
        QUERY = f"""
                select repo_name, language
                from bigquery-public-data.github_repos.languages
                order by repo_name
                LIMIT {limit} OFFSET {offset}
                """
        res = bq_assistant.query_to_pandas_safe(QUERY)
        saveLanguages(res)
        count = len(res.values)
        if (count == 0):
            break
        offset += limit

def importCommits():
    limit = global_limit
    offset = 0
    while (True):
        fromDate = datetime.datetime(1998, 1, 1).timestamp()
        toDate = datetime.datetime(2002, 12, 31).timestamp()
        QUERY = f"""
                select repo_name, commit, author.name, author.date
                from bigquery-public-data.github_repos.commits
                where author.date.seconds >= {fromDate}
                and author.date.seconds <= {toDate}
                LIMIT {limit} OFFSET {offset}
                """
        res = bq_assistant.query_to_pandas_safe(QUERY, max_gb_scanned=107)
        saveCommits(res)
        count = len(res.values)
        if (count == 0):
            break
        offset += limit

def importFiles():
    limit = global_limit
    offset = 0
    while (True):
        QUERY = f"""
                select repo_name, path
                from bigquery-public-data.github_repos.files
                order by repo_name, path
                LIMIT {limit} OFFSET {offset}
                """
        res = bq_assistant.query_to_pandas_safe(QUERY)
        saveFiles(res)
        count = len(res.values)
        if (count == 0):
            break
        offset += limit

importRepos()
#importLanguages()
#importCommits()
