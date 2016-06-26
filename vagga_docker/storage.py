import logging
import docker

log = logging.getLogger(__name__)


def get_volume(vagga, dock):
    vol_path = vagga.vagga_dir / '.docker-volume'
    if vol_path.exists():
        with vol_path.open('rt') as f:
            name = f.read().strip()
        try:
            volume_info = dock.inspect_volume(name)
        except docker.errors.NotFound:
            # we don't create volumes that should already be created, this
            # because we assume that something is wrong with the system, like
            # maybe some provider of docker volumes doesn't work, or maybe you
            # connect to a wrong docker
            raise RuntimeError("It looks like volume {!r} has been deleted "
                               "manually. Remove `.vagga/.docker-volume` "
                               "to fix the problem"
                                .format(name))
        else:
            log.debug("Volume info: %r", volume_info)
            return name

    vol_name = vagga.base.parts[-1]
    try:
        dock.inspect_volume(vol_name)
    except docker.errors.NotFound:
        pass
    else:
        # same algorithm that is used for storage-dir
        for i in range(100):
            tmpname = "{}-{}".format(vol_name, i)
            try:
                dock.inspect_volume(tmpname)
            except docker.errors.NotFound:
                vol_name = tmpname
                break;
            else:
                continue
        else:
            raise RuntimeError("Can't find valid name for volume {!r}, "
                               "tried up to {!r}".format(vol_name, tmpname))
    log.info("Creating volume %r", vol_name)
    dock.create_volume(vol_name)
    with vol_path.open('wt') as file:
        file.write(vol_name)
    return vol_name
