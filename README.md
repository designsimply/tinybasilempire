# 🌱 tinybasilempire 🌱

For collecting links and small notes—a tiny empire of basil, if you will.

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
