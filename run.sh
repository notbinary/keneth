#!/usr/bin/env bash

# Run as a container for local test/development
docker build --tag botathon . && \
docker run -it --rm -p 5000:5000 \
    botathon
