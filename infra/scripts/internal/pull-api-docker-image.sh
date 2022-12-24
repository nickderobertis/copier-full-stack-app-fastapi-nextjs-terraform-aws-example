#!/bin/bash
# NOTE: Run from api deployment dir
output=$(terragrunt output -json)
aws_region=$(echo $output | jq -r '.aws_region.value')
ecr_address=$(echo $output | jq -r '.ecr_address.value')
full_image_name=$(echo $output | jq -r '.full_image_name.value')

# Log into docker first to fail fast if no access
aws ecr get-login-password --region "$aws_region" | docker login --username AWS --password-stdin "$ecr_address"

echo "Pulling image ${full_image_name}"
docker pull $full_image_name