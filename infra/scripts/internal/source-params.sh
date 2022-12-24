#!/bin/bash
# Set environment variables from SSM
# Usage:
# source-params.sh <region> <namespace>
# APP_NAME environment variable should be set before running

region="$1"
namespace="${2:-app}"

get_parameter_store_tags() {
    echo $(aws ssm get-parameters-by-path --with-decryption --path /$FULL_APP_NAME/$namespace  --region $region)
}

params_to_env () {
    params=$1

    # If .Tags does not exist we assume ssm Parameters object.
    SELECTOR="Name"

    for key in $(echo $params | /usr/bin/jq -r ".[][].${SELECTOR}"); do
                value=$(echo $params | /usr/bin/jq -r ".[][] | select(.${SELECTOR}==\"$key\") | .Value")
                key=$(echo "${key##*/}" | /usr/bin/tr ':' '_' | /usr/bin/tr '-' '_' | /usr/bin/tr '[:lower:]' '[:upper:]')
                export $key="$value"
                # Echo in a format that can be used for github actions env
                # This requires handling multiline values differently
                # https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#multiline-strings
                if (( $(grep -c . <<<"$value") > 1 )); then
                    echo "$key<<EOF"
                    echo "${!key}"
                    echo "EOF"
                else
                    echo "$key=${!key}"
                fi

    done
}
TAGS=$(get_parameter_store_tags)
params_to_env "$TAGS"