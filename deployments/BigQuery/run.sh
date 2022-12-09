docker build . -t ingest:latest
docker run --rm --network shared_network --name ingest ingest