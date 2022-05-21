# wip: TestRig

utility container for linting and testing existing uninstrumented Python containers

How this works:

1. We create a virtualenv with linting and testing packages (`bandit`, `black`, `flake8`, `isort`, `mypy`, `pycodestyle`, `pylint`, `pytest`) -- for specific versions of python on specific distros.
2. You create a persistent volume called `testrig` (in your compose file or manually)
3. You run the TestRig container once (aka "testrig-setup") and it rsyncs this virtualenv to your `/testrig` persistent volume.
4. When you want to test a python app, you run it's container with the `/testrig` persistent volume attached and the entrypoint set to `/testrig/run`.

This scheme means the linting and testing packages bring their own dependencies via the `/testrig` persistent volume, the app's dependencies are already in the container image. The testing utils can load all the tested app's dependencies exactly as the app normally does. **You get to fully lint & test a production container image without having to bake in any additional infrastructure.**

TestRig uses config keys found in [`setup.cfg`](/setup.cfg) to control the directory walking it does for pylint and the exclusions it passes to bandit.

## Docker Images

This repo's images are automatically published to [backplane/testrig](https://hub.docker.com/r/backplane/testrig) on Docker Hub. Tags are in the format `{testrig_semver}-{python_version}-{distro_version}` (for example: `v0.8.0-3.7-alpine3.14`). In addition, the latest version of each distro image is available with these tags:

* `backplane/testrig:latest-3-slim` - for use testing Python code in Debian-based containers
* `backplane/testrig:latest-3-alpine` - for use testing Python code in Apline-based containers

### Other images

The tags are currently a bit of a mess; they're created by a build-matrix with the goal of letting users lock to: a specific version of testrig, built for a specific version of Python, on a specific version of Apline or Debian.

I'd suggest starting with:

* `latest` for TestRig version
* the same minor version of Python the app under test is using
* `slim` for Debian containers or `alpine` for Apline containers
* that's `latest-3.9-slim` for Python 3.9 app in a Debian container.

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
