# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
import datetime

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")

# --- https://www.stackstalk.com/2022/08/avro-producer-consumer-python.html ---
repo_schema = avro.load("Avro/repo.avsc")
language_schema = avro.load("Avro/language.avsc")
commit_schema = avro.load("Avro/commit.avsc")

producer_config = { 
    "bootstrap.servers": "kafka-1:9092,kafka-2:9092,kafka-3:9092", 
    "schema.registry.url": "http://schema-registry:8081" 
} 

def saveRepos(res):
    producer = AvroProducer(producer_config, default_value_schema=repo_schema)
    for value in res.values:
        repo_name = value[0]
        data = {"repo_name": repo_name}
        producer.produce(topic = "repos", value = data)
        producer.flush()

def saveLanguages(res):
    producer = AvroProducer(producer_config, default_value_schema=language_schema)
    for val in res.values:
        repo_name = val[0]
        language = val[1]
        languages = {}
        for lang in language:
            name = lang["name"]
            bytes = lang["bytes"]
            languages[name] = bytes
        data = {
                'repo_name': repo_name,
                'languages' : languages
                }
        producer.produce(topic = "languages", value = data)
        producer.flush()

def saveCommits(res):
    producer = AvroProducer(producer_config, default_value_schema=commit_schema)
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
        producer.produce(topic = "commits", value = data)
        producer.flush()

def importRepos():
    QUERY = f"""
            select repo_name
            from bigquery-public-data.github_repos.sample_repos
            limit 10
            """
    res = bq_assistant.query_to_pandas_safe(QUERY)
    saveRepos(res)

def importLanguages():
    QUERY = f"""
            select repo_name, language
            from bigquery-public-data.github_repos.languages
            limit 10
            """
    res = bq_assistant.query_to_pandas_safe(QUERY)
    saveLanguages(res)

def importCommits():
    fromDate = datetime.datetime(2022, 1, 1).timestamp()
    toDate = datetime.datetime(2022, 12, 1).timestamp()
    QUERY = f"""
            select repo_name, commit, author.name, author.date
            from bigquery-public-data.github_repos.commits
            where author.date.seconds between {fromDate} and {toDate}
            limit 10
            """
    res = bq_assistant.query_to_pandas_safe(QUERY, max_gb_scanned=107)
    saveCommits(res)

importRepos()
importLanguages()
importCommits()
