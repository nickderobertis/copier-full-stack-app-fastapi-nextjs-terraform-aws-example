#!/bin/bash
# Use jinja cli to generate the grafana dashboard files from the templates
# in the ./templates folder.
#
# Usage:
# Accepts two arguments:
# 1. The path to the folder containing the templates.
# 2. The path to the folder where the generated files should be placed.
for file in "$1"/*.json.j2; do
    output_path="$2/$(basename "$file" .j2)"
    jinja -E APP_NAME "$file" > "$output_path"
done