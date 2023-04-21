#!bash

# set up the right python
source .venv/bin/activate

# set up the environment variables                                                                                                                                                           ~/www/tinybasilempire
source .secrets

# run your application
flask run --cert="cert.pem" --key="priv_key.pem"
