#!/bin/bash

set -e

if grep "CentOS Linux 7" /etc/os-release >/dev/null; then
  cat >/etc/yum.repos.d/virt.repo <<EOF
[virt7-container-common-candidate]
name=virt7-container-common-candidate
baseurl=https://cbs.centos.org/repos/virt7-container-common-candidate/x86_64/os/
enabled=1
gpgcheck=0
EOF
  # yum remove -y python-chardet  # pip loves overlayfs
  yum install -y epel-release
  yum install -y acl nmap-ncat python2-pip python-six pyxattr python2-docker git
  pip install pytest
  pip install git+https://github.com/fedora-modularity/conu
else
  echo "Unsupported distro"
  exit 1
fi
