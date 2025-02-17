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

up:
	docker compose up -d

down:
	docker compose stop

restart: down up ps

reload_nginx:
	docker compose exec nginx sh -c 'nginx -s reload'

logs:
	docker compose logs

gunicorn_bash:
	docker compose exec gunicorn bash

nginx_sh:
	docker compose exec nginx sh

py:
	docker compose exec gunicorn shell.sh

ps:
	docker compose ps

psql:
	docker compose exec postgres bash -c 'PGPASSWORD=$$POSTGRES_PASSWORD psql -U $$POSTGRES_USER -h $$POSTGRES_HOST -d $$POSTGRES_DB_NAME'

db_backup:
	. ./.secrets \
	&& docker compose \
		run \
		--volume ./db/backups:/backups \
		postgres \
		bash -c "PGPASSWORD=$$POSTGRES_PASSWORD pg_dump -U $$POSTGRES_USER -h $$POSTGRES_HOST -d $$POSTGRES_DB_NAME --verbose --file=/backups/pg_digitalocean_$(shell date -u +'%y%m%d_%H%M%S').backup"

db_restore:
	. ./.secrets \
	&& docker compose exec postgres bash -c \
	"PGPASSWORD=$$POSTGRES_PASSWORD psql -U $$POSTGRES_USER -h $$POSTGRES_HOST -d $$POSTGRES_DB_NAME -f /backups/240109_201409.backup"

# from cheat sheet https://github.com/ChristianLempa/cheat-sheets/blob/main/docker/docker.md
db_fs_backup:
	. ./.secrets \
	&& docker run --rm --volumes-from tinybasilempire-postgres-1 -e POSTGRES_PASSWORD=$$POSTGRES_PASSWORD -v $(shell pwd):/backup busybox tar cvf /backup/backup.tar /var/lib/postgresql/data

# from cheat sheet https://github.com/ChristianLempa/cheat-sheets/blob/main/docker/docker.md
db_fs_restore:
	. ./.secrets \
	&& docker run --rm --volumes-from tinybasilempire-postgres-1 -e POSTGRES_PASSWORD=$$POSTGRES_PASSWORD -v $(shell pwd):/backup busybox sh -c "cd /var/lib/postgresql/data && tar xvf /backup/backup-from-webserver.tar --strip 1"

install_acme_script:
	. ./.secrets && \
	docker compose exec nginx sh -c 'cd ~/ ; curl https://get.acme.sh | sh -s email=$$DEV_EMAIL'

issue_acme_cert:
	. ./.secrets && \
	docker compose exec nginx sh -c '/root/.acme.sh/acme.sh --issue -d $$DOMAIN  -w /var/www/html'

test:
	. ./.secrets && \
	echo $$DOMAIN

install_acme_cert:
	. ./.secrets \
	&& echo $$DOMAIN \
	&& docker compose exec nginx sh -c "/root/.acme.sh/acme.sh --install-cert -d $$DOMAIN --fullchain-file /etc/zerossl/fullchain.cer --key-file /etc/zerossl/tinybasilempire.com.key --reloadcmd 'nginx -s reload'"

blah:
	echo docker compose exec nginx sh -c '/root/.acme.sh/acme.sh --install-cert -d $$DOMAIN \
	--fullchain-file /etc/zerossl/fullchain.cer \
	--key-file /etc/zerossl/tinybasilempire.com.key \
	--reloadcmd "nginx -s reload"'

install_acme_cron:
	docker compose exec nginx sh -c '/root/.acme.sh/acme.sh --install-cronjob'

renew_acme_cert:
	. ./.secrets && \
	docker compose exec nginx sh -c '/root/.acme.sh/acme.sh --renew -d $$DOMAIN --force --ecc'

# ############################################################################ #
# Help
# ############################################################################ #

# Show this message.
help:
	@echo ""
	@echo "Usage: make <target>"
	@echo "Targets:"
	@grep -E "^[a-z,A-Z,0-9,-,_]+:.*" Makefile | sort | cut -d : -f 1 | xargs printf ' %s'
	@echo ""

.DEFAULT_GOAL=help
.PHONY:  build db_backup down gunicorn_bash help install_acme_cert install_acme_cron install_acme_script issue_acme_cert logs nginx_sh psql py reload_nginx renew_acme_cert restart up
