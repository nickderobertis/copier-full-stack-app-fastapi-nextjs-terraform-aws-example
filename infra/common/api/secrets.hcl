terraform {
  source = "../../../modules/secrets//."
}

dependency "api" {
  config_path = "../api"
}

inputs = {
  secrets = dependency.api.outputs.secrets
  params  = dependency.api.outputs.params
}
