#!/bin/bash
monitoring_dir="$(dirname $(dirname $(realpath $0)) )/monitoring"
cd $monitoring_dir
../../scripts/internal/connect-monitoring.sh