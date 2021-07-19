# wip: TestRig

utility container for running linting and testing tools in existing python containers

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

```python
steps = "black isort pylint flake8 mypy bandit PASS".split()
padded_step_width = max([len(s) for s in steps]) + 2
padded_steps = [s.center(padded_step_width) for s in steps]
line_width = 80 - len('2021-07-19T11:25:25 testrig ')
print("\n".join([line.center(line_width, "#") for line in padded_steps]))
```
