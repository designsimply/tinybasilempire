#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout $SCRIPT_DIR/key.pem -out $SCRIPT_DIR/cert.pem