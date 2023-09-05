up:
	sudo docker compose -f docker-compose-local.yaml up -d && sleep 2s && alembic upgrade head

down:
	sudo docker compose -f docker-compose-local.yaml down --remove-orphans

run tests:
	sudo docker compose -f docker-compose-local.yaml up -d && sleep 2s && python -m pytest -vv && make down