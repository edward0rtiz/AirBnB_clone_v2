#!/usr/bin/python3
""" Script that distributes an archive to your web servers using do_deploy"""

from fabric.api import local
from fabric.operations import run, put
import os.path
from fabric.api import env
env.hosts = ['35.185.103.0', '35.237.21.105']


def do_deploy(archive_path):
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        config = archive_path.split("/")[-1]
        ndir = ("/data/web_static/releases" + config.split(".")[0])
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(ndir))
        run("tar -xzf {} -C {}".format(config, ndir))
        run("rm /tmp/{}".format(config))
        run("mv {}/web_static/ {}/".format(ndir, ndir))
        run("rm -rf {}/web_static".format(ndir))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(ndir))
        return True
    except:
        return False
