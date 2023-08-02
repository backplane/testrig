#!/usr/bin/env python3
""" utility for invoking linters and testing in existing python containers """
import argparse
import configparser
import logging
import os
import subprocess  # nosec B404 considered
import sys
from typing import Callable, Dict, Final, List, NamedTuple, Optional, Set

DEFAULT_CONFIG_FILE: Final = "./setup.cfg"
CONFIG_SECTION_PYLINT: Final = "testrig.pylint"
CONFIG_SECTION_BANDIT: Final = "testrig.bandit"
EXCLUDE: Final = "exclude"


class Context(NamedTuple):
    """
    a typed class for passing the config/runtime context to handlers
    """

    args: argparse.Namespace
    config: Optional[configparser.ConfigParser]

    def get_setting(
        self,
        section: str,
        key: str,
    ) -> Optional[str]:
        """
        helper for getting an optional key from an optional section of an optional configparser
        """
        if self.config is not None and section in self.config:
            return self.config[section].get(key)
        return None


def call(cmd: List[str]):
    """run the given utility, logging its output"""
    # derived from https://stackoverflow.com/a/21978778
    logging.debug("running command: %s", repr(cmd))
    with subprocess.Popen(  # nosec B603 not allowing untrusted
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ) as process:
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


def source_walk(root: str, exclude: Optional[Set[str]] = None) -> List[str]:
    """
    walk the given root path looking for ".py" python source files, return the
    list, skipping files or directories of the given (optional) exclude set
    """
    results = []
    exclusions = set() if exclude is None else exclude
    full_path_compare = False

    if any(os.path.sep in excl for excl in exclusions):
        # one of the exclusions contains a slash, meaning during the walk
        # we need to compare the exclusion list to each subdir name, but with
        # the path prepended
        full_path_compare = True

    for path, subdirs, files in os.walk(root):
        # prune name-based excluded subdirs from the walk (don't descend into them)
        for epath in exclusions & set(subdirs):
            subdirs.remove(epath)

        # filter the file list (removing the name-based excluded files)
        filtered_files = set(files) - exclusions

        # filter out path-based exclusions (those containing a slash)
        if full_path_compare:
            full_subdir_paths = {os.path.join(path, subdir) for subdir in subdirs}
            full_file_paths = {os.path.join(path, filename) for filename in files}
            for epath in exclusions & full_subdir_paths:
                subdirs.remove(epath)
            filtered_files -= full_file_paths

        for file in filtered_files:
            if file.endswith(".py"):
                results.append(os.path.join(path, file))

    return results


def banner(message: str, is_error: bool = False):
    """
    prints the given message center-padded by "#", to 80 columns; delimits
    major sections in the program's output
    """
    # "2021-07-20 01:05:13,913 INFO " is 29 chars; 80-29 = 51 chars for info
    # "2021-07-20 01:05:01,950 ERROR " is 30 chars; 80-30 = 50 chars for error
    if is_error:
        logging.error(f" {message} ".center(50, "#"))
        return
    logging.info(f" {message} ".center(51, "#"))


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
    exclude_paths = None
    if (rawval := ctx.get_setting(CONFIG_SECTION_PYLINT, EXCLUDE)) is not None:
        exclude_paths = {os.path.normpath(path.strip()) for path in rawval.split(",")}
        logging.debug("loaded exclude paths: %s", exclude_paths)

    call(["pylint", "--"] + source_walk(".", exclude_paths))


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
    exclude_paths: List[str] = []
    if (rawval := ctx.get_setting(CONFIG_SECTION_BANDIT, EXCLUDE)) is not None:
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
        with open(args.config, "rt", encoding="utf-8") as configfh:
            confp = configparser.ConfigParser()
            confp.read_file(configfh, args.config)
    else:
        if args.config != DEFAULT_CONFIG_FILE:
            # if it is explicitly specified an it doesn't exist, throw an error
            logging.fatal(
                "the config file '%s' does not exist or is not a regular file",
                args.config,
            )

    # values that are settable in the config file or as args

    ctx = Context(args, confp)
    for step, handler in handlers.items():
        if step in args.skip:
            logging.debug("skipping %s", step)
            continue
        banner(step)
        try:
            handler(ctx)
        except subprocess.CalledProcessError as err:
            if step in args.failok:
                logging.warning(
                    "%s gave non-zero exit code: %s [ignoring]", step, err.returncode
                )
                continue
            logging.error("%s gave non-zero exit code: %s", step, err.returncode)
            banner("FAIL", True)
            return err.returncode
        except KeyboardInterrupt:
            logging.error("%s interrupted by user request (KeyboardInterrupt)", step)
            return 1

    banner("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
