#!/usr/bin/env python3
""" utility for invoking linters and testing in existing python containers """
import argparse
import configparser
import logging
import os
import subprocess  # nosec B404 considered
import sys
from typing import Callable, Dict, Final, List, NamedTuple, Optional


class Context(NamedTuple):
    """
    a typed class for passing the config/runtime context to handlers
    """

    args: argparse.Namespace
    config: Optional[configparser.ConfigParser]


DEFAULT_CONFIG_FILE: Final = "./setup.cfg"
CONFIG_SECTION_PYLINT: Final = "testrig.pylint"
CONFIG_SECTION_BANDIT: Final = "testrig.bandit"
EXCLUDE: Final = "exclude"


def call(cmd: List[str]):
    """run the given utility, logging its output, return pass/fail"""
    # derived from https://stackoverflow.com/a/21978778
    logging.debug("running command: %s", cmd.__repr__())
    process = subprocess.Popen(  # nosec B603 not allowing untrusted
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if process is None or process.stdout is None:  # strictly for mypy
        raise RuntimeError("unexpected subprocess response")
    with process.stdout as pipe:
        for line in iter(pipe.readline, b""):  # b'\n'-separated lines
            logging.info(
                "%s: %s",
                cmd[0],
                line.decode("utf-8", errors="replace").strip(),
            )
    exit_code = process.wait()
    if exit_code != 0:
        raise subprocess.CalledProcessError(exit_code, cmd)


def get_setting(
    config: Optional[configparser.ConfigParser], section: str, key: str
) -> Optional[str]:
    """
    helper for getting an optional key from an optional section of an optional configparser
    """
    if config is not None and section in config:
        return config[section].get(key)
    return None


def source_walk(ctx: Context) -> List[str]:
    """
    walk the cwd looking for python source files, return the list, skipping
    directories as configured
    """
    results = []
    exclude_paths = set([])
    if (rawval := get_setting(ctx.config, CONFIG_SECTION_PYLINT, EXCLUDE)) is not None:
        exclude_paths = {os.path.normpath(path.strip()) for path in rawval.split(",")}
    logging.debug("loaded exclude paths: %s", exclude_paths)
    for path, subdirs, files in os.walk("."):
        # prune excluded subdirs from the walk
        for epath in exclude_paths & set(subdirs):
            subdirs.remove(epath)
        # prune excluded files from the walk
        for file in set(files) - exclude_paths:
            if file.endswith(".py"):
                results.append(os.path.join(path, file))

    return results


def run_black(ctx: Context):
    """run the black code formatter"""
    # pylint: disable=unused-argument
    call(["black", "--check", "."])


def run_isort(ctx: Context):
    """run the isort import sorter"""
    # pylint: disable=unused-argument
    call(["isort", "--check", "."])


def run_pylint(ctx: Context):
    """run the general-purpose code linter pylint"""
    # pylint: disable=unused-argument
    call(["pylint", "--"] + source_walk(ctx))


def run_flake8(ctx: Context):
    """run the formatting-oriented linter flake8"""
    # pylint: disable=unused-argument
    call(["flake8", "."])


def run_mypy(ctx: Context):
    """run the type-checker mypy"""
    # pylint: disable=unused-argument
    call(["mypy", "."])


def run_bandit(ctx: Context):
    """run the security-oriented code linter bandit"""
    exclude_paths = []
    if (rawval := get_setting(ctx.config, CONFIG_SECTION_BANDIT, EXCLUDE)) is not None:
        exclude_paths = [path.strip() for path in rawval.split(",")]

    if exclude_paths:
        cmd = ["bandit", "-r", "-x", ",".join(exclude_paths), "."]
    else:
        cmd = ["bandit", "-r", "."]

    call(cmd)


def main() -> int:
    """
    entrypoint for direct execution
    returns an int suitable for use with sys.exit
    """
    handlers: Dict[str, Callable] = {
        "black": run_black,
        "isort": run_isort,
        "pylint": run_pylint,
        "flake8": run_flake8,
        "mypy": run_mypy,
        "bandit": run_bandit,
    }

    argp = argparse.ArgumentParser(
        "run",
        description="invoking linters and tests",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    argp.add_argument(
        "-w",
        "--workdir",
        type=str,
        default=".",
        help="the working directory from which to run tests",
    )
    argp.add_argument(
        "--skip",
        type=str,
        action="append",
        default=[],
        choices=handlers.keys(),
        help="skip running one or more of the utilities (can be specified multiple times)",
    )
    argp.add_argument(
        "--failok",
        type=str,
        action="append",
        default=[],
        choices=handlers.keys(),
        help="allow the given utilities to fail without failing the run (can be specified multiple times)",
    )
    argp.add_argument(
        "--loglevel",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="how verbosely to ouput logging info",
    )
    argp.add_argument(
        "-c",
        "--config",
        type=str,
        default=DEFAULT_CONFIG_FILE,
        help="the path to the setup.cfg file to read",
    )
    args = argp.parse_args()
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(message)s",
        level=args.loglevel,
    )

    os.chdir(args.workdir)

    # read the setup.cfg file (or whatever the user said)
    confp = None
    if os.path.isfile(args.config):
        with open(args.config, "rt") as configfh:
            confp = configparser.ConfigParser()
            confp.read_file(configfh, args.config)
    else:
        if args.config != DEFAULT_CONFIG_FILE:
            # if it is explicitly specified an it doesn't exist, throw an error
            logging.fatal(
                "the config file '%s' does not exist or is not a regular file",
                args.config,
            )

    for step in handlers:
        if step in args.skip:
            continue
        logging.info(f" {step} ".center(51, "#"))
        try:
            handlers[step](Context(args, confp))
        except subprocess.CalledProcessError as e:
            if step in args.failok:
                logging.warning(
                    "%s gave non-zero exit code: %s [ignoring]", step, e.returncode
                )
                continue
            logging.error("%s gave non-zero exit code: %s", step, e.returncode)
            logging.error(" FAIL ".center(50, "#"))
            return e.returncode
        except KeyboardInterrupt:
            logging.error("%s interrupted by user request (KeyboardInterrupt)", step)
            return 1

    logging.info(" PASS ".center(51, "#"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
