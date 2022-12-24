#!/bin/bash
# Note: run from api/api environment folder
output=$(terragrunt output -json)
aws_region=$(echo $output | jq -r '.aws_region.value')
cluster_name=$(echo $output | jq -r '.cluster_name.value')
service_name=$(echo $output | jq -r '.service_name.value')

echo "Getting task ARN for service $service_name and cluster $cluster_name"
task_arn=$(aws ecs list-tasks --cluster $cluster_name --service $service_name --region $aws_region --output text --query 'taskArns[0]')
echo "Exec into task $task_arn"
aws ecs execute-command --region $aws_region --cluster $cluster_name --task $task_arn --command "sh" --interactive