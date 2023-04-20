# ############################################################################ #
# Targets
# ############################################################################ #


build:
	docker compose build

run:
	docker compose up -d

stop:
	docker compose stop

logs:
	docker compose logs

sh:
	docker compose exec web bash

py:
	docker compose exec web shell

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
.PHONY:  build help logs run sh stop py