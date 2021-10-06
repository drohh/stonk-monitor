up:
	docker-compose --env-file env up --build -d

down: 
	docker-compose --env-file env down

shell-etl:
	docker exec -ti pipeliner bash
	
shell-dash:
	docker exec -ti visualizer bash

shell-db:
	docker exec -ti warehouse bash

stop-etl: 
	docker exec pipeliner service cron stop
