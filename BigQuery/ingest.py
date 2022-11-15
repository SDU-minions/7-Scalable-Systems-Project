# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper
from kafka import KafkaProducer
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
        for repo in repo_name:
            name = repo["name"]
            repo_names.append(name)
        commit = val[1]
        author = val[2]["name"]
        date = val[2]["date"]["seconds"]
        data = {
            'repo_names ': repo_names,
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
            select repo_name
            from bigquery-public-data.github_repos.sample_repos
            ORDER BY repo_name
            LIMIT {limit} OFFSET {offset}
            """
        res = bq_assistant.query_to_pandas_safe(QUERY)
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
                where repo_name in (
                select repo_name
                from bigquery-public-data.github_repos.sample_repos)
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
        QUERY = f"""
                select repo_name, commit, author
                from bigquery-public-data.github_repos.sample_commits
                where repo_name in (
                select repo_name
                from bigquery-public-data.github_repos.sample_repos)
                and author.date > "2005-01-01 00:00:01 UTC"
                and author.date < "2016-12-13 23:59:59 UTC"
                order by author.date asc, commit
                LIMIT {limit} OFFSET {offset}
                """
        res = bq_assistant.query_to_pandas_safe(QUERY)
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
                from bigquery-public-data.github_repos.sample_files
                where repo_name in (
                select repo_name
                from bigquery-public-data.github_repos.sample_repos)
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
#importCommits()
importLanguages()

k_producer.close()
