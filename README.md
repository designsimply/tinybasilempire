# 🌱 tinybasilempire 🌱

Tiny Basil Empire is a small platform you can use for collecting links and small notes. It was built uising python flask, postgres, gunicorn, nginx, Google OAuth, and ZeroSSL.  It has a growing list of keyboard shortcuts and is secured with Google Authentication.

## Setup

`make build` create the container
Update DNS to point domain to your server IP address.
Create or transfer certificates to services/zerossl and services/dhparam.
Create database using schema.sql
Copy nginx.conf.template to nginx.conf and replace 'localhost' with your domain name.

## Certificates

`make install_acme_script` install acme.sh

### Manual SSL Certificate Renewal

1. Open a shell into the server where the app is being hosted.  
2. Load the environment variables stored in the `.secrets` file.
3. Open a shell into the nginx server running inside the Docker container.
4. Run the `acme.sh` script with the following options:

   * `--renew`: Forces the renewal of the certificate, even if it is not close to expiration.
   * `-d`: Specifies the domain name for which to issue or renew the SSL certificate.
   * `--force`: Forces the script to proceed with actions, even if it detects that the certificate is up to date.
   * `-ecc`: Uses ECC (Elliptic Curve Cryptography) to generate the SSL certificate, offering enhanced performance and security.

To renew the SSL certificate directly from the server, add the following target to your Makefile:

```
renew_acme_cert:
	. .secrets && \
	docker compose exec nginx sh -c "\
		/root/.acme.sh/acme.sh \
		--renew \
		-d $$DOMAIN \
		--force \
		--ecc"
```

## Running

`make run` run the container with the gunicorn server
`make shell` access bash shell
`make py` access python flask shell

## Consider something like this for the file structure

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
