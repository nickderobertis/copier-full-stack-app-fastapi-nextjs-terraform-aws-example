#!/bin/bash
api_dir="$(dirname $(dirname $(realpath $0)) )/api/api"
cd $api_dir
../../../scripts/internal/rollback-fargate.sh