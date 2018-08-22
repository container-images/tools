#!/usr/bin/python3

import logging
import os

import conu

import pytest


IMAGE = os.environ.get("IMAGE_NAME", "docker.io/modularitycontainers/tools")
TAG = os.environ.get("IMAGE_TAG", "latest")


@pytest.fixture(scope="module")
def container(request):
    with conu.DockerBackend(logging_level=logging.DEBUG) as backend:
        im = backend.ImageClass(IMAGE, tag=TAG)
        b = conu.DockerRunBuilder(command=["sleep", "infinity"])
        b.options += [
            "--net", "host",
            "--pid=host",
            "--ipc", "host",
            "-it",
            "--privileged",
            "-v", "/run:/run",
            "-v", "/:/host",
            "-v", "/var/log:/var/log",
        ]
        machine_id_path = "/etc/machine-id"
        if os.path.exists(machine_id_path):
            b.options += [
                "-v", "%s:%s" % (machine_id_path, machine_id_path)
            ]
        localtime_path = "/etc/localtime"
        if os.path.exists(localtime_path):
            b.options += [
                "-v", "%s:%s" % (localtime_path, localtime_path)
            ]
        container = im.run_via_binary(b)
    yield container
    container.stop()
    container.delete()


class TestContainer:
    def test_ethtool(self, container):
        # with self.container.mount() as fs:
        #     networks_devices = os.listdir(fs.p("/sys/class/net"))
        networks_devices = ["lo"]
        for device in networks_devices:
            container.execute(["ethtool", device])
        with pytest.raises(conu.ConuException):
            container.execute(["ethtool", "quantum-teleport"])

    def test_netstat(self, container):
        container.execute(["netstat"])

    def test_ss(self, container):
        container.execute(["ss"])

    def test_pstack(self, container):
        container.execute(["pstack", "1"])

    def test_nstat(self, container):
        container.execute(["nstat"])

    def test_numastat(self, container):
        container.execute(["numastat"])

    def test_pmap(self, container):
        container.execute(["pmap", "1"])

    def test_strace(self, container):
        container.execute(["strace", "-V"])


if __name__ == '__main__':
    pytest.main()
