docker build . -t ingest:latest
docker run --rm --network sharednetwork --name ingest ingest