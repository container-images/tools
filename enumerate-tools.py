#!/usr/bin/python3

import subprocess
import re

RE_EXECS = "^/usr/s?bin/.*$"
PACKAGES = [
    "bash-completion",
    "bc",
    "bind-utils",
    "blktrace",
    "crash",
    "e2fsprogs",
    "ethtool",
    "file",
    "gcc",
    "gdb",
    "git",
    "glibc-utils",
    "gomtree",
    "htop",
    "hwloc",
    "iotop",
    "iproute",
    "iputils",
    "less",
    "ltrace",
    "mailx",
    "net-tools",
    "netsniff-ng",
    "nmap-ncat",
    "numactl",
    "numactl-devel",
    "parted",
    "pciutils",
    "perf",
    "procps-ng",
    "psmisc",
    "screen",
    "sos",
    "strace",
    "sysstat",
    "tcpdump",
    "tmux",
    "vim-enhanced",
    "xfsprogs",
]

class Package:
    def __init__(self, package_name):
        self.name = package_name
        self._files = None
        self._executables = None
        self._summary = None

    @classmethod
    def list_files(cls, package):
        cmd = ["rpm", "-ql", package]
        files = subprocess.check_output(cmd)
        return [x.decode("utf-8") for x in files.split(b"\n")]

    @classmethod
    def list_execs(cls, package):
        file_list = cls.list_files(package)
        reg = re.compile(RE_EXECS)
        result = []
        for f in file_list:
            if reg.match(f):
                result.append(f)
        return result

    @property
    def summary(self):
        if self._summary is None:
            cmd = ["rpm", "-q", "--qf", "%{SUMMARY}", self.name]
            self._summary = subprocess.check_output(cmd).strip().decode("utf-8")
        return self._summary

    @property
    def executables(self):
        if self._executables is None:
            self._executables = sorted(Package.list_execs(self.name))
        return self._executables


class Printer:
    def __init__(self, packages):
        self.packages = packages

    def display(self):
        template = "| %s | %s | %s |"
        print(template % ("Package", "Summary", "Executables"))
        print(template % ("---", "---", "---"))
        for p in self.packages:
            first_exec = "" if not p.executables else p.executables[0]
            other_exec = "" if len(p.executables) <= 1 else p.executables[1:]
            print(template % (p.name, p.summary, first_exec))
            for e in other_exec:
                print(template % ("", "", e))


def main():
    printer = Printer([Package(p) for p in PACKAGES])
    printer.display()


main()
