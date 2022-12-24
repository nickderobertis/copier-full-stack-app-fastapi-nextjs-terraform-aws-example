terraform {
  source = "../../modules/secrets//."
}

dependency "vpn" {
  config_path = "../vpn"
}

inputs = {
  secrets = dependency.vpn.outputs.secrets
}
