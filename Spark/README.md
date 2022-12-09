# Spark

After running the docker application, Spark needs to be set up.

Execute into the Spark master container
```console
docker exec -it spark-master bin/sh
```

Create Spark environment
```console
bash scripts/create_environment.sh
```

Submit the applications to Spark (Run in two seperate terminals)
```console
bash scripts/start_commit_consumer.sh
bash scripts/start_language_consumer.sh
```