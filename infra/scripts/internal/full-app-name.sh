#!/bin/bash
# NOTE: APP_NAME env var must be set
# Usage: full-app-name.sh <env hcl path>
env_hcl_path="$1"

# Parse the following line from the file at $env_hcl_path.
#   name_suffix = "prod"
# extracting prod
# Or if it is in the format:
#   name_suffix = get_env("APP_STAGING_NAME_SUFFIX")
# extracting the value from the environment variable APP_STAGING_NAME_SUFFIX

# First try the get_env format
name_suffix="$(grep -oP '(?<=name_suffix = get_env\(")[^"]*' $env_hcl_path)"
# If it exists, then set it from that environment variable
if [ -n "$name_suffix" ]; then
    name_suffix="$(eval echo \$$name_suffix)"
else
    # Otherwise, try the simple format
    name_suffix="$(grep -oP '(?<=name_suffix = ")[^"]*' $env_hcl_path)"
fi

# Now put together the full app name with the suffix
echo "$GLOBAL_APP_NAME-$name_suffix"
