include .env
export $(shell sed 's/=.*//' .env)

run:
	fastapi dev api/app.py

format:
	black api/

test:
	pytest tests/
