#!/bin/bash
enable_dev_only_tests="false"

e2e_dir="$(dirname $(dirname $(realpath $0)) )/../../e2e"
aws_region_script="$(dirname $(realpath $0))/region.sh"
aws_region="$(source $aws_region_script)"
full_app_name_script="$(dirname $(realpath $0))/full-app-name.sh"
full_app_name="$(source $full_app_name_script)"

cd $e2e_dir
echo "Running e2e tests for $full_app_name in region $aws_region"
APP_NAME="$full_app_name" \
    AWS_DEFAULT_REGION="$aws_region" \
    E2E_ENABLE_DEV_ONLY_TESTS="$enable_dev_only_tests" \
    pipenv run pytest -s --screenshot only-on-failure --tracing retain-on-failure