#!/bin/bash

COMPOSE_FILE="dev-db/dev-db.docker-compose.yml"

case "$1" in
  start)
    docker-compose -f "$COMPOSE_FILE" up
    ;;
  stop)
    docker-compose -f "$COMPOSE_FILE" down
    ;;
  clear)
    docker-compose -f "$COMPOSE_FILE" down -v
    ;;
  *)
    echo "Usage: $0 {start|stop|clear}"
    exit 1
    ;;
esac