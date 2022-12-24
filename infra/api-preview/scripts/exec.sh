#!/bin/bash
# Note: run from infra folder
env_path=$(dirname $(dirname $(realpath $0)) )
project_root=$(dirname $env_path)
script_path="$project_root/scripts/internal/exec.sh"
api_path="$env_path/api/api"
cd $api_path
$script_path