# 🌱 tinybasilempire 🌱

Tiny Basil Empire is a small platform you can use for collecting links and small notes. It was built uising python flask, postgres, gunicorn, nginx, Google OAuth, and ZeroSSL.  It has a growing list of keyboard shortcuts and is secured with Google Authentication.

# Running

`make build` create the container
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
