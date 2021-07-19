# wip: TestRig

utility container for linting and testing existing uninstrumented python containers

We populate a persistent volume with linting and testing tools in a virtualenv. Next we test existing containers by attaching the volume to them and aiming the entrypoint at the volume.

TestRig uses config keys found in [`setup.cfg`](/setup.cfg) to control the directory walking it does for pylint and the exclusions it passes to bandit.

## Docker Images

This repo's images are automatically published to <https://hub.docker.com/r/backplanebv/testrig>. Tags are in the format `{semver}-{distro}` (for example: `v0.3.1-debian`). In addition, the latest version of each distro image is available with these tags:

* `backplanebv/testrig:latest-debian` - for use testing python code in debian-based containers
* `backplanebv/testrig:latest-alpine` - for use testing python code in alpine-based containers

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
