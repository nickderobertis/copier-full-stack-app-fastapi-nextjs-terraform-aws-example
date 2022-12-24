#!/bin/bash
# Set the COMPOSE_FILE environment variable based on the values of DOCKER_ENVIRONMENT and DOCKER_INCLUDE_MONITORING.
# When DOCKER_ENVIRONMENT is set to "dev", files with the .dev.yml extension will be included.
# When DOCKER_ENVIRONMENT is set to "prod", files with the .prod.yml extension will be included.
# When DOCKER_INCLUDE_MONITORING is set to "true", files with the .monitoring.yml extension will be included.

if [ -z "$DOCKER_ENVIRONMENT" ]; then
  echo "Need the DOCKER_ENVIRONMENT env variable to be set to either 'dev' or 'prod'."
  exit 1
fi
if [ -z "$DOCKER_INCLUDE_MONITORING" ]; then
  echo "Need the DOCKER_INCLUDE_MONITORING env variable to be set to either 'true' or 'false'."
  exit 1
fi

COMPOSE_FILE="docker-compose.yml"

if [ "$DOCKER_INCLUDE_MONITORING" = "true" ]; then
  COMPOSE_FILE="$COMPOSE_FILE:docker-compose.monitoring.yml"
fi

if [ "$DOCKER_ENVIRONMENT" = "dev" ]; then
  COMPOSE_FILE="$COMPOSE_FILE:docker-compose.dev.yml"
  if [ "$DOCKER_INCLUDE_MONITORING" = "true" ]; then
    COMPOSE_FILE="$COMPOSE_FILE:docker-compose.monitoring.dev.yml"
  fi
fi

if [ "$DOCKER_ENVIRONMENT" = "prod" ]; then
  # No docker-compose.prod.yml because only monitoring is deployed to prod via docker compose
  if [ "$DOCKER_INCLUDE_MONITORING" = "true" ]; then
    COMPOSE_FILE="$COMPOSE_FILE:docker-compose.monitoring.prod.yml"
  fi
fi

export COMPOSE_FILE