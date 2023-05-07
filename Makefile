# ############################################################################ #
# Variables
# ############################################################################ #

export TINY_HTTP_PORT=80
export TINY_HTTPS_PORT=443

# ############################################################################ #
# Targets
# ############################################################################ #


build:
	docker compose build

start:
	docker compose up -d

dev: start 

prod:
	CMD=run.sh $(MAKE) start

restart: stop start

restart-nginx:
	docker compose stop nginx
	$(MAKE) start

stop:
	docker compose stop

logs:
	docker compose logs

bash:
	docker compose exec gunicorn bash

sh:
	docker compose exec nginx sh

py:
	docker compose exec gunicorn shell.sh

psql:
	docker compose exec db bash -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DB'


# ############################################################################ #
# Help
# ############################################################################ #

# Show this message.
help:
	@echo ""
	@echo "Usage: make <target>"
	@echo "Targets:"
	@grep -E "^[a-z,A-Z,0-9,-]+:.*" Makefile | sort | cut -d : -f 1 | xargs printf ' %s'
	@echo ""

.DEFAULT_GOAL=help
.PHONY:   bash build dev help logs prod psql py restart-nginx restart sh start stop