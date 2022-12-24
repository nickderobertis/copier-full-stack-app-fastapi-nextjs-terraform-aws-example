include "root" {
  path   = find_in_parent_folders()
  expose = true
}

include "common" {
  path = "${dirname(find_in_parent_folders())}/common/frontend.hcl"
}

inputs = {
  project_name = "${include.root.inputs.app_name}-web"
  domain_name  = include.root.inputs.fe_fqdn
}
