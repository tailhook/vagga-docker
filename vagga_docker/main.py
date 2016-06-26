import os
import sys
import logging
import docker

from . import config
from . import storage
from . import runtime


log = logging.getLogger(__name__)


def main():

    logging.basicConfig(
        # TODO(tailhook) should we use RUST_LOG like in original vagga?
        level=os.environ.get('VAGGA_LOG', 'WARNING'))

    path, cfg, suffix = config.get_config()
    vagga = runtime.Vagga(path, cfg)
    cli = docker.Client()

    if not vagga.vagga_dir.exists():
        os.mkdir(vagga.vagga_dir)

    vagga.storage_volume = storage.get_volume(vagga, cli)

    command_line = [
        "docker", "run",
        "--volume={}:/work".format(vagga.base),
        "--workdir=/work/{}".format(suffix),
        "--privileged",
        "--interactive",
        "--tty",
        "--rm",
        "tailhook/vagga:latest",
        "/vagga/bin/vagga",
        "--ignore-owner-check", # this is needed on linux only
        ] + sys.argv[1:]
    log.info("Docker command-line: %r", command_line)
    # This don't work on Windows. We may figure out a better way
    os.execvp("docker", command_line)


