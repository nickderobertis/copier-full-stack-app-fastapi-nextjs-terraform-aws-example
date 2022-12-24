terraform {
  source = "../../modules//secrets"
}

dependency "db" {
  config_path = "../db"
}

inputs = {
  secrets = {
    DB_HOST     = dependency.db.outputs.db_host
    DB_PASSWORD = dependency.db.outputs.db_password
    DB_USER     = dependency.db.outputs.db_user
    DB_PORT     = dependency.db.outputs.db_port
  }
}
