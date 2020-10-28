help:
	@## Displays this message
	@echo -e "Usage:\n"
	@awk ' \
		/^[a-zA-Z_-]+:/ { \
			t = $$0; \
			sub(/:.*/, "", t) \
		} \
		/^\s+@?##/ { \
			h = $$0; \
			sub(/^\s*@*##/, "", h); \
			print "§" t "§" h; \
			t = "" \
		} \
' Makefile | column -t -s $$'§'


up:
	## Run app, daemonized
	docker-compose up -d

run:
	## Run app, interactive
	docker-compose run --rm app

run-hard:
	## Run app, interactive
	HARD=True docker-compose run --rm app

watch-run:
	## Launch app and track changes for reload
	docker-compose run --rm app watchmedo shell-command -R -W -p '*.py' -c 'python3 -m app'

down:
	## Stop app + remove containers
	docker-compose down

shell:
	## Give access to container, sourced
	docker-compose exec app /bin/bash

build:
	## Build containers
	docker-compose build

rebuild:
	## Same as build, but from scratch
	docker-compose build --no-cache

logs-app:
	## Display logs for app service
	docker-compose logs -f app

ps:
	## Show all containers processes
	docker-compose ps

test:
	## Launch unit tests once
	docker-compose run --rm app pytest .

watch-test:
	## Laucnh unit tests and track changes for reload
	docker-compose run --rm app watchmedo shell-command -R -W -p '*.py' -c 'pytest .'

play:
	## Launch game directly
	python -m app
