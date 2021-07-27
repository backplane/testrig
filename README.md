# wip: TestRig

utility container for linting and testing existing uninstrumented python containers

We populate a persistent volume with linting and testing tools in a virtualenv. Next we test existing containers by attaching the volume to them and aiming the entrypoint at the volume.

TestRig uses config keys found in [`setup.cfg`](/setup.cfg) to control the directory walking it does for pylint and the exclusions it passes to bandit.

## Docker Images

This repo's images are automatically published to [backplane/testrig](https://hub.docker.com/r/backplane/testrig) on Docker Hub. Tags are in the format `{testrig_semver}-{python_version}-{distro_version}` (for example: `v0.6.3-3.7-alpine3.14`). In addition, the latest version of each distro image is available with these tags:

* `backplane/testrig:latest-3-slim` - for use testing python code in Debian-based containers
* `backplane/testrig:latest-3-alpine` - for use testing python code in alpine-based containers

### Other images

The tags are currently a bit of a mess; they're created by a build-matrix with the goal of letting users lock to: a specific version of testrig, built for a specific version of python, on a specific version of alpine or Debian.

I'd suggest starting with:

* `latest` for TestRig version
* the same minor version of python the app under test is using
* `slim` for Debian containers or `alpine` for alpine containers
* that's `latest-3.9-slim` for python 3.9 app in a Debian container.

This is the list of currently available images…

* `backplane/testrig:latest-3-slim`
* `backplane/testrig:latest-3-alpine`
* `backplane/testrig:latest-3-slim-buster`
* `backplane/testrig:latest-3-alpine3.14`
* `backplane/testrig:latest-3.6-slim`
* `backplane/testrig:latest-3.6-alpine`
* `backplane/testrig:latest-3.6-slim-buster`
* `backplane/testrig:latest-3.6-alpine3.14`
* `backplane/testrig:latest-3.7-slim`
* `backplane/testrig:latest-3.7-alpine`
* `backplane/testrig:latest-3.7-slim-buster`
* `backplane/testrig:latest-3.7-alpine3.14`
* `backplane/testrig:latest-3.8-slim`
* `backplane/testrig:latest-3.8-alpine`
* `backplane/testrig:latest-3.8-slim-buster`
* `backplane/testrig:latest-3.8-alpine3.14`
* `backplane/testrig:latest-3.9-slim`
* `backplane/testrig:latest-3.9-alpine`
* `backplane/testrig:latest-3.9-slim-buster`
* `backplane/testrig:latest-3.9-alpine3.14`
* `backplane/testrig:v0.6.3-3-slim`
* `backplane/testrig:v0.6.3-3-alpine`
* `backplane/testrig:v0.6.3-3-slim-buster`
* `backplane/testrig:v0.6.3-3-alpine3.14`
* `backplane/testrig:v0.6.3-3.6-slim`
* `backplane/testrig:v0.6.3-3.6-alpine`
* `backplane/testrig:v0.6.3-3.6-slim-buster`
* `backplane/testrig:v0.6.3-3.6-alpine3.14`
* `backplane/testrig:v0.6.3-3.7-slim`
* `backplane/testrig:v0.6.3-3.7-alpine`
* `backplane/testrig:v0.6.3-3.7-slim-buster`
* `backplane/testrig:v0.6.3-3.7-alpine3.14`
* `backplane/testrig:v0.6.3-3.8-slim`
* `backplane/testrig:v0.6.3-3.8-alpine`
* `backplane/testrig:v0.6.3-3.8-slim-buster`
* `backplane/testrig:v0.6.3-3.8-alpine3.14`
* `backplane/testrig:v0.6.3-3.9-slim`
* `backplane/testrig:v0.6.3-3.9-alpine`
* `backplane/testrig:v0.6.3-3.9-slim-buster`
* `backplane/testrig:v0.6.3-3.9-alpine3.14`

## demo

```sh
docker-compose build alpine demoapp
docker-compose run --rm testrig-setup # only needed once
docker-compose run --rm testrig
```

## License Note

The AGPL v3 LICENSE in this repo covers only the code in the repo, the built docker images contain various software packages which have their own licenses.

## Misc Dev Notes

docker "platform" | "arch" command output
----------------- | ---------------------
`amd64`           | `x86_64`
`arm64`           | `aarch64`
`arm/v7`          | `armv7l`
