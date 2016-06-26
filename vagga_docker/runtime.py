class Vagga(object):

    def __init__(self, path, config):
        self.base = path
        self.vagga_dir = path / '.vagga'
        self.containers = config.get('containers')
        self.commands = config.get('commands')
