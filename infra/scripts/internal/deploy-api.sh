#!/bin/bash
# NOTE: Run from api deployment dir
output=$(terragrunt output -json)
cluster_name=$(echo $output | jq -r '.cluster_name.value')
service_name=$(echo $output | jq -r '.service_name.value')
container_name=$(echo $output | jq -r '.container_name.value')
aws_region=$(echo $output | jq -r '.aws_region.value')
base_image_name=$(echo $output | jq -r '.base_image_name.value')
ecr_address=$(echo $output | jq -r '.ecr_address.value')

# Log into docker first to fail fast if no access
aws ecr get-login-password --region "$aws_region" | docker login --username AWS --password-stdin "$ecr_address"

project_path=../../../../backend

hash=$(LC_ALL=POSIX find $project_path -type f -print0 | sort -z | xargs -0 sha1sum | sha1sum | cut -d " " -f 1)
full_image_name="$base_image_name:$hash"
echo "Building API image ${full_image_name}"
docker build -t $full_image_name $project_path

echo "Pushing API image ${full_image_name}"
docker push $full_image_name

echo "Deploying $full_image_name to $cluster_name/$service_name/$container_name"
ecs deploy "$cluster_name" "$service_name" --image "$container_name" "$full_image_name" --region "$aws_region" --timeout
1200