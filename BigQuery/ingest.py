# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper
from kafka import KafkaProducer
import datetime
import json

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")
k_producer = KafkaProducer(bootstrap_servers=['kafka-1:9092'])

global_limit = 100000

def saveRepos(res):
    for value in res.values:
        repo_name = value[0]
        k_producer.send('repos', bytes(repo_name, 'utf-8'))
        k_producer.flush()

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
                'repo_name ': repo_name,
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
    limit = global_limit
    offset = 0
    while (True):
        QUERY = f"""
            select repo
            from bigquery-public-data.github_repos.commits c 
            CROSS JOIN UNNEST(c.repo_name) as repo
            GROUP BY repo
            ORDER BY repo
            LIMIT {limit} OFFSET {offset}
            """
        res = bq_assistant.query_to_pandas_safe(QUERY, max_gb_scanned=91)
        saveRepos(res)
        count = len(res.values)
        if (count == 0):
            break
        offset += limit

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
        fromDate = datetime.datetime(2012, 1, 1).timestamp()
        toDate = datetime.datetime(2016, 12, 31).timestamp()
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

#importRepos()
#importLanguages()
importCommits()

k_producer.close()
