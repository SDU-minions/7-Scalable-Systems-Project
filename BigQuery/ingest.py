# https://github.com/SohierDane/BigQuery_Helper
from bq_helper import BigQueryHelper
from kafka import KafkaProducer
import json

bq_assistant = BigQueryHelper("bigquery-public-data", "github_repos")
k_producer = KafkaProducer(bootstrap_servers=['kafka-1:9092'])

def importRepos():
    QUERY = """
            select repo_name
            from bigquery-public-data.github_repos.sample_repos
            """ # LIMIT count [ OFFSET skip_rows ]
    res = bq_assistant.query_to_pandas_safe(QUERY)

    print(res.values.size, " repos found.")
    for value in res.values:
        repo_name = value[0]
        k_producer.send('repos', bytes(repo_name, 'utf-8'))
        k_producer.flush()

def importCommits():
    QUERY = """
        select repo_name, commit, author, committer
        from bigquery-public-data.github_repos.sample_commits
        where repo_name in (
        select repo_name
        from bigquery-public-data.github_repos.sample_repos)
        and author.date > "2005-01-01 00:00:01 UTC"
        and author.date < "2016-12-13 23:59:59 UTC"
        order by author.date asc, commit
        """
    res = bq_assistant.query_to_pandas_safe(QUERY)

    print(res.values.size, " commits found.")
    for val in res.values:
        repo_name = val[0]
        commit = val[1]
        author = val[2]["name"]
        date = val[2]["date"].isoformat()
        data = {
            'repo_name ': repo_name,
            'commit' : commit,
            'author' : author,
            'date': date
            }
        k_producer.send('commits', json.dumps(data).encode('utf-8'))
        k_producer.flush()

def importFiles():
    QUERY = """
            select repo_name, path
            from bigquery-public-data.github_repos.sample_files
            where repo_name in (
            select repo_name
            from bigquery-public-data.github_repos.sample_repos)
            """
    res = bq_assistant.query_to_pandas_safe(QUERY, max_gb_scanned=6)

    print(res.values.size, " files found.")
    for val in res.values:
        repo_name = val[0]
        path = val[1]
        data = {
            'repo_name ': repo_name,
            'path' : path
            }
        k_producer.send('files', json.dumps(data).encode('utf-8'))
        k_producer.flush()

def importLanguages():
    QUERY = """
            select repo_name, language
            from bigquery-public-data.github_repos.languages
            where repo_name in (
            select repo_name
            from bigquery-public-data.github_repos.sample_repos)
            """
    res = bq_assistant.query_to_pandas_safe(QUERY)

    print(res.values.size, " languages found.")
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

importRepos()
importCommits()
importFiles()
importLanguages()

k_producer.flush()
k_producer.close()
