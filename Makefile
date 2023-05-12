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

prod:
	CMD=run.sh $(MAKE) start

restart: down up

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

psql:
	docker compose exec postgres bash -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DB_NAME'

install_acme_script:
	docker compose exec nginx sh -c 'cd ~/ ; curl https://get.acme.sh | sh -s email=$$DEV_EMAIL'

issue_acme_cert:
	docker compose exec nginx sh -c '/root/.acme.sh/acme.sh --issue -d $$DOMAIN -w /var/www/html'

install_acme_cert:
	/root/.acme.sh/acme.sh --install-cert -d $$DOMAIN \
	--fullchain-file /etc/zerossl/fullchain.cer \
	--key-file /etc/zerossl/tinybasilempire.com.key \
	--reloadcmd "nginx -s reload"'

install_acme_cron:
	docker compose exec nginx sh -c '/root/.acme.sh/acme.sh --install-cronjob'

renew_acme_cert:
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
.PHONY: build down gunicorn_bash help install_acme_cert install_acme_cron install_acme_script issue_acme_cert logs nginx_sh prod psql py reload_nginx renew_acme_cert restart up