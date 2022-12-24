#!/bin/bash
/etc/grafana/generate-from-templates.sh /etc/grafana-templates/provisioning/dashboards /etc/grafana/provisioning/dashboards
# Start grafana
exec /run.sh "$@"