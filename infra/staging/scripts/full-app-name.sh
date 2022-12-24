#!/bin/bash
env_hcl_path="$(dirname $(dirname $(realpath $0)) )/env.hcl"
full_app_name_script="$(dirname $(dirname $(dirname $(realpath $0)) ) )/scripts/internal/full-app-name.sh"
$full_app_name_script $env_hcl_path