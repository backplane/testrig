# wip: TestRig

utility container for running linting and testing tools in existing python containers

## Docker Images

This repo's images are automatically published to <https://hub.docker.com/r/backplanebv/testrig>. Tags are in the format `{semver}-{distro}` (for example: `v0.3.1-debian`). In addition, the latest version of each distro image is available with these tags:

* `backplanebv/testrig:latest-debian` - for use testing python code in debian-based containers
* `backplanebv/testrig:latest-alpine` - for use testing python code in alpine-based containers

## License Note

The AGPL v3 LICENSE in this repo covers only the code in the repo, the built docker images contain various software packages which have their own licenses.

## Misc Notes

docker "platform" | "arch" command output
----------------- | ---------------------
`amd64`           | `x86_64`
`arm64`           | `aarch64`
`arm/v7`          | `armv7l`
