class Vagga(object):

    def __init__(self, path, config, arguments):
        self.base = path
        self.vagga_dir = path / '.vagga'
        self.containers = config.get('containers', {})
        self.commands = config.get('commands', {})
        self.arguments = arguments

        if arguments.command:
            self.run_commands = [arguments.command[0]]
        else:
            self.run_commands = arguments.run_multi

    def exposed_ports(self):
        return frozenset(self._exposed_ports())

    def _exposed_ports(self):
        for cmd_name in self.run_commands:
            # allow expose ports in the command
            cmd = self.commands.get(cmd_name, {})
            yield from get_ports(cmd)
            # and in children commands (for supervise)
            for child in cmd.get('children', {}).values():
                yield from get_ports(cmd)


def get_ports(cmd):
    ports = cmd.get('_expose-ports', [])
    if not isinstance(ports, list):
        raise RuntimeError("the `_expose-ports` setting must be a list"
              "of integers, got {!r} instead".format(ports))
    yield from ports

