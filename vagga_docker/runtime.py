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
            self.run_commands = arguments.run_multi or []

