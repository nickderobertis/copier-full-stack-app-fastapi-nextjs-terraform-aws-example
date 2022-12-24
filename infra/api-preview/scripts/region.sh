#!/bin/bash
region_hcl_path="$(dirname $(dirname $(realpath $0)) )/region.hcl"
# Parse the following line from the file at $region_hcl_path:
#   aws_region = "us-east-1"
# extracting us-east-1
aws_region="$(grep -oP '(?<=aws_region = ")[^"]*' $region_hcl_path)"
echo "$aws_region"
