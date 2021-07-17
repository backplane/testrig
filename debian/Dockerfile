FROM python:3.9-slim-buster
LABEL maintainer="Backplane BV <info@backplane.be>"

ARG AG="env DEBIAN_FRONTEND=noninteractive apt-get -yq --no-install-recommends"

RUN set -x \
  && $AG update \
  && $AG install \
    bash \
    rsync \
  && $AG autoremove \
  && $AG clean \
  && rm -rf \
    /var/lib/apt/lists/* \
    /var/lib/dpkg/*-old /var/cache/debconf/*-old \
  && true

# this container is for populating a docker volume
# with a python venv containing testing & linting
# utilities

# this container is only run to setup that part of
# your environment. when you actually want to run
# tests, you run your application container with
# the testrig:/testrig volume mounted and the
# entrypoint set to /testrig/run.sh

COPY requirements.txt /
RUN set -x \
  && mkdir /testrig \
  && cd /testrig \
  && python -m venv venv \
  && . venv/bin/activate \
  && pip install --upgrade pip \
  && pip install -r /requirements.txt \
  && pip cache purge

# we're going to rename the testrig directory so the target volume can have
# that path at runtime
RUN set -x \
  && mv /testrig /testrig-src
COPY run.sh /testrig-src/

# when this container is run it will have
# a bind-mount or named-volume at /testrig
# our purpose is to rsync /testrig-src to /testrig

# finally our entrypoint
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
