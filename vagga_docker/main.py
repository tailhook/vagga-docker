import os
import sys
import json
import logging
import docker
import subprocess

from . import VAGGA_IMAGE
from . import config
from . import storage
from . import runtime
from . import arguments
from . import settings
from . import network


log = logging.getLogger(__name__)


def pull_container(cli, image):
    try:
        info = cli.inspect_image(image)
    except docker.errors.NotFound:
        # Use command-line so that we don't have to reimplement progressbar
        subprocess.check_call(["docker", "pull", VAGGA_IMAGE])


def main():

    logging.basicConfig(
        # TODO(tailhook) should we use RUST_LOG like in original vagga?
        level=os.environ.get('VAGGA_LOG', 'WARNING'))

    path, cfg, suffix = config.get_config()
    args = arguments.parse_args()

    setting = settings.parse_all(path)

    vagga = runtime.Vagga(path, cfg, args)
    cli = docker.from_env(assert_hostname=False)

    if not vagga.vagga_dir.exists():
        vagga.vagga_dir.mkdir()

    pull_container(cli, VAGGA_IMAGE)

    vagga.storage_volume = storage.get_volume(vagga, cli)

    vagga.network_container = network.check_container(vagga, cli)

    setting['auto-apply-sysctl'] = True

    command_line = [
        "docker", "run",
        "--volume={}:/work".format(vagga.base),
        "--volume={}:/work/.vagga".format(vagga.storage_volume),
        "--workdir=/work/{}".format(suffix),
        "--privileged",
        "--interactive",
        "--tty",
        "--rm",
        "--net=container:" + vagga.network_container,
        "--env=VAGGA_SETTINGS=" + json.dumps(setting),
        "--env=RUST_BACKTRACE=1",
        VAGGA_IMAGE,
        "/vagga/vagga",
        "--ignore-owner-check", # this is needed on linux only
        ] + sys.argv[1:]
    log.info("Docker command-line: %r", command_line)
    # This don't work on Windows. We may figure out a better way
    os.execvp("docker", command_line)


