#!/bin/bash
# NOTE: Run from api deployment dir
connection_string=$(terragrunt output -raw connection_string)

set -x
$connection_string