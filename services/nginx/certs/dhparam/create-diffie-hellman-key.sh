#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo openssl dhparam -out $SCRIPT_DIR/dhparam-2048.pem 2048