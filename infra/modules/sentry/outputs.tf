
output "project_details" {
  value = data.sentry_key.this
}

output "team_id" {
  value = sentry_team.this.id
}