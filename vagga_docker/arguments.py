import argparse


def parse_args():
    ap = argparse.ArgumentParser(
        usage="vagga [options] COMMAND [ARGS...]",
        description="""
            Runs a command in container, optionally builds container if that
            does not exists or outdated. Run `vagga` without arguments to see
            the list of commands.
        """)
    ap.add_argument("command", nargs=argparse.REMAINDER,
        help="A vagga command to run")
    ap.add_argument("-V", "--version", help="Show vagga version and exit")
    ap.add_argument("-E", "--env", "--environ", metavar="NAME=VALUE",
        help="Set environment variable for running command")
    ap.add_argument("-e", "--use-env", metavar="VAR",
        help="Propagate variable VAR into command environment")
    ap.add_argument("--ignore-owner-check", action="store_true",
        help="Ignore checking owner of the project directory")
    ap.add_argument("--no-prerequisites", action="store_true",
        help="Run only specified command(s), don't run prerequisites")
    ap.add_argument("--no-image-download", action="store_true",
        help="Do not download container image from image index.")
    ap.add_argument("--no-build", action="store_true",
        help="Do not build container even if it is out of date. \
              Return error code 29 if it's out of date.")
    ap.add_argument("--no-version-check", action="store_true",
        help="Do not run versioning code, just pick whatever \
              container version with the name was run last (or \
              actually whatever is symlinked under \
              `.vagga/container_name`). Implies `--no-build`")
    ap.add_argument("-m", "--run-multi", nargs="*",
        help="Run the following list of commands. Each without an \
              arguments. When any of them fails, stop the chain. \
              Basically it's the shortcut to `vagga cmd1 && vagga \
              cmd2` except containers for `cmd2` are built \
              beforehand, for your convenience. Also builtin commands \
              (those starting with underscore) do not work with \
              `vagga -m`")
    return ap.parse_args()
