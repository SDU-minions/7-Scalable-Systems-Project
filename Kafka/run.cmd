docker build . -t scheme:latest
docker run --rm --network shared_network --name scheme scheme