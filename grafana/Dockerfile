FROM grafana/grafana:8.2.6

ARG APP_NAME
ARG DOMAIN_NAME
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/grafana/.local/bin:$PATH"

WORKDIR /home/grafana
RUN PASSWORD=$(echo $RANDOM | md5sum | head -c 20) && \
    openssl genrsa -des3 -passout pass:$PASSWORD -out server.pass.key 2048 && \
    openssl rsa -passin pass:$PASSWORD -in server.pass.key -out server.key && \
    rm server.pass.key && \
    openssl req -new -key server.key -out server.csr \
        -subj "/C=US/ST=Virginia/L=Fairfax/O=$APP_NAME/OU=IT Department/CN=$DOMAIN_NAME" && \
    openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
USER root
RUN cp server.crt /etc/grafana/grafana.crt && \
    cp server.key /etc/grafana/grafana.key && \
    chown -R grafana /etc/grafana/grafana.crt && \
    chown -R grafana /etc/grafana/grafana.key && \
    chmod 600 /etc/grafana/grafana.key && \
    chmod 600 /etc/grafana/grafana.crt

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python

USER grafana

RUN python3 -m ensurepip
RUN python3 -m pip install --no-cache --upgrade pip setuptools
RUN python3 -m pip install jinja-cli

USER root
COPY templates /etc/grafana-templates
COPY provisioning/ /etc/grafana/provisioning/
COPY scripts/generate-from-templates.sh /etc/grafana/generate-from-templates.sh
COPY scripts/entrypoint.sh /etc/grafana/entrypoint.sh
RUN chown -R grafana /etc/grafana-templates && \
    chown -R grafana /etc/grafana/provisioning && \
    chown -R grafana /etc/grafana/generate-from-templates.sh && \
    chown -R grafana /etc/grafana/entrypoint.sh

USER grafana
ENTRYPOINT [ "/etc/grafana/entrypoint.sh" ]

