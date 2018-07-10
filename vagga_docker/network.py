import logging
import docker

from . import VAGGA_IMAGE


log = logging.getLogger(__name__)


def check_container(vagga, cli):
    # use storage volume as identifier for the container
    container_name = vagga.storage_volume

    ports = _find_all_exposed_ports(vagga)
    if not _validate_container(container_name, ports, cli):
        cli.create_container(
            name=container_name,
            image=VAGGA_IMAGE,
            command=["/vagga/busybox", "sleep", "86400000"],  # 1000 days
            ports=list(ports),
            host_config=cli.create_host_config(
                port_bindings={x: x for x in ports},
            ),
        )
        cli.start(container_name)
    return container_name


def _validate_container(container_name, ports, cli):
    try:
        info = cli.inspect_container(container_name)
    except docker.errors.NotFound:
        log.debug("No such container %r", container_name)
        return False
    else:
        extra = set()
        absent = set(ports)
        for port, value in (info['NetworkSettings']['Ports'] or {}).items():
            num, kind = port.split('/')
            if kind != 'tcp':
                log.warning("Non tcp port %r", port)
            num = int(num)
            if num in ports:
                absent.remove(num)
            else:
                extra.add(num)
        if absent or extra:
            all_containers = cli.containers(filters=dict(status='running'))
            netw = 'container:' + container_name
            used_containers = [item['name']
                               for item in all_containers
                               if item['HostConfig']['NetworkMode'] == netw]
            if used_containers:
                log.warning("Exposed ports don't match, extra %r, absent %r. "
                            "You need to stop all containers so we can update "
                            "exposed ports. Running containers %r",
                            absent, extra, ', '.join(used_containers))
            else:
                cli.remove_container(container_name, force=True)
                return False

        if info['State']['Running']:
            log.debug("Container is ok and running")
            return True
        else:
            cli.remove_container(container_name)
            return False


def _find_all_exposed_ports(vagga):
    return frozenset(_exposed_ports(vagga.commands))


def _exposed_ports(commands):
    for cmd in commands.values():
        # allow expose ports in the command
        yield from _get_ports(cmd)
        # and in children commands (for supervise)
        for child in cmd.get('children', {}).values():
            yield from _get_ports(child)


def _get_ports(cmd):
    ports = cmd.get('_expose-ports', [])
    if not isinstance(ports, list):
        raise RuntimeError("the `_expose-ports` setting must be a list"
              "of integers, got {!r} instead".format(ports))
    yield from ports

