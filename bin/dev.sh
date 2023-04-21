#!/bin/bash

# set up the right python
source ${ENVDIR}/bin/activate

# TODO: wait for postgres at ${POSTGRES_HOST}:${POSTGRES_PORT}

cd ${SOURCEDIR} && flask run --reload --host 0.0.0.0 --port 8000