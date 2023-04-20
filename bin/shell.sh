#!/bin/bash

# set up the right python
source ${ENVDIR}/bin/activate

# set up the environment variables
# ~/www/tinybasilempire
source ${SOURCEDIR}/.secrets

# run your application
flask shell
