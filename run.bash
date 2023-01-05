# make sure that the container is up to date
docker build -t machine_simulator . 

# spin up container
docker run \
    -it \
    --rm \
    --network host \
    machine_simulator:latest
