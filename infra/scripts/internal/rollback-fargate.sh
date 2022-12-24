#!/bin/bash
# NOTE: Run from api deployment folder
output=$(terragrunt output -json)
cluster_name=$(echo $output | jq -r '.cluster_name.value')
service_name=$(echo $output | jq -r '.service_name.value')
container_name=$(echo $output | jq -r '.container_name.value')
aws_region=$(echo $output | jq -r '.aws_region.value')
base_image_name=$(echo $output | jq -r '.base_image_name.value')
ecr_address=$(echo $output | jq -r '.ecr_address.value')
task_definition_family=$(echo $output | jq -r '.task_definition_family.value')

tasks=$(aws ecs list-task-definitions \
  --family-prefix "$task_definition_family" \
  --query taskDefinitionArns \
  --region $aws_region \
  --sort DESC)
second_task_definition=$(echo $tasks | jq -r '.[1]')
echo "Rolling back $cluster_name/$service_name/$container_name to $second_task_definition"
aws ecs update-service \
  --cluster "$cluster_name" \
  --service "$service_name" \
  --task-definition "$second_task_definition" \
  --region "$aws_region"