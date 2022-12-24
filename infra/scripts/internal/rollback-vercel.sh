#/bin/bash
# NOTE: Run from frontend deployment dir
project_id=$(terragrunt output -raw vercel_project_id)
npx vercel-rollback $project_id