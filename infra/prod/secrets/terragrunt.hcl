include "root" {
  path = find_in_parent_folders()
  expose = true
}

include "common" {
  path = "${dirname(find_in_parent_folders())}/common/secrets.hcl"
  expose = true
}

inputs = {
  params = merge(
    include.common.inputs.params,
    {
      API_URL = include.root.locals.api_url
      FE_URL  = include.root.locals.fe_url
      MONITORING_URL = include.root.locals.monitoring_url
    },
  )
}