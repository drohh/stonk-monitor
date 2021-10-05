up:
	docker-compose --env-file env up --build -d

down: 
	docker-compose --env-file env down

shell:
	docker exec -ti pipeliner bash

format:
	docker exec pipeliner python -m black -S --line-length 79 .

isort:
	docker exec pipeliner isort .

pytest:
	docker exec pipeliner pytest /code/test

type:
	docker exec pipeliner mypy --ignore-missing-imports /code

lint: 
	docker exec pipeliner flake8 /code 

ci: isort format type lint pytest

stop-etl: 
	docker exec pipeliner service cron stop
