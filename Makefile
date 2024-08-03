include .env
export $(shell sed 's/=.*//' .env)

run:
	fastapi dev api/app.py

pretty:
	black api/

test:
	pytest tests/
