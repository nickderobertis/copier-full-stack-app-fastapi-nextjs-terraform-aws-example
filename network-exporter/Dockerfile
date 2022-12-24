# TODO: slimmer image base
FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG CW_EXPORTER_VERSION="0.38.0-alpha"
ARG CW_EXPORTER_ARCHIVE="yet-another-cloudwatch-exporter_${CW_EXPORTER_VERSION}_Linux_x86_64.tar.gz"

RUN apt-get update && apt-get install -y wget ca-certificates
RUN wget "https://github.com/nerdswords/yet-another-cloudwatch-exporter/releases/download/v${CW_EXPORTER_VERSION}/${CW_EXPORTER_ARCHIVE}"
RUN tar -xf "$CW_EXPORTER_ARCHIVE"
RUN cp yace /usr/local/bin/yace

WORKDIR /exporter/
COPY config-template.yml /exporter
RUN mkdir /config

ARG AWS_DEFAULT_REGION
ARG APP_NAME

RUN CONFIG_CONTENTS=$(eval "echo \"$(cat config-template.yml)\"") && \
    echo "$CONFIG_CONTENTS" > /config/config.yml

EXPOSE 5000
CMD ["yace", "--config.file=/config/config.yml"]