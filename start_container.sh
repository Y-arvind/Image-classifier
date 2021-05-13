#!/usr/bin/env bash

set -e

# start the docker container
python app.py
#docker run -d -p 5000:5000 classifier