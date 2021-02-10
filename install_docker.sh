#!/bin/bash

docker stop swimdock_i
docker rm swimdock_i
docker build -t=swimdock .
docker run -d \
        --name swimdock_i \
        -v "$(pwd)":/app/data \
        swimdock
docker logs -f swimdock_i