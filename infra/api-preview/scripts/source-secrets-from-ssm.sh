#!/bin/bash
# Usage: source ./scripts/source-secrets-from-ssm.sh
# GLOBAL_APP_NAME environment variable should be set before running
region_script="$(dirname $(realpath $0))/region.sh"
full_app_name_script="$(dirname $(realpath $0))/full-app-name.sh"
generated_dir="$(dirname $(dirname $(realpath ${BASH_SOURCE[0]})) )/generated"

region=$($region_script)
full_app_name=$($full_app_name_script)
source_params_script="$(dirname $(dirname $(dirname $(realpath $0)) ) )/scripts/internal/source-params.sh"

# Source staging secrets as part of the environment is shared with staging
FULL_APP_NAME="$GLOBAL_APP_NAME-staging" source $source_params_script us-east-1

# Source app-level secrets
FULL_APP_NAME="$full_app_name" source $source_params_script $region

# Source global secrets
FULL_APP_NAME="$GLOBAL_APP_NAME" source $source_params_script us-west-1 global

# Output openvpn config file from secret
mkdir -p "$generated_dir/ovpn-config"
echo "$OPENVPN_CONFIG_CONTENTS" > "$generated_dir/ovpn-config/user.ovpn"