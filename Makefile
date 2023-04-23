# ############################################################################ #
# Targets
# ############################################################################ #


build:
	docker compose build

run:
	docker compose up -d

start: run

restart: stop run

restart-nginx:
	docker compose stop nginx
	docker compose up -d

stop:
	docker compose stop

logs:
	docker compose logs

bash: run
	docker compose exec web bash

sh: run
	docker compose exec nginx sh

py: run
	docker compose exec web shell.sh

psql: run
	docker-compose exec db bash -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DB'

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
.PHONY:   build help logs psql py run sh stop