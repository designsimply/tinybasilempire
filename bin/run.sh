#!/bin/bash

# set up the right python
source ${ENVDIR}/bin/activate

# set up the environment variables
# ~/www/tinybasilempire
source ${SOURCEDIR}/.secrets

# TODO: wait for postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}

# run your application with uvicorn
gunicorn \
    --reload \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    app:app