#!/bin/bash
project_dir="$(dirname $(dirname $(realpath $0)) )/../../"
cd $project_dir
raw_contents=$(COMPOSE_FILE="docker-compose.monitoring.yml:docker-compose.monitoring.prod.yml" docker-compose config --no-interpolate)
# Fix because https://github.com/docker/compose/pull/9703 is not yet released
# Replace all $$ with $ in the raw contents
echo "$raw_contents" | sed 's/\$\$/$/g'