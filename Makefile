run:
	fastapi dev api/app.py

pretty:
	black api/

test:
	pytest tests/
