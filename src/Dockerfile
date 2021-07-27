ARG PYTAG=3-alpine
FROM python:${PYTAG}

# in stage 0 we build a venv for our selected distro which contains linting
#   and testing tools
#
# in stage 1 we have a minimal container which has an entrypoint that simply
#   rsyncs that venv to /testrig (which is hopefully a persistent volume at
#   runtime)
#
# this container is only run directly to setup a "testrig" volume; the actual
# linting and testing is run directly from that volume

# using -e and trailing semicolons on this step because of the unusual complexity
RUN set -ex; \
  apt_install() { \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get -yq update; \
    apt-get -yq --no-install-recommends install \
      build-essential \
      rsync \
      ; \
  }; \
  apk_install() { \
    apk add --no-cache \
      g++ \
      gcc \
      musl-dev \
      ; \
  }; \
  if grep -F Alpine /etc/issue; then \
    apk_install; \
  else \
    apt_install; \
  fi

COPY requirements.txt /
RUN set -x \
  && python \
    -m venv \
    --system-site-packages \
    --copies \
    --upgrade-deps \
    /testrig/venv \
  && . /testrig/venv/bin/activate \
  && pip install -r /requirements.txt

COPY ["run.sh", "/testrig/run"]
COPY ["testrig.py", "/testrig/"]

FROM alpine:3
LABEL maintainer="Backplane BV <info@backplane.be>"

RUN set -x \
  && apk add --no-cache \
    rsync \
  && true

COPY --from=0 /testrig /testrig-src

COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
