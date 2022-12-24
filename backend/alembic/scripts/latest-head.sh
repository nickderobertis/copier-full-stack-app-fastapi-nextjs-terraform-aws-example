#!/bin/bash
# NOTE: Run from root of api directory

# TODO: This would break with multiple heads

# Get the head revision in the format "2ab89177fcba (head)"
latest_head_raw=$(alembic heads)
# Extract the revision, e.g. 2ab89177fcba
latest_head=$(echo $latest_head_raw | cut -d' ' -f1)
echo $latest_head