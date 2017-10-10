#!/usr/bin/python3

import logging
import os

import conu

import pytest


IMAGE = os.environ.get("IMAGE_NAME", "docker.io/modularitycontainers/tools")
TAG = os.environ.get("IMAGE_TAG", "latest")


class TestContainer:
    image = None
    container = None
    backend = None

    @classmethod
    def setup_class(cls):
        cls.backend = conu.DockerBackend(logging_level=logging.DEBUG)
        cls.image = cls.backend.ImageClass(IMAGE, tag=TAG)
        c = conu.DockerRunBuilder(command=["sleep", "infinity"])
        c.options += [
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
            c.options += [
                "-v", "%s:%s" % (machine_id_path, machine_id_path)
            ]
        localtime_path = "/etc/localtime"
        if os.path.exists(localtime_path):
            c.options += [
                "-v", "%s:%s" % (localtime_path, localtime_path)
            ]

        cls.container = cls.image.run_via_binary(c)

    def test_ethtool(self):
        # with self.container.mount() as fs:
        #     networks_devices = os.listdir(fs.p("/sys/class/net"))
        networks_devices = ["lo"]
        for device in networks_devices:
            self.container.execute(["ethtool", device])
        with pytest.raises(conu.ConuException):
            self.container.execute(["ethtool", "quantum-teleport"])

    def test_netstat(self):
        self.container.execute(["netstat"])

    def test_ss(self):
        self.container.execute(["ss"])

    def test_pstack(self):
        self.container.execute(["pstack", "1"])

    def test_nstat(self):
        self.container.execute(["nstat"])

    def test_numastat(self):
        self.container.execute(["numastat"])

    def test_pmap(self):
        self.container.execute(["pmap", "1"])

    def test_strace(self):
        self.container.execute(["strace", "-V"])


if __name__ == '__main__':
    pytest.main()
