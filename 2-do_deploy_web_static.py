#!/usr/bin/python3
"""Distribute web static package to web servers
"""
from fabric.api import *
from os import path

env.hosts = ['54.165.39.238', '54.152.134.23']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Deploy web files to server
    """
    if not path.exists(archive_path):
        return False

    try:
        # Upload archive to /tmp/ directory of web servers
        put(archive_path, '/tmp/')

        # Extract archive to /data/web_static/releases/<archive_filename>/
        archive_filename = archive_path.split('/')[-1]
        release_folder = '/data/web_static/releases/{}'.format(
            archive_filename.split('.')[0])
        run('sudo mkdir -p {}'.format(release_folder))
        run('sudo tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Remove uploaded archive from web servers
        run('sudo rm /tmp/{}'.format(archive_filename))

        # Move contents to proper location and remove temporary directory
        run('sudo mv {}/web_static/* {}'.format(release_folder, release_folder))
        run('sudo rm -rf {}/web_static'.format(release_folder))

        # Remove existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Create new symbolic link
        run('sudo ln -s {} /data/web_static/current'.format(release_folder))

        return True

    except Exception as e:
        print(e)
        return False
