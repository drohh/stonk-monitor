up:
	docker-compose --env-file env up --build -d

down: 
	docker-compose --env-file env down

shell-etl:
	docker exec -ti pipeliner bash
	
stop-etl: 
	docker exec pipeliner service cron stop
