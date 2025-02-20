# 🌱 tinybasilempire 🌱

Tiny Basil Empire is a small platform you can use for collecting links and small notes. It was built uising python flask, postgres, gunicorn, nginx, Google OAuth, and ZeroSSL.  It has a growing list of keyboard shortcuts and is secured with Google Authentication.

# Setup

`make build` create the container
Update DNS to point domain to your server IP address.
Create or transfer certificates to services/zerossl and services/dhparam.
Create database using schema.sql
Copy nginx.conf.template to nginx.conf and replace 'localhost' with your domain name.

# Certificates

`make install_acme_script` install acme.sh

# Running

`make run` run the container with the gunicorn server
`make shell` access bash shell
`make py` access python flask shell

# Consider something like this for the file structure

```
services/
   web/
      Dockerfile
      bin/
      sh/ -- delete?
      requirements.txt
      src/
          __init__.py
          app.py
          config.py
          db/
          static/
          templates/
```
