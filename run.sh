#!/usr/bin/env bash

# Run as a container for local test/development
export SERVICE_ACCOUNT_KEY=$(cat dvla-keneth-*)
export VES_API_KEY=$(cat ves-key.txt)

docker build --build-arg SERVICE_ACCOUNT_KEY --build-arg VES_API_KEY --tag botathon . && \
docker run -it --rm -p 6000:5000 botathon
