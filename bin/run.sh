#!/bin/bash

# set up the right python
source ${ENVDIR}/bin/activate

# TODO: wait for postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}s

# run your application with uvicorn
cd ${SOURCEDIR} && \
    gunicorn --reload --bind 0.0.0.0:8000 --workers 4 app:app
