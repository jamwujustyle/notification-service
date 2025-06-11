# justfile

start:
    ./scripts/start-dev.sh

migrate:
    docker exec -it notification-service sh -c "aerich migrate"

upgrade:
    docker exec -it notification-service sh -c "aerich upgrade"

cli name:
    fastapi generate route {{name}}


stop:
    docker-compose stop