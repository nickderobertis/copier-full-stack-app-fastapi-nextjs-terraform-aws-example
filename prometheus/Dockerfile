FROM prom/prometheus:v2.38.0

ARG CLOUDWATCH_EXPORTER_URL_NO_SCHEME
ARG PROMETHEUS_URL
ARG AWS_DEFAULT_REGION

COPY prometheus.yml .
RUN CONFIG_CONTENTS=$(eval "echo \"$(cat prometheus.yml)\"") && \
    echo "$CONFIG_CONTENTS" > /etc/prometheus/prometheus.yml