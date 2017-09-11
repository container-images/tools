#!/usr/bin/env python

import os
import re
import subprocess

RE_EXECS = "^/usr/s?bin/.*$"

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
        template_src = "| {package:%s} | {summary:%s} | {exe:%s} |"

        package_names = [len(p.name) for p in self.packages]
        package_summs = [len(p.summary) for p in self.packages]
        package_execs = [len(e) for p in self.packages for e in p.executables]
        max_name = max(package_names)
        max_summ = max(package_summs)
        max_exec = max(package_execs)

        template = template_src % (max_name, max_summ, max_exec)

        print(template.format(package="Package", summary="Summary", exe="Executables"))
        print(template.format(
            package="-" * max_name,
            summary="-" * max_summ,
            exe="-" * max_exec
        ))
        for p in self.packages:
            if p.summary and p.executables:
                first_exec = "" if not p.executables else p.executables[0]
                other_exec = "" if len(p.executables) <= 1 else p.executables[1:]
                print(template.format(package=p.name, summary=p.summary, exe=first_exec))
                for e in other_exec:
                    print(template.format(
                        package=" " * max_name,
                        summary=" " * max_summ,
                        exe=e
                    ))


def main():
    packages = os.environ["TOOLS_PACKAGES"].split(",")
    printer = Printer([Package(p) for p in packages])
    printer.display()


main()
