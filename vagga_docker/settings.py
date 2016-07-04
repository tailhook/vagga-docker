import os
import yaml
import pathlib
import logging
import warnings


log = logging.getLogger(__name__)
SETTING_FILES = [
    '.vagga.yaml',
    '.vagga/settings.yaml',
    '.config/vagga/settings.yaml',
]


def parse_all(vagga_base):
    base_str = str(vagga_base)
    settings = {}
    for filename in SETTING_FILES:
        path = pathlib.Path(os.path.expanduser('~')) / filename
        if path.exists():
            with path.open('rb') as f:
                try:
                    data = yaml.load(f)
                except ValueError:
                    print("WARNING: error loading settings from {}: {}"
                        .format(path, data))
                    continue
            site = data.pop('site-settings', {}).get(base_str, {})
            settings.update(data)
            settings.update(site)
            if settings.pop('external-volumes', None):
                warnings.warn("External volumes are not supported "
                    " (defined in {})".format(path))
            if settings.pop('storage-dir', None):
                warnings.warn("storage-dir is not supported as we use docker"
                    " volumes for storage"
                    " (defined in {})".format(path))
            if settings.pop('cache-dir', None):
                warnings.warn("cache-dir is not supported yet"
                    " (defined in {})".format(path))
    log.debug("Got settings %r", settings)
    return settings

