SERVICE_NAME := kidney_io

setup:
	@poetry install --no-root

lint:
	@poetry run flake8 $(SERVICE_NAME) --select=WPS

start_db:
	docker compose up -d pg rabbitmq

start_web:
	@poetry run python -m $(SERVICE_NAME).web

start_worker:
	@poetry run python -m $(SERVICE_NAME).worker
