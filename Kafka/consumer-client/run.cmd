docker build . -t client:latest
docker run --rm -it --network sharednetwork --name client client