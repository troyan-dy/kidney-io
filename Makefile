SERVICE_NAME := kidney_io

setup:
	@poetry install --no-root

start_db:
	docker-compose up -d pg rabbit

start_web:
	@poetry run python -m $(SERVICE_NAME).web

start_worker:
	@poetry run python -m $(SERVICE_NAME).worker
