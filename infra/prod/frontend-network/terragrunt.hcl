include "root" {
  path = find_in_parent_folders()
}

include "common" {
  path = "${dirname(find_in_parent_folders())}/common/frontend-network.hcl"
}

inputs = {
  record_type = "A"
}
